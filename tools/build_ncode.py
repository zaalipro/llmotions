#!/usr/bin/env python3
"""Build the ncode site (code.llmotions.com) from Markdown.

Python 3.9+ standard library only. The binding source format is the ncode docs contract:
front matter, a names table, partials, a small Markdown subset, `_nav.txt` manifests,
placeholders for phase-2 captures and a denylist.

    python3 tools/build_ncode.py                    build into code/
    python3 tools/build_ncode.py --draft --out DIR  placeholders drawn as dashed boxes (never commit)
    python3 tools/build_ncode.py --check            validate; no file is written
    python3 tools/build_ncode.py --check --release  also fail on placeholders, TBD and install.sh stamps
    python3 tools/build_ncode.py --check --no-drift skip the committed-output comparison while drafting
    python3 tools/build_ncode.py --import-cli PATH --ref SHA
                                                    copy the CLI's generated keyboard and settings references

Exit status: 0 ok, 1 errors, 2 usage.
"""
import argparse
import hashlib
import html
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://code.llmotions.com"
PRODUCTS = ("desktop", "cli")
PRODUCT_NAMES = {"desktop": "Desktop", "cli": "CLI"}
PRODUCT_LEDES = {
    "desktop": "The native macOS app: the workspace, the agents pane, the timeline and everything "
               "a run does, drawn live.",
    "cli": "The full-screen terminal session, the plain presenter and headless runs, on the same "
           "engine and the same database as the app.",
}
SHARED_PARTIALS = (
    "approvals", "tools", "providers", "secrets", "web-search", "mcp", "instructions",
    "project-config", "workflows", "scheduled", "research", "checkpoints", "storage",
    "privacy", "names", "together",
)
IMPORT_PARTIALS = ("keybindings", "settings")
IMPORT_SOURCES = {"keybindings": "docs/keybindings.md", "settings": "docs/settings.md"}
ALLOW_FILES = ("shared/secrets.md", "shared/names.md")
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
# Site-root paths that are served but not built here (uploaded by a separate, owner-confirmed step).
UNBUILT_PREFIXES = ("/downloads/",)

# The denylist runs on the Markdown source before name substitution. Brand and wording terms are
# not searched inside HTML comments (source comments cite real repo paths); secret-shaped terms
# are searched everywhere, comments included.
DENYLIST = (
    # The words are split so that a plain grep of this repository for the denylist finds only
    # real leaks, never this table.
    ("pipeline" "(", re.compile(r"pipeline\("), "brand"),
    ("Key" "chain", re.compile("key" "chain", re.I), "brand"),
    ("Swarm" "Code", re.compile("Swarm" "Code"), "brand"),
    ("swarm" "code", re.compile("swarm" "code"), "brand"),
    ("swarm" "_code", re.compile("swarm" "_code"), "brand"),
    ("dae" "mon", re.compile("dae" "mon", re.I), "brand"),
    ("spec N", re.compile(r"\bspec \d+", re.I), "brand"),
    ("pass N", re.compile(r"\bpass \d+", re.I), "brand"),
    ("/Us" "ers/", re.compile("/Us" "ers/"), "secret"),
    ("sk-" "ant-", re.compile("sk-" "ant-"), "secret"),
    ("sk-" "proj-", re.compile("sk-" "proj-"), "secret"),
    ("tvly" "-", re.compile("tvly" "-"), "secret"),
    ("LLMOTIONS_API_KEY" "=", re.compile("LLMOTIONS_API_KEY" "="), "secret"),
)
ALLOW_RE = re.compile(r"<!--\s*allow:\s*([^>]*?)\s*-->")
COMMENT_RE = re.compile(r"<!--.*?-->")
SOURCE_RE = re.compile(r"<!--\s*source:\s*\S.*?-->")
PARTIAL_RE = re.compile(r"^\{\{>\s*(shared|import)/([a-z0-9-]+)\s*\}\}\s*$")
NAME_RE = re.compile(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}")
CAPTURE_RE = re.compile(r"^<!--\s*capture:\s*(.*?)\s*-->\s*$")
SHOT_RE = re.compile(r"^<!--\s*shot:\s*(.*?)\s*-->\s*$")
IMPORT_REF_RE = re.compile(r"<!--\s*import-ref:\s*([0-9a-f]{7,40})\s*-->")
LBRACE = "\x00LB\x00"


class Report:
    """Collects errors and warnings with a location."""

    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, where, msg):
        self.errors.append("%s: %s" % (where, msg))

    def warn(self, where, msg):
        self.warnings.append("%s: %s" % (where, msg))


# ----------------------------------------------------------------------------- source files

def rel(path, base):
    try:
        return str(Path(path).relative_to(base))
    except ValueError:
        return str(path)


def load_names(content, rep):
    path = content / "names.json"
    if not path.is_file():
        rep.error(rel(path, ROOT), "names.json is missing")
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        rep.error(rel(path, ROOT), "not valid JSON: %s" % exc)
        return {}
    if not isinstance(data, dict) or not all(
            isinstance(k, str) and isinstance(v, str) for k, v in data.items()):
        rep.error(rel(path, ROOT), "must be an object of string values")
        return {}
    return data


def parse_nav(path, rep):
    """`# Group` lines and `slug | Sidebar title` entries -> [(group, [(slug, title, line)])]."""
    groups = []
    seen = set()
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        where = "%s:%d" % (rel(path, ROOT), n)
        if line.startswith("# "):
            groups.append((line[2:].strip(), []))
            continue
        if "|" not in line:
            rep.error(where, "expected `slug | Sidebar title` or `# Group`")
            continue
        slug, title = [part.strip() for part in line.split("|", 1)]
        if not SLUG_RE.match(slug):
            rep.error(where, "slug %r is not lowercase a-z0-9-" % slug)
            continue
        if slug in seen:
            rep.error(where, "slug %r is listed twice" % slug)
            continue
        seen.add(slug)
        if not groups:
            groups.append(("", []))
        groups[-1][1].append((slug, title, n))
    return groups


def split_front_matter(text, where, rep):
    """Returns (meta, body_lines, first_body_line_number)."""
    lines = text.split("\n")
    meta = {}
    if not lines or lines[0].strip() != "---":
        rep.error(where, "front matter missing: the page must start with `---`")
        return meta, lines, 1
    for i in range(1, len(lines)):
        line = lines[i]
        if line.strip() == "---":
            break
        m = re.match(r"^(title|description):\s*(.*?)\s*$", line)
        if not m:
            rep.error("%s:%d" % (where, i + 1), "front matter allows only `title:` and `description:`")
            continue
        meta[m.group(1)] = m.group(2)
    else:
        rep.error(where, "front matter is not closed with `---`")
        return meta, [], len(lines) + 1
    for key in ("title", "description"):
        if not meta.get(key):
            rep.error(where, "front matter has no %s" % key)
    return meta, lines[i + 1:], i + 2


def denylist_scan(label, lines, first_line, rep, allow_ok):
    """Scans source lines (before name substitution). Returns the number of hits."""
    hits = 0
    in_comment = False
    for offset, line in enumerate(lines):
        where = "%s:%d" % (label, first_line + offset)
        allowed = set()
        for m in ALLOW_RE.finditer(line):
            allowed.update(t.strip() for t in m.group(1).split(",") if t.strip())
        if allowed and not allow_ok:
            rep.warn(where, "an `allow:` comment outside shared/secrets.md and shared/names.md is ignored")
            allowed = set()
        # the parts of the line outside HTML comments (comments may span lines)
        visible = []
        rest = line
        while rest:
            if in_comment:
                end = rest.find("-->")
                if end < 0:
                    rest = ""
                else:
                    rest = rest[end + 3:]
                    in_comment = False
            else:
                start = rest.find("<!--")
                if start < 0:
                    visible.append(rest)
                    rest = ""
                else:
                    visible.append(rest[:start])
                    rest = rest[start + 4:]
                    in_comment = True
        visible_text = " ".join(visible)
        for term, pattern, kind in DENYLIST:
            haystack = line if kind == "secret" else visible_text
            if pattern.search(haystack) and term not in allowed:
                rep.error(where, "denylisted %r" % term)
                hits += 1
    return hits


def substitute_names(line, names, where, rep):
    """`{{name}}` -> value; `\\{{` -> a literal `{{`; an unknown name is a build error."""
    line = line.replace("\\{{", LBRACE)

    def repl(m):
        key = m.group(1)
        if key not in names:
            rep.error(where, "unknown name {{%s}}" % key)
            return m.group(0)
        return names[key]

    out = NAME_RE.sub(repl, line)
    if "{{" in out and not NAME_RE.search(out):
        rep.error(where, "an unclosed or malformed `{{`")
    return out.replace(LBRACE, "{{")


class Source:
    """One Markdown file after partial expansion: (text, file label, line number) per line."""

    def __init__(self):
        self.lines = []
        self.imports = {}   # import name -> ref

    def extend(self, lines, label, first):
        for offset, text in enumerate(lines):
            self.lines.append((text, label, first + offset))


def read_partial(content, kind, name, cache, rep):
    """Returns (lines, label) of a partial, scanning it once for the denylist and a source comment."""
    key = (kind, name)
    if key in cache:
        return cache[key]
    path = content / ("docs/shared" if kind == "shared" else "import") / (name + ".md")
    label = rel(path, ROOT)
    if not path.is_file():
        cache[key] = None
        return None
    lines = path.read_text(encoding="utf-8").split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    text = "\n".join(lines)
    if not SOURCE_RE.search(text):
        rep.error(label, "no `<!-- source: … -->` comment")
    before = len(rep.errors)
    denylist_scan(label, lines, 1, rep, allow_ok=("%s/%s.md" % (kind, name)) in ALLOW_FILES)
    if kind == "import" and len(rep.errors) > before:
        rep.warn(label, "denylist hits in a generated reference: fix them at the source (lane A), "
                        "never by hand")
    for n, line in enumerate(lines, 1):
        if line.startswith("## ") or line.startswith("# "):
            rep.error("%s:%d" % (label, n), "a partial starts at `###`")
        if "{{>" in line:
            rep.error("%s:%d" % (label, n), "partials do not nest")
    ref = IMPORT_REF_RE.search(text)
    cache[key] = (lines, label, ref.group(1) if ref else None)
    return cache[key]


def expand(body, label, first, content, cache, rep):
    """Page body lines -> Source with partials inserted in place."""
    src = Source()
    for offset, line in enumerate(body):
        n = first + offset
        m = PARTIAL_RE.match(line.strip()) if line.lstrip().startswith("{{>") else None
        if m:
            kind, name = m.groups()
            known = SHARED_PARTIALS if kind == "shared" else IMPORT_PARTIALS
            if name not in known:
                rep.error("%s:%d" % (label, n), "%s/%s is not in the fixed partial set" % (kind, name))
                continue
            part = read_partial(content, kind, name, cache, rep)
            if part is None:
                rep.error("%s:%d" % (label, n), "missing partial %s/%s" % (kind, name))
                continue
            plines, plabel, ref = part
            if kind == "import":
                src.imports[name] = ref
            src.extend(plines, plabel, 1)
        elif "{{>" in line:
            rep.error("%s:%d" % (label, n), "a partial include must be alone on its line")
            src.extend([line], label, n)
        else:
            src.extend([line], label, n)
    return src


# ----------------------------------------------------------------------------- Markdown subset

FENCE_RE = re.compile(r"^(\s*)```\s*([A-Za-z0-9_+.-]*)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
EXPLICIT_ID_RE = re.compile(r"\s*\{#([a-z0-9][a-z0-9-]*)\}\s*$")
LIST_RE = re.compile(r"^(\s*)(-|\d+\.)\s+(.*)$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")
IMAGE_LINE_RE = re.compile(r"^!\[([^\]]*)\]\(([^)\s]+)\)$")
CALLOUT_RE = re.compile(r"^\*\*(Note|Tip|Warning)\*\*[:.]?\s*(.*)$")
CODE_SPAN_RE = re.compile(r"(`+)(.+?)\1")
RAW_TAG_RE = re.compile(r"</?(a|b|br|code|details|div|em|i|iframe|img|kbd|li|ol|p|pre|script|span|"
                        r"strong|style|summary|sub|sup|table|td|th|tr|u|ul)\b[^>]*>", re.I)
ITALIC_RE = re.compile(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])")


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def plain_inline(text):
    """Markdown inline -> plain text (ids, TOC, search)."""
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[\[([^\]]+?)\]\]", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = text.replace("**", "").replace("`", "")
    text = ITALIC_RE.sub(r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def attr(value):
    return value.replace('"', "&quot;")


def check_url(url, where, rep):
    if url.startswith(("/", "#", "https://", "http://", "mailto:")):
        if url.startswith("//"):
            rep.error(where, "protocol-relative link %r" % url)
        return
    rep.error(where, "link %r must be root-absolute (`/docs/…/`) or a full URL" % url)


SHOTS_PREFIX = "/assets/shots/"


def image_size(data):
    """(width, height) in pixels of a PNG or WebP (lossy, lossless or extended), else None."""
    if data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR":
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        chunk = data[12:16]
        if chunk == b"VP8 " and data[23:26] == b"\x9d\x01\x2a":
            return (int.from_bytes(data[26:28], "little") & 0x3FFF,
                    int.from_bytes(data[28:30], "little") & 0x3FFF)
        if chunk == b"VP8L" and data[20:21] == b"\x2f":
            bits = int.from_bytes(data[21:25], "little")
            return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
        if chunk == b"VP8X":
            return int.from_bytes(data[24:27], "little") + 1, int.from_bytes(data[27:30], "little") + 1
    return None


def figure_img(url, alt, images):
    """A block image. Its width/height (so the page does not jump while it loads) come from the
    file; screenshots under /assets/shots/ are 2x captures, so they declare half their pixels."""
    size = images(url) if images else None
    dims = ""
    if size:
        w, h = size
        if url.startswith(SHOTS_PREFIX):
            w, h = max(1, round(w / 2)), max(1, round(h / 2))
        dims = ' width="%d" height="%d"' % (w, h)
    return ('<figure><img src="%s" alt="%s"%s loading="lazy" decoding="async"></figure>'
            % (attr(url), attr(html.escape(alt, quote=False)), dims))


def render_inline(text, where, rep):
    codes = []

    def keep(m):
        codes.append("<code>%s</code>" % html.escape(m.group(2).strip(" ") or m.group(2), quote=False))
        return "\x01%d\x01" % (len(codes) - 1)

    text = CODE_SPAN_RE.sub(keep, text)
    if RAW_TAG_RE.search(text):
        rep.warn(where, "raw HTML is not allowed; it is shown as text")
    text = html.escape(text, quote=False)
    text = re.sub(r"\[\[([^\]]+?)\]\]", r"<kbd>\1</kbd>", text)

    def image(m):
        check_url(m.group(2), where, rep)
        return '<img src="%s" alt="%s" loading="lazy">' % (attr(m.group(2)), attr(m.group(1)))

    def link(m):
        check_url(m.group(2), where, rep)
        return '<a href="%s">%s</a>' % (attr(m.group(2)), m.group(1))

    text = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", image, text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = ITALIC_RE.sub(r"<em>\1</em>", text)
    return re.sub("\x01(\\d+)\x01", lambda m: codes[int(m.group(1))], text)


def split_cells(line):
    """A pipe-table row -> cells; `\\|` and pipes inside code spans stay in the cell."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells, cur, i, tick = [], [], 0, 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur.append("|")
            i += 2
            continue
        if c == "`":
            j = i
            while j < len(s) and s[j] == "`":
                j += 1
            run = j - i
            if tick == 0 and s.find("`" * run, j) >= 0:
                tick = run
            elif tick == run:
                tick = 0
            cur.append(s[i:j])
            i = j
            continue
        if c == "|" and tick == 0:
            cells.append("".join(cur).strip())
            cur = []
        else:
            cur.append(c)
        i += 1
    cells.append("".join(cur).strip())
    return cells


class Doc:
    """The rendered body of one page."""

    def __init__(self):
        self.parts = []
        self.headings = []        # (level, plain text, inline html, id)
        self.ids = {}
        self.sections = [["", "", []]]   # [heading, anchor, text chunks]
        self.placeholders = []    # (kind, payload, where)

    def text(self, chunk):
        if chunk:
            self.sections[-1][2].append(chunk)

    def unique_id(self, base):
        base = base or "section"
        n = self.ids.get(base, 0) + 1
        self.ids[base] = n
        return base if n == 1 else "%s-%d" % (base, n)


def preprocess(src, names, rep):
    """Names substituted, comments removed outside fences, placeholders turned into tokens.

    Returns [(kind, text, where)] with kind in line | capture | shot."""
    out = []
    in_fence = False
    in_comment = False
    for text, label, n in src.lines:
        where = "%s:%d" % (label, n)
        text = substitute_names(text, names, where, rep)
        if FENCE_RE.match(text) and not in_comment:
            in_fence = not in_fence
            out.append(("line", text, where))
            continue
        if in_fence:
            out.append(("line", text, where))
            continue
        if not in_comment:
            m = CAPTURE_RE.match(text.strip()) or SHOT_RE.match(text.strip())
            if m:
                kind = "capture" if CAPTURE_RE.match(text.strip()) else "shot"
                out.append((kind, m.group(1), where))
                continue
        kept = []
        rest = text
        had_comment = in_comment      # a line that starts inside a comment is touched by it
        while rest:
            if in_comment:
                end = rest.find("-->")
                if end < 0:
                    rest = ""
                else:
                    rest = rest[end + 3:]
                    in_comment = False
            else:
                start = rest.find("<!--")
                if start < 0:
                    kept.append(rest)
                    rest = ""
                else:
                    had_comment = True
                    kept.append(rest[:start])
                    rest = rest[start + 4:]
                    in_comment = True
        line = "".join(kept).rstrip() if had_comment or in_comment else text
        if (had_comment or in_comment) and not line.strip():
            continue      # a comment-only line leaves no trace, not even a paragraph break
        out.append(("line", line, where))
    if in_fence:
        rep.error(src.lines[-1][1] if src.lines else "?", "a code fence is not closed")
    return out


def validate_placeholder(kind, payload, where, rep):
    parts = [p.strip() for p in payload.split("|")]
    if kind == "capture":
        ok = (len(parts) == 3 and re.match(r"^cli/[a-z0-9-]+$", parts[0])
              and re.match(r"^\d+x\d+$", parts[2]) and parts[1])
        if not ok:
            rep.error(where, "capture placeholder must be `cli/<name> | <what> | <cols>x<rows>`")
    else:
        ok = (len(parts) in (2, 3) and re.match(r"^(cli|desktop)/[a-z0-9-]+\.png$", parts[0])
              and parts[-1] and (len(parts) == 2 or parts[1] == "owner"))
        if not ok:
            rep.error(where, "shot placeholder must be `desktop/<name>.png | <what>` "
                             "(owner shots: `desktop/gatekeeper-<n>.png | owner | <what>`)")
    return parts


def render_code(lang, body, where, rep):
    code = html.escape("\n".join(body), quote=False)
    if lang == "term":
        return '<div class="term"><pre>%s</pre></div>' % code
    if not lang:
        rep.error(where, "a code fence needs a language (```sh, ```text, ```term …)")
    return ('<div class="code"><div class="code-bar"><span class="code-lang">%s</span>'
            '<button type="button" class="copy" hidden>Copy</button></div>'
            '<pre><code%s>%s</code></pre></div>'
            % (html.escape(lang or "text"), ' class="language-%s"' % attr(lang) if lang else "", code))


def render_markdown(items, rep, draft=False, doc=None, images=None):
    """[(kind, text, where)] -> Doc. images: url -> (width, height) or None, for block images."""
    doc = doc or Doc()
    i = 0
    para = []

    def flush():
        if para:
            body = " ".join(t.strip() for t, _ in para)
            doc.parts.append("<p>%s</p>" % render_inline(body, para[0][1], rep))
            doc.text(plain_inline(body))
            del para[:]

    while i < len(items):
        kind, text, where = items[i]
        if kind in ("capture", "shot"):
            flush()
            parts = validate_placeholder(kind, text, where, rep)
            doc.placeholders.append((kind, text, where))
            if draft:
                if kind == "capture":
                    label = "Terminal capture · " + " · ".join([parts[0]] + parts[2:3])
                    what = parts[1] if len(parts) > 1 else ""
                else:
                    label = "Screenshot · " + " · ".join(parts[:-1])
                    what = parts[-1] if len(parts) > 1 else ""
                doc.parts.append('<div class="ph ph-%s" role="note"><span class="ph-kind">%s</span>'
                                 '<span class="ph-what">%s</span></div>'
                                 % (kind, html.escape(label, quote=False), html.escape(what, quote=False)))
            i += 1
            continue
        stripped = text.strip()
        fence = FENCE_RE.match(text)
        if fence:
            flush()
            lang = fence.group(2)
            body = []
            i += 1
            while i < len(items) and not FENCE_RE.match(items[i][1]):
                body.append(items[i][1])
                i += 1
            i += 1
            doc.parts.append(render_code(lang, body, where, rep))
            continue
        if not stripped:
            flush()
            i += 1
            continue
        heading = HEADING_RE.match(stripped)
        if heading:
            flush()
            level = len(heading.group(1))
            content = heading.group(2)
            if level == 1:
                rep.error(where, "no `#` heading in the body: the title is the H1")
                level = 2
            elif level > 4:
                rep.error(where, "headings go down to `####`")
                level = 4
            explicit = EXPLICIT_ID_RE.search(content)
            if explicit:
                content = content[:explicit.start()]
            plain = plain_inline(content)
            hid = doc.unique_id(explicit.group(1) if explicit else slugify(plain))
            inner = render_inline(content, where, rep)
            doc.headings.append((level, plain, inner, hid))
            doc.parts.append('<h%d id="%s">%s<a class="hash" href="#%s" aria-label="Link to %s">#</a></h%d>'
                             % (level, hid, inner, hid, attr(html.escape(plain, quote=False)), level))
            if level <= 3:
                doc.sections.append([plain, hid, []])
            else:
                doc.text(plain)
            i += 1
            continue
        if stripped.startswith("|") and i + 1 < len(items) and TABLE_SEP_RE.match(items[i + 1][1]):
            flush()
            head = split_cells(stripped)
            rows = []
            i += 2
            while i < len(items) and items[i][0] == "line" and items[i][1].strip().startswith("|"):
                rows.append((split_cells(items[i][1]), items[i][2]))
                i += 1
            out = ['<div class="tbl" role="region" tabindex="0" aria-label="%s"><table><thead><tr>'
                   % attr(html.escape("Table: " + ", ".join(plain_inline(c) for c in head), quote=False))]
            out += ["<th>%s</th>" % render_inline(c, where, rep) for c in head]
            out.append("</tr></thead><tbody>")
            for cells, rwhere in rows:
                if len(cells) != len(head):
                    rep.warn(rwhere, "table row has %d cells, the header %d" % (len(cells), len(head)))
                cells = (cells + [""] * len(head))[:max(len(head), 1)]
                out.append("<tr>%s</tr>" % "".join("<td>%s</td>" % render_inline(c, rwhere, rep)
                                                    for c in cells))
                doc.text(" · ".join(plain_inline(c) for c in cells))
            out.append("</tbody></table></div>")
            doc.parts.append("".join(out))
            continue
        if stripped.startswith(">"):
            flush()
            quote = []
            while i < len(items) and items[i][0] == "line" and items[i][1].strip().startswith(">"):
                quote.append(items[i][1].strip()[1:].strip())
                i += 1
            body = " ".join(q for q in quote if q)
            m = CALLOUT_RE.match(body)
            if m:
                label, rest = m.groups()
                doc.parts.append('<div class="callout callout-%s" role="note"><p><strong class="callout-label">'
                                 '%s</strong> %s</p></div>'
                                 % (label.lower(), label, render_inline(rest, where, rep)))
                doc.text("%s: %s" % (label, plain_inline(rest)))
            else:
                rep.warn(where, "a quote that is not a `> **Note**`, `> **Tip**` or `> **Warning**` callout")
                doc.parts.append("<blockquote><p>%s</p></blockquote>" % render_inline(body, where, rep))
                doc.text(plain_inline(body))
            continue
        image = IMAGE_LINE_RE.match(stripped)
        if image:
            flush()
            check_url(image.group(2), where, rep)
            doc.parts.append(figure_img(image.group(2), image.group(1), images))
            i += 1
            continue
        if LIST_RE.match(text):
            flush()
            i = render_list(items, i, doc, rep)
            continue
        para.append((text, where))
        i += 1
    flush()
    return doc


def render_list(items, i, doc, rep):
    """A list with at most one nested level (2-space indent). An item may carry an indented code
    fence or an indented paragraph after a blank line. Returns the next index."""
    top = None           # {"ordered": bool, "items": [item]}; item = [text, where, sub, blocks]

    def indent_of(text):
        return len(text) - len(text.lstrip())

    def last_item(text):
        item = top["items"][-1]
        if item[2] is not None and indent_of(text) >= 4:
            item = item[2]["items"][-1]
        return item

    while i < len(items):
        kind, text, where = items[i]
        if kind != "line":
            break
        m = LIST_RE.match(text)
        if not text.strip():
            # a blank line ends the list unless an item or an indented block follows
            j = i + 1
            while j < len(items) and items[j][0] == "line" and not items[j][1].strip():
                j += 1
            if j < len(items) and items[j][0] == "line" and (
                    LIST_RE.match(items[j][1]) or (top and indent_of(items[j][1]) >= 2)):
                if not LIST_RE.match(items[j][1]) and not FENCE_RE.match(items[j][1]):
                    last_item(items[j][1])[3].append(("para", [], items[j][2]))
                i = j
                continue
            break
        fence = FENCE_RE.match(text)
        if fence and top and indent_of(text) >= 2:
            pad = len(fence.group(1))
            body = []
            i += 1
            while i < len(items) and not FENCE_RE.match(items[i][1]):
                line = items[i][1]
                body.append(line[pad:] if line[:pad].strip() == "" else line.lstrip())
                i += 1
            if i >= len(items):
                rep.error(where, "a code fence is not closed")
            i += 1
            last_item(text)[3].append(("html", render_code(fence.group(2), body, where, rep), where))
            continue
        if m:
            indent, marker, body = len(m.group(1)), m.group(2), m.group(3)
            ordered = marker != "-"
            if indent < 2:
                if top is None:
                    top = {"ordered": ordered, "items": []}
                elif top["ordered"] != ordered:
                    break
                top["items"].append([body, where, None, []])
            else:
                if indent >= 4:
                    rep.error(where, "lists nest one level only")
                if top is None or not top["items"]:
                    rep.error(where, "a nested item without a parent")
                    top = top or {"ordered": ordered, "items": []}
                    top["items"].append([body, where, None, []])
                else:
                    parent = top["items"][-1]
                    if parent[2] is None:
                        parent[2] = {"ordered": ordered, "items": []}
                    parent[2]["items"].append([body, where, None, []])
            i += 1
            continue
        if HEADING_RE.match(text.strip()) or fence or text.strip().startswith(("|", ">")):
            break
        # a continuation line joins the item's text, or the paragraph opened after a blank line
        item = last_item(text)
        if item[3] and item[3][-1][0] == "para":
            item[3][-1][1].append(text.strip())
        else:
            item[0] += " " + text.strip()
        i += 1

    def emit(lst):
        tag = "ol" if lst["ordered"] else "ul"
        out = ["<%s>" % tag]
        for body, where, sub, blocks in lst["items"]:
            doc.text(plain_inline(body))
            extra = []
            for kind, value, bwhere in blocks:
                if kind == "html":
                    extra.append(value)
                elif value:
                    extra.append("<p>%s</p>" % render_inline(" ".join(value), bwhere, rep))
                    doc.text(plain_inline(" ".join(value)))
            first = render_inline(body, where, rep)
            if extra:
                first = "<p>%s</p>" % first
            out.append("<li>%s%s%s</li>" % (first, "".join(extra), emit(sub) if sub else ""))
        out.append("</%s>" % tag)
        return "".join(out)

    if top:
        doc.parts.append(emit(top))
    return i


# ----------------------------------------------------------------------------- templates

# The ncode mark: an open ring around rising bars, the middle one carrying a dot. The geometry is
# the desktop app's `logo_mark/1` (fitted by its make_icon.py); keep it in sync with that source.
MARK_PATHS = (
    '<g fill="none" stroke="currentColor" stroke-width="36" stroke-linecap="round">'
    '<path d="M313.1 41.3 A223.5 223.5 0 1 0 365.1 455.5"/><path d="M131.9 303.9 L124.5 353.9"/>'
    '<path d="M201.2 265.1 L182.0 393.9"/><path d="M276.8 218.5 L268.2 275.5"/>'
    '<path d="M254.9 367.5 L247.5 416.5"/><path d="M351.7 173.4 L317.3 404.2"/>'
    '<path d="M424.7 117.9 L387.3 367.7"/></g><circle cx="259.3" cy="319.4" r="22.5" fill="currentColor"/>'
)
MARK_SVG = '<svg class="mark" viewBox="-30 0 520 520" aria-hidden="true" focusable="false">%s</svg>' % MARK_PATHS
FONTS = ("https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@500;600;700"
         "&amp;family=Inter:wght@400;500;600&amp;display=swap")


def esc(text):
    return html.escape(text, quote=True)


def page_url(product, slug):
    return "/docs/%s/" % product if slug == "overview" else "/docs/%s/%s/" % (product, slug)


def url_to_path(url):
    return url.lstrip("/") + "index.html"


class Site:
    """What every template needs: names, asset stamps, the draft flag."""

    def __init__(self, names, stamp, draft):
        self.names = names
        self.stamp = stamp
        self.draft = draft

    def name(self, key, default=""):
        return self.names.get(key, default)


def head(site, title, description, url, kind="article"):
    robots = '<meta name="robots" content="noindex">\n' if site.draft else ""
    return (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>%(title)s</title>\n<meta name=\"description\" content=\"%(desc)s\">\n%(robots)s"
        '<link rel="canonical" href="%(site)s%(url)s">\n'
        '<meta property="og:type" content="%(kind)s">\n<meta property="og:site_name" content="ncode">\n'
        '<meta property="og:title" content="%(title)s">\n<meta property="og:description" content="%(desc)s">\n'
        '<meta property="og:url" content="%(site)s%(url)s">\n<meta name="theme-color" content="#0a0a0f">\n'
        '<link rel="icon" href="/favicon.ico" sizes="any">\n'
        '<link rel="icon" type="image/svg+xml" href="%(icon)s">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="%(fonts)s">\n<link rel="stylesheet" href="%(css)s">\n'
        '<script src="%(js)s" defer></script>\n</head>\n'
    ) % {
        "title": esc(title), "desc": esc(description), "robots": robots, "site": SITE_URL, "url": url,
        "kind": kind, "icon": site.stamp("assets/brand/ncode-icon.svg"), "fonts": FONTS,
        "css": site.stamp("assets/docs.css"), "js": site.stamp("assets/docs.js"),
    }


def topbar(site, product=None):
    switch = "".join(
        '<a href="/docs/%s/"%s>%s</a>' % (p, ' aria-current="true"' if p == product else "", PRODUCT_NAMES[p])
        for p in PRODUCTS)
    search = ""
    if product:
        search = (
            '<div class="d-search" data-search="/docs/%(p)s/search.json" hidden>'
            '<label class="sr" for="d-q">Search the %(n)s docs</label>'
            '<input id="d-q" type="search" placeholder="Search %(n)s docs" autocomplete="off" '
            'spellcheck="false" aria-controls="d-hits">'
            '<kbd class="d-slash" aria-hidden="true">/</kbd>'
            '<div class="d-hits" id="d-hits" hidden><ul></ul></div></div>'
            '<p class="sr" id="d-count" aria-live="polite"></p>'
        ) % {"p": product, "n": PRODUCT_NAMES[product]}
    return (
        '<a class="skip" href="#main">Skip to content</a>\n'
        '<header class="d-top">'
        '<a class="d-brand" href="/" aria-label="ncode home">%s<span class="d-word">ncode</span></a>'
        '<span class="d-docs" aria-hidden="true">docs</span>'
        '<nav class="d-switch" aria-label="Documentation set">%s</nav>%s'
        '<nav class="d-links" aria-label="Site"><a href="/docs/">All docs</a>'
        '<a href="/releases/">Releases</a><a href="/#download">Download</a></nav>'
        "</header>\n"
    ) % (MARK_SVG, switch, search)


def footer(site, notes=()):
    extra = "".join('<p class="d-gen">%s</p>' % n for n in notes)
    return (
        '<footer class="d-foot"><div class="d-foot-in">'
        '<p><a class="d-foot-brand" href="/">%s<span>ncode</span></a> %s · developer preview</p>'
        '<p class="d-foot-links"><a href="/docs/">Docs</a><a href="/releases/">Releases</a>'
        '<a href="%s">CLI source</a><a href="https://llmotions.com/">LLMotions</a></p>%s'
        "</div></footer>\n"
    ) % (MARK_SVG, esc(site.name("version")), esc(site.name("cli_repo", "https://github.com/")), extra)


def sidebar(product, groups, current):
    out = []
    for group, entries in groups:
        links = "".join(
            '<li><a href="%s"%s>%s</a></li>'
            % (page_url(product, slug), ' aria-current="page"' if slug == current else "", esc(title))
            for slug, title, _ in entries)
        if group:
            out.append('<div class="d-group"><p class="d-group-h">%s</p><ul aria-label="%s">%s</ul></div>'
                       % (esc(group), esc(group), links))
        else:
            out.append('<div class="d-group"><ul>%s</ul></div>' % links)
    return "".join(out)


def toc(headings):
    items = [(lvl, inner, hid) for lvl, _, inner, hid in headings if lvl in (2, 3)]
    if not items:
        return ""
    out, open_sub = [], False
    for n, (lvl, inner, hid) in enumerate(items):
        link = '<a href="#%s">%s</a>' % (hid, re.sub(r"</?a\b[^>]*>", "", inner))
        if lvl == 2:
            if open_sub:
                out.append("</ul></li>")
                open_sub = False
            elif n:
                out.append("</li>")
            out.append("<li>" + link)
        else:
            if not open_sub:
                if not out:
                    out.append("<li>")
                out.append("<ul>")
                open_sub = True
            out.append("<li>%s</li>" % link)
    out.append("</ul></li>" if open_sub else "</li>")
    return ('<aside class="d-toc" aria-labelledby="d-toc-h"><p id="d-toc-h">On this page</p>'
            '<ul>%s</ul></aside>' % "".join(out))


def render_page(site, product, groups, page, prev, nxt):
    notes = []
    for name, ref in sorted(page["imports"].items()):
        what = "keyboard reference" if name == "keybindings" else "settings reference"
        notes.append("The %s on this page is generated from the ncode CLI at <code>%s</code>."
                     % (what, esc(ref or "an unrecorded commit")))
    side = sidebar(product, groups, page["slug"])
    pager = []
    if prev:
        pager.append('<a class="d-prev" rel="prev" href="%s"><span>Previous</span>%s</a>'
                     % (page_url(product, prev["slug"]), esc(prev["nav_title"])))
    if nxt:
        pager.append('<a class="d-next" rel="next" href="%s"><span>Next</span>%s</a>'
                     % (page_url(product, nxt["slug"]), esc(nxt["nav_title"])))
    crumb = '<a href="/docs/%s/">ncode %s</a>' % (product, PRODUCT_NAMES[product])
    if page["group"]:
        crumb += ' <span aria-hidden="true">/</span> %s' % esc(page["group"])
    title = "%s · ncode %s docs" % (page["title"], PRODUCT_NAMES[product])
    if page["slug"] == "overview":
        title = "ncode %s docs" % PRODUCT_NAMES[product]
    return "".join([
        head(site, title, page["description"], page["url"]),
        '<body class="d" data-product="%s">\n' % product,
        topbar(site, product),
        '<div class="d-shell">',
        '<nav class="d-side" aria-label="%s docs">%s</nav>' % (PRODUCT_NAMES[product], side),
        '<details class="d-menu"><summary>%s docs <span>%s</span></summary>'
        '<nav aria-label="%s docs, menu">%s</nav></details>'
        % (PRODUCT_NAMES[product], esc(page["nav_title"]), PRODUCT_NAMES[product], side),
        '<main id="main" class="d-main" tabindex="-1"><article class="d-article">',
        '<p class="d-crumb">%s</p>' % crumb,
        "<h1>%s</h1>\n" % esc(page["title"]),
        "\n".join(page["doc"].parts),
        '\n<nav class="d-pager" aria-label="Previous and next page">%s</nav>' % "".join(pager) if pager else "",
        "</article></main>",
        toc(page["doc"].headings),
        "</div>\n",
        footer(site, notes),
        "</body>\n</html>\n",
    ])


def render_hub(site, sets):
    cards = []
    for product in PRODUCTS:
        groups, pages = sets.get(product, ([], []))
        lists = []
        for group, entries in groups:
            lists.append('<div class="hub-group"><h3>%s</h3><ul>%s</ul></div>' % (
                esc(group or PRODUCT_NAMES[product]),
                "".join('<li><a href="%s">%s</a></li>' % (page_url(product, s), esc(t)) for s, t, _ in entries)))
        body = "".join(lists) if lists else '<p class="hub-empty">This guide is being written.</p>'
        cards.append(
            '<section class="hub-card hub-%(p)s" aria-labelledby="hub-%(p)s">'
            '<h2 id="hub-%(p)s"><a href="/docs/%(p)s/">ncode %(n)s</a></h2><p class="hub-lede">%(lede)s</p>'
            '<p class="hub-count">%(count)d pages</p>%(body)s</section>'
            % {"p": product, "n": PRODUCT_NAMES[product], "lede": esc(PRODUCT_LEDES[product]),
               "count": len(pages), "body": body})
    return "".join([
        head(site, "ncode docs", "The ncode documentation: the desktop app and the CLI, each with its own "
                                 "complete guide.", "/docs/", kind="website"),
        '<body class="d d-hubpage">\n', topbar(site),
        '<main id="main" class="d-hub" tabindex="-1"><header class="hub-head">'
        '<p class="hub-eyebrow">Documentation</p><h1>Two faces, one engine</h1>'
        '<p>The desktop app and the CLI run the same engine on the same local database. Each has its own '
        'complete guide: pick the one you use.</p></header>'
        '<div class="hub-grid">%s</div></main>\n' % "".join(cards),
        footer(site), "</body>\n</html>\n",
    ])


def render_releases(site, doc):
    return "".join([
        head(site, "ncode releases", "Every ncode release, newest first, with the SHA-256 of each download.",
             "/releases/", kind="website"),
        '<body class="d d-relpage">\n', topbar(site),
        '<div class="d-shell d-shell-wide"><main id="main" class="d-main" tabindex="-1">'
        '<article class="d-article"><p class="d-crumb"><a href="/docs/">ncode</a></p><h1>Releases</h1>\n',
        "\n".join(doc.parts), "</article></main>", toc(doc.headings), "</div>\n",
        footer(site), "</body>\n</html>\n",
    ])


def search_index(product, pages):
    out = []
    for page in pages:
        sections = []
        for heading, anchor, chunks in page["doc"].sections:
            text = " ".join(chunks)
            snippet = text[:200].rsplit(" ", 1)[0] + "…" if len(text) > 200 else text
            if heading or snippet:
                sections.append([heading, anchor, snippet])
        out.append({"t": page["title"], "u": page["url"], "g": page["group"], "d": page["description"],
                    "s": sections})
    return json.dumps({"product": product, "pages": out}, ensure_ascii=False, separators=(",", ":")) + "\n"


def sitemap(urls):
    body = "".join("  <url><loc>%s%s</loc></url>\n" % (SITE_URL, esc(u)) for u in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % body)


ROBOTS = "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE_URL


# ----------------------------------------------------------------------------- output checks

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class PageScan(HTMLParser):
    """Collects ids and root-absolute references, and checks that tags nest."""

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.ids = set()
        self.dup_ids = set()
        self.refs = []
        self.stack = []
        self.problems = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:
                self.dup_ids.add(a["id"])
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if a.get(key) is not None and tag in ("a", "link", "script", "img", "source"):
                self.refs.append((tag, a[key], self.getpos()[0]))
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        if tag in VOID or any(t == "svg" for t, _ in self.stack):
            # void elements, and self-closing elements inside inline SVG (foreign content)
            self.handle_starttag(tag, attrs)
            if tag not in VOID:
                self.stack.pop()
        else:
            self.problems.append("line %d: <%s/> is not a void element" % (self.getpos()[0], tag))

    def handle_endtag(self, tag):
        if tag in VOID:
            self.problems.append("line %d: </%s> closes a void element" % (self.getpos()[0], tag))
            return
        if not self.stack:
            self.problems.append("line %d: </%s> without an open tag" % (self.getpos()[0], tag))
            return
        open_tag, line = self.stack.pop()
        if open_tag != tag:
            self.problems.append("line %d: </%s> closes <%s> from line %d"
                                 % (self.getpos()[0], tag, open_tag, line))

    def finish(self):
        self.close()
        for tag, line in self.stack:
            self.problems.append("line %d: <%s> is never closed" % (line, tag))
        return self


def scan_html(text):
    scan = PageScan()
    scan.feed(text)
    return scan.finish()


def path_to_url(relpath):
    if relpath == "index.html":
        return "/"
    if relpath.endswith("/index.html"):
        return "/" + relpath[:-len("index.html")]
    return "/" + relpath


def check_output(files, handwritten, rep, origin):
    """Link, anchor and well-formedness check over every HTML page of the site.

    files: generated {relpath: bytes}; handwritten: {relpath: bytes} of the site's own files;
    origin: relpath -> the source label to name in messages."""
    everything = dict(handwritten)
    everything.update(files)
    scans = {}
    for relpath, data in sorted(everything.items()):
        if relpath.endswith(".html"):
            scan = scan_html(data.decode("utf-8"))
            scans[relpath] = scan
            label = origin.get(relpath, "code/" + relpath)
            for problem in scan.problems:
                rep.error(label, "not well-formed: " + problem)
            for dup in sorted(scan.dup_ids):
                rep.error(label, "duplicate id %r" % dup)
    for relpath, scan in sorted(scans.items()):
        label = origin.get(relpath, "code/" + relpath)
        for tag, ref, line in scan.refs:
            if ref.startswith(("https://", "http://", "mailto:")):
                continue
            if ref.startswith("#"):
                if ref[1:] and ref[1:] not in scan.ids:
                    rep.error(label, "anchor %r is not on this page" % ref)
                continue
            if not ref.startswith("/") or ref.startswith("//"):
                rep.error(label, "link %r is not root-absolute" % ref)
                continue
            path, _, frag = ref.partition("#")
            path = path.split("?", 1)[0]
            if path.startswith(UNBUILT_PREFIXES):
                continue
            if path == "/install.sh":
                continue      # lane F's stamped installer; check_release looks at it
            target = path.lstrip("/")
            if path.endswith("/"):
                target += "index.html"
            elif target not in everything and (target + "/index.html") in everything:
                rep.error(label, "link %r needs its trailing slash" % ref)
                continue
            if target not in everything:
                rep.error(label, "broken link %r (line %d of the output)" % (ref, line))
                continue
            if frag and target in scans and frag not in scans[target].ids:
                rep.error(label, "broken anchor %r: no id %r on %s" % (ref, frag, path_to_url(target)))


def newest_release(text):
    """The first `## ` entry of releases.md -> dict(version, cli, desktop, date)."""
    info = {"version": None, "date": None, "cli": None, "desktop": None}
    seen = False
    for line in text.split("\n"):
        if line.startswith("## "):
            if seen:
                break
            seen = True
            m = re.search(r"(\d+\.\d+\.\d+)", line)
            info["version"] = m.group(1) if m else None
            d = re.search(r"(\d{4}-\d{2}-[0-9X]{2})", line)
            info["date"] = d.group(1) if d else None
            continue
        m = re.match(r"^-\s*(cli|desktop):\s*(\S+)\s+sha256\s+(\S+)\s*$", line.strip())
        if seen and m:
            info[m.group(1)] = (m.group(2), m.group(3))
    return info


def check_release(content, site, rep, release):
    path = content / "releases.md"
    if not path.is_file():
        rep.error(rel(path, ROOT), "releases.md is missing")
        return
    text = path.read_text(encoding="utf-8")
    report = rep.error if release else rep.warn
    for n, line in enumerate(text.split("\n"), 1):
        if re.search(r"\bTBD\b", line):
            report("%s:%d" % (rel(path, ROOT), n), "TBD left in releases.md")
        if re.match(r"^## .*\d{4}-\d{2}-XX", line):
            report("%s:%d" % (rel(path, ROOT), n), "release date not set")
        if line.strip() == "Notes as a list.":
            report("%s:%d" % (rel(path, ROOT), n), "release notes not written yet")
    for page in sorted(site.glob("*.html")) if site.is_dir() else []:
        for n, line in enumerate(page.read_text(encoding="utf-8").split("\n"), 1):
            if re.search(r"\bTBD\b", line):
                report("%s:%d" % (rel(page, ROOT), n), "TBD left in a hand-written page")
    info = newest_release(text)
    check_landing(content, site, info, report)
    install = site / "install.sh"
    if not install.is_file():
        # the contract's phase-1 warning; a release without the installer is not a release
        report(rel(install, ROOT), "missing (lane F copies the stamped installer here)")
        return
    script = install.read_text(encoding="utf-8", errors="replace")
    ver = re.search(r'VERSION="\$\{NCODE_VERSION:-([^}"]*)\}"', script)
    sha = re.search(r'(?m)^\s*SHA256="([^"]*)"', script)
    ver = ver.group(1) if ver else None
    sha = sha.group(1) if sha else None
    cli_sha = info["cli"][1] if info["cli"] else None
    if ver != info["version"] or sha != cli_sha or not sha or not re.match(r"^[0-9a-f]{64}$", sha or ""):
        report(rel(install, ROOT), "stamps VERSION=%r SHA256=%r do not match the newest release %r / %r"
               % (ver, sha, info["version"], cli_sha))


LANDING_VERSION_RE = re.compile(r"(?:\bncode[- ]|\b[Vv]ersion )(\d+\.\d+\.\d+)")
DMG_SHA_RE = re.compile(r'id="dmg-sha"[^>]*>([^<]*)<')


def check_landing(content, site, info, report):
    """The landing's download facts follow the newest releases.md entry and names.json (K14 for
    the DMG): the SHA-256 in <code id="dmg-sha">, the /downloads/<dmg> link and every
    "ncode X.Y.Z" / "Version X.Y.Z" / "ncode-X.Y.Z.dmg". `report` warns, or fails under --release."""
    page = site / "index.html"
    if not page.is_file():
        return
    label = rel(page, ROOT)
    text = page.read_text(encoding="utf-8")
    version = info["version"]
    dmg, dmg_sha = info["desktop"] or (None, None)
    names_label = rel(content / "names.json", ROOT)
    names = load_names(content, Report())       # build() already reported a broken names.json
    if dmg is None:
        report(rel(content / "releases.md", ROOT), "the newest release has no `- desktop:` line")
    elif names.get("dmg") != dmg:
        report(names_label, "dmg %r differs from the newest release's %r" % (names.get("dmg"), dmg))
    if names.get("version") != version:
        report(names_label, "version %r differs from the newest release's %r" % (names.get("version"), version))
    shown = DMG_SHA_RE.search(text)
    if not shown:
        report(label, 'no <code id="dmg-sha"> showing the DMG\'s SHA-256')
    elif shown.group(1).strip() != dmg_sha or not re.match(r"^[0-9a-f]{64}$", shown.group(1).strip()):
        report(label, "DMG SHA-256 %r does not match the newest release's %r" % (shown.group(1).strip(), dmg_sha))
    if dmg and ('href="/downloads/%s"' % dmg) not in text:
        report(label, "no download link to /downloads/%s" % dmg)
    for n, line in enumerate(text.split("\n"), 1):
        for found in LANDING_VERSION_RE.findall(line):
            if found != version:
                report("%s:%d" % (label, n), "version %s is not the newest release %s" % (found, version))


# ----------------------------------------------------------------------------- build

def sha8(data):
    return hashlib.sha1(data).hexdigest()[:8]


OWN_BRAND = ("ncode-icon.svg", "ncode-mark.svg")   # hand-written; the rest of assets/brand/ is copied


def generated_copy(relpath):
    """assets/llm.css and assets/brand/* (except OWN_BRAND) are copies of llmotions.com's assets."""
    if relpath == "assets/llm.css":
        return True
    return relpath.startswith("assets/brand/") and relpath[len("assets/brand/"):] not in OWN_BRAND


def stale_copies(files, out):
    """Copied apex assets under `out` that the apex no longer has."""
    found = [out / "assets" / "llm.css"]
    brand = out / "assets" / "brand"
    found += sorted(brand.rglob("*")) if brand.is_dir() else []
    return [p for p in found if p.is_file() and p.name != ".DS_Store"
            and generated_copy(p.relative_to(out).as_posix())
            and p.relative_to(out).as_posix() not in files]


def handwritten_files(site):
    """The site's own files: everything under code/ outside the generated folders, the copied
    apex assets and the uploads."""
    out = {}
    if not site.is_dir():
        return out
    for path in sorted(site.rglob("*")):
        if not path.is_file() or path.name == ".DS_Store":
            continue
        relpath = path.relative_to(site).as_posix()
        if relpath.split("/", 1)[0] in ("docs", "releases", "downloads") or generated_copy(relpath):
            continue
        out[relpath] = path.read_bytes()
    return out


STAMP_RE = re.compile(r'(["\'(])(/assets/[A-Za-z0-9_./-]+)\?v=[A-Za-z0-9]+')


def build(content, site, assets_src, draft, rep):
    """Everything the generator owns, as {relpath: bytes}, plus origins for messages. Writes nothing."""
    files, origin = {}, {}
    names = load_names(content, rep)
    hand = handwritten_files(site)
    # assets shared with llmotions.com, copied so the subdomain deploys on its own
    llm = assets_src / "llm.css"
    if llm.is_file():
        files["assets/llm.css"] = llm.read_bytes()
    else:
        rep.error(rel(llm, ROOT), "missing")
    brand = assets_src / "brand"
    for path in sorted(brand.iterdir()) if brand.is_dir() else []:
        if path.is_file() and not path.name.startswith("."):
            files["assets/brand/" + path.name] = path.read_bytes()

    def stamp(relpath):
        data = files.get(relpath, hand.get(relpath))
        if data is None:
            rep.error("code/" + relpath, "asset is missing")
            return "/" + relpath
        return "/%s?v=%s" % (relpath, sha8(data))

    site_ctx = Site(names, stamp, draft)

    def images(url):
        path = url.split("#", 1)[0].split("?", 1)[0]
        data = files.get(path.lstrip("/"), hand.get(path.lstrip("/"))) if path.startswith("/") else None
        return image_size(data) if data else None

    cache = {}
    sets = {}
    all_pages = []
    release_placeholders = []
    for product in PRODUCTS:
        pdir = content / "docs" / product
        if not pdir.is_dir():
            rep.warn(rel(pdir, ROOT), "no %s docs yet" % product)
            continue
        navfile = pdir / "_nav.txt"
        if not navfile.is_file():
            rep.error(rel(navfile, ROOT), "missing")
            continue
        groups = parse_nav(navfile, rep)
        entries = [(g, s, t) for g, items in groups for s, t, _ in items]
        on_disk = sorted(p.stem for p in pdir.glob("*.md"))
        listed = [s for _, s, _ in entries]
        for slug in on_disk:
            if slug not in listed:
                rep.error(rel(pdir / (slug + ".md"), ROOT), "page is not in _nav.txt")
        for slug in listed:
            if slug not in on_disk:
                rep.error(rel(navfile, ROOT), "entry %r has no page" % slug)
        if "overview" not in listed:
            rep.error(rel(navfile, ROOT), "needs an `overview` page (it is /docs/%s/)" % product)
        pages = []
        for group, slug, nav_title in entries:
            path = pdir / (slug + ".md")
            if not path.is_file():
                continue
            label = rel(path, ROOT)
            text = path.read_text(encoding="utf-8")
            if not SOURCE_RE.search(text):
                rep.error(label, "no `<!-- source: … -->` comment")
            denylist_scan(label, text.split("\n"), 1, rep, allow_ok=False)
            meta, body, first = split_front_matter(text, label, rep)
            src = expand(body, label, first, content, cache, rep)
            doc = render_markdown(preprocess(src, names, rep), rep, draft, images=images)
            title = substitute_names(meta.get("title", slug), names, label, rep)
            description = substitute_names(meta.get("description", ""), names, label, rep)
            if len(description) > 160:
                rep.error(label, "description is %d characters (at most 160)" % len(description))
            pages.append({"slug": slug, "nav_title": substitute_names(nav_title, names, label, rep),
                          "group": group, "title": title, "description": description, "doc": doc,
                          "url": page_url(product, slug), "imports": src.imports, "label": label})
        for n, page in enumerate(pages):
            prev = pages[n - 1] if n else None
            nxt = pages[n + 1] if n + 1 < len(pages) else None
            relpath = url_to_path(page["url"])
            files[relpath] = render_page(site_ctx, product, groups, page, prev, nxt).encode("utf-8")
            origin[relpath] = page["label"]
        files["docs/%s/search.json" % product] = search_index(product, pages).encode("utf-8")
        sets[product] = (groups, pages)
        all_pages += pages
    # every partial on disk is scanned, included or not (the repo is public); the cache makes
    # this a no-op for the ones a page already included. Outside the fixed set: a warning.
    shared = content / "docs" / "shared"
    for path in sorted(shared.glob("*.md")) if shared.is_dir() else []:
        if path.stem not in SHARED_PARTIALS:
            rep.warn(rel(path, ROOT), "not in the fixed partial set")
        read_partial(content, "shared", path.stem, cache, rep)
    imports = content / "import"
    for path in sorted(imports.glob("*.md")) if imports.is_dir() else []:
        read_partial(content, "import", path.stem, cache, rep)
    files["docs/index.html"] = render_hub(site_ctx, sets).encode("utf-8")
    origin["docs/index.html"] = "the /docs/ hub (tools/build_ncode.py)"
    releases = content / "releases.md"
    if releases.is_file():
        label = rel(releases, ROOT)
        lines = releases.read_text(encoding="utf-8").split("\n")
        denylist_scan(label, lines, 1, rep, allow_ok=False)
        src = Source()
        src.extend(lines, label, 1)
        doc = render_markdown(preprocess(src, names, rep), rep, draft)
        files["releases/index.html"] = render_releases(site_ctx, doc).encode("utf-8")
        origin["releases/index.html"] = label
        release_placeholders = list(doc.placeholders)
    else:
        rep.error(rel(releases, ROOT), "missing")
    urls = ["/", "/docs/", "/releases/"] + [p["url"] for p in all_pages]
    files["sitemap.xml"] = sitemap(urls).encode("utf-8")
    files["robots.txt"] = ROBOTS.encode("utf-8")
    # hand-written pages carry ?v= stamps of the assets they load; keep them current
    for relpath, data in sorted(hand.items()):
        if relpath.endswith(".html") and "/" not in relpath:
            text = data.decode("utf-8")
            fresh = STAMP_RE.sub(lambda m: m.group(1) + stamp(m.group(2)[1:]), text)
            if fresh != text:
                files[relpath] = fresh.encode("utf-8")
            origin.setdefault(relpath, "code/" + relpath)
    placeholders = [ph for p in all_pages for ph in p["doc"].placeholders] + release_placeholders
    return files, origin, hand, placeholders


def drift(files, out, rep):
    for relpath, data in sorted(files.items()):
        path = out / relpath
        if not path.is_file() or path.read_bytes() != data:
            rep.error("code/" + relpath, "differs from a fresh build (run tools/build_ncode.py and commit)")
    for top in ("docs", "releases"):
        base = out / top
        for path in sorted(base.rglob("*")) if base.is_dir() else []:
            relpath = path.relative_to(out).as_posix()
            if path.is_file() and path.name != ".DS_Store" and relpath not in files:
                rep.error("code/" + relpath, "stale: no source builds it")
    for path in stale_copies(files, out):
        rep.error("code/" + path.relative_to(out).as_posix(), "stale: a copy of an apex asset that is gone")


def write(files, hand, out, site):
    out.mkdir(parents=True, exist_ok=True)
    if out.resolve() != site.resolve():
        for relpath, data in hand.items():
            target = out / relpath
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    for top in ("docs", "releases"):
        base = out / top
        for path in sorted(base.rglob("*"), reverse=True) if base.is_dir() else []:
            relpath = path.relative_to(out).as_posix()
            if path.is_file() and relpath not in files:
                path.unlink()
            elif path.is_dir() and not any(path.iterdir()):
                path.rmdir()
    for path in stale_copies(files, out):
        path.unlink()
    written = 0
    for relpath, data in sorted(files.items()):
        target = out / relpath
        if target.is_file() and target.read_bytes() == data:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        written += 1
    return written


# ----------------------------------------------------------------------------- import

def import_cli(cli, ref, content, rep):
    """Copies the CLI's two generated references into content/ncode/import/ as partials."""
    if not re.match(r"^[0-9a-f]{7,40}$", ref):
        rep.error("--ref", "expected a commit sha (7-40 hex characters)")
        return
    target = content / "import"
    target.mkdir(parents=True, exist_ok=True)
    is_git = (cli / ".git").exists()
    if not is_git:
        rep.warn(str(cli), "not a git checkout: files are read from the working tree; ref recorded as given")
    for name in IMPORT_PARTIALS:
        src_rel = IMPORT_SOURCES[name]
        if is_git:
            proc = subprocess.run(["git", "-C", str(cli), "show", "%s:%s" % (ref, src_rel)],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if proc.returncode:
                rep.error(src_rel, "git show %s:%s failed: %s"
                          % (ref, src_rel, proc.stderr.decode("utf-8", "replace").strip()))
                continue
            text = proc.stdout.decode("utf-8")
        else:
            path = cli / src_rel
            if not path.is_file():
                rep.error(str(path), "missing")
                continue
            text = path.read_text(encoding="utf-8")
        body = convert_reference(text)
        header = ("<!-- generated by tools/build_ncode.py --import-cli from C:%s at %s; never edit by hand -->\n"
                  "<!-- source: C:%s -->\n<!-- import-ref: %s -->\n\n" % (src_rel, ref, src_rel, ref))
        out = target / (name + ".md")
        out.write_text(header + body, encoding="utf-8")
        before = len(rep.errors)
        denylist_scan(rel(out, ROOT), (header + body).split("\n"), 1, rep, allow_ok=False)
        hits = len(rep.errors) - before
        if hits:
            # a generated file is fixed at its source, so hits are reported, not fatal here
            rep.warnings += ["%s (report to lane A)" % e for e in rep.errors[before:]]
            del rep.errors[before:]
        print("imported %s -> %s" % (src_rel, rel(out, ROOT)))


PROJECT_DIR_RE = re.compile(r"(?<![\w~/.])\.swarm_code(?!\w|\.\w)")


def convert_reference(text):
    """A CLI reference page -> a partial: no H1, no "Generated by" note, headings one level down
    (a later H1 -> `###`), `{{` kept literal, `.swarm_code` -> `{{project_dir}}`."""
    lines = text.replace("\r\n", "\n").split("\n")
    out = []
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].startswith("# "):
        i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].startswith("Generated by"):
        while i < len(lines) and lines[i].strip():
            i += 1
    in_fence = False
    for line in lines[i:]:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence:
            m = re.match(r"^(#{1,6})\s", line)
            if m:
                # a later H1 (the reference's second part) sits beside the demoted `##` sections
                level = 3 if len(m.group(1)) == 1 else min(len(m.group(1)) + 1, 4)
                line = "#" * level + line[len(m.group(1)):]
        # the project folder keeps its old name (owner decision); the reference names it through
        # {{project_dir}} so the source denylist stays exact and the output is unchanged
        out.append(PROJECT_DIR_RE.sub("{{project_dir}}", line.replace("{{", "\\{{")))
    while out and not out[0].strip():
        out.pop(0)
    return "\n".join(out).rstrip("\n") + "\n"


# ----------------------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(description="Build the ncode site (code.llmotions.com).")
    ap.add_argument("--content", type=Path, default=ROOT / "content" / "ncode")
    ap.add_argument("--site", type=Path, default=ROOT / "code",
                    help="the site folder holding the hand-written pages (default code/)")
    ap.add_argument("--out", type=Path, help="where to write (default: the site folder)")
    ap.add_argument("--assets", type=Path, default=ROOT / "assets", help="llmotions.com assets to copy")
    ap.add_argument("--draft", action="store_true", help="draw placeholders; never commit a draft build")
    ap.add_argument("--check", action="store_true", help="validate without writing")
    ap.add_argument("--release", action="store_true", help="with --check: fail on anything unfinished")
    ap.add_argument("--no-drift", action="store_true", help="with --check: skip the committed-output comparison")
    ap.add_argument("--import-cli", type=Path, metavar="PATH")
    ap.add_argument("--ref", metavar="SHA")
    args = ap.parse_args(argv)
    rep = Report()
    if args.release and not args.check:
        ap.error("--release needs --check")
    if args.no_drift and not args.check:
        ap.error("--no-drift needs --check")
    if args.check and args.draft:
        ap.error("--check validates the normal build; drop --draft")
    if bool(args.import_cli) != bool(args.ref):
        ap.error("--import-cli and --ref go together")
    if args.import_cli:
        import_cli(args.import_cli, args.ref, args.content, rep)
        return finish(rep)
    out = args.out or args.site
    files, origin, hand, placeholders = build(args.content, args.site, args.assets, args.draft, rep)
    if args.check:
        check_output(files, hand, rep, origin)
        for kind, payload, where in placeholders:
            (rep.error if args.release else rep.warn)(where, "%s placeholder left: %s" % (kind, payload))
        check_release(args.content, args.site, rep, args.release)
        if not args.no_drift:
            drift(files, out, rep)
        status = finish(rep)
        if not status:
            print("check passed: %d generated files" % len(files))
        return status
    if rep.errors:
        return finish(rep)
    written = write(files, hand, out, args.site)
    print("built %d files (%d changed) into %s" % (len(files), written, out))
    return finish(rep)


def finish(rep):
    for w in rep.warnings:
        print("warning: " + w, file=sys.stderr)
    for e in rep.errors:
        print("error: " + e, file=sys.stderr)
    if rep.errors:
        print("%d error(s), %d warning(s)" % (len(rep.errors), len(rep.warnings)), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
