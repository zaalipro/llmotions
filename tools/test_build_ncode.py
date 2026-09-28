"""Tests for tools/build_ncode.py.

    python3 -m unittest tools/test_build_ncode.py
    UPDATE_GOLDEN=1 python3 -m unittest tools/test_build_ncode.py    rewrite the golden page

The fixtures live in tools/testdata: content/ (pages, partials, imports, names, releases),
site/ (a stand-in hand-written landing), assets/ (a stand-in llmotions.com asset folder),
cli/ (a stand-in CLI checkout for --import-cli) and golden/.
"""
import io
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_ncode as B  # noqa: E402

FX = HERE / "testdata"
GOLDEN = FX / "golden" / "cli-install.html"


class Tree:
    """A private copy of the fixture tree, with files replaced or removed."""

    def __init__(self, tc, overrides=None, remove=()):
        tmp = tempfile.TemporaryDirectory()
        tc.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        for name in ("content", "site", "assets"):
            shutil.copytree(str(FX / name), str(self.root / name))
        for relpath, text in (overrides or {}).items():
            path = self.root / relpath
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        for relpath in remove:
            (self.root / relpath).unlink()
        self.content = self.root / "content"
        self.site = self.root / "site"
        self.assets = self.root / "assets"

    def run(self, *args):
        err, out = io.StringIO(), io.StringIO()
        with redirect_stderr(err), redirect_stdout(out):
            code = B.main(["--content", str(self.content), "--site", str(self.site),
                           "--assets", str(self.assets)] + list(args))
        return code, err.getvalue() + out.getvalue()

    def build(self, draft=False):
        rep = B.Report()
        files, origin, hand, placeholders = B.build(self.content, self.site, self.assets, draft, rep)
        return files, rep, placeholders

    def check(self):
        """Build + the output checker, as --check --no-drift does."""
        rep = B.Report()
        files, origin, hand, _ = B.build(self.content, self.site, self.assets, False, rep)
        B.check_output(files, hand, rep, origin)
        return rep


def page(title, body, source=True):
    text = "---\ntitle: %s\ndescription: A test page.\n---\n\n%s\n" % (title, body)
    if source:
        text += "\n<!-- source: D:README.md:1 -->\n"
    return text


def errors_of(rep, needle):
    return [e for e in rep.errors if needle in e]


class GoldenPage(unittest.TestCase):
    def test_cli_install_page_matches_the_golden_file(self):
        rep = B.Report()
        files, _, _, _ = B.build(FX / "content", FX / "site", FX / "assets", False, rep)
        self.assertEqual(rep.errors, [])
        got = files["docs/cli/install/index.html"].decode("utf-8")
        if os.environ.get("UPDATE_GOLDEN"):
            GOLDEN.write_text(got, encoding="utf-8")
        self.assertEqual(got, GOLDEN.read_text(encoding="utf-8"))

    def test_the_fixture_passes_check_without_drift(self):
        code, out = Tree(self).run("--check", "--no-drift")
        self.assertEqual(code, 0, out)
        self.assertIn("check passed", out)

    def test_build_writes_and_a_second_check_sees_no_drift(self):
        tree = Tree(self)
        out = tree.root / "out"
        code, log = tree.run("--out", str(out))
        self.assertEqual(code, 0, log)
        self.assertTrue((out / "docs/cli/install/index.html").is_file())
        self.assertTrue((out / "index.html").is_file(), "hand-written pages are copied to --out")
        code, log = tree.run("--out", str(out), "--check")
        self.assertEqual(code, 0, log)
        (out / "docs/cli/index.html").write_text("changed", encoding="utf-8")
        (out / "docs/cli/old").mkdir()
        (out / "docs/cli/old/index.html").write_text("stale", encoding="utf-8")
        code, log = tree.run("--out", str(out), "--check")
        self.assertEqual(code, 1)
        self.assertIn("differs from a fresh build", log)
        self.assertIn("stale", log)
        tree.run("--out", str(out))
        self.assertFalse((out / "docs/cli/old").exists(), "a rebuild removes stale pages")


class Links(unittest.TestCase):
    def test_broken_internal_link(self):
        tree = Tree(self, {"content/docs/cli/overview.md": page("O", "See [x](/docs/cli/nope/).")})
        self.assertTrue(errors_of(tree.check(), "broken link '/docs/cli/nope/'"))

    def test_broken_anchor(self):
        tree = Tree(self, {"content/docs/cli/overview.md": page("O", "See [x](/docs/cli/install/#nope).")})
        self.assertTrue(errors_of(tree.check(), "broken anchor '/docs/cli/install/#nope'"))

    def test_good_anchor_and_cross_product_link(self):
        body = "See [a](/docs/cli/install/#uninstall-2) and [b](/docs/desktop/install/#first-launch)."
        tree = Tree(self, {"content/docs/cli/overview.md": page("O", body)})
        self.assertEqual(tree.check().errors, [])

    def test_same_page_anchor(self):
        tree = Tree(self, {"content/docs/cli/overview.md": page("O", "## Here\n\n[up](#here) [no](#gone)")})
        rep = tree.check()
        self.assertEqual(len(errors_of(rep, "anchor '#gone'")), 1)
        self.assertFalse(errors_of(rep, "'#here'"))

    def test_relative_link_is_refused(self):
        tree = Tree(self, {"content/docs/cli/overview.md": page("O", "See [x](install/).")})
        self.assertTrue(errors_of(tree.check(), "must be root-absolute"))

    def test_missing_trailing_slash(self):
        tree = Tree(self, {"content/docs/cli/overview.md": page("O", "See [x](/docs/cli/install).")})
        self.assertTrue(errors_of(tree.check(), "needs its trailing slash"))

    def test_hand_written_landing_is_checked_too(self):
        tree = Tree(self)
        index = tree.site / "index.html"
        index.write_text(index.read_text().replace("#first-launch", "#first-run"), encoding="utf-8")
        rep = tree.check()
        self.assertTrue(errors_of(rep, "no id 'first-run'"))

    def test_downloads_are_not_built_and_not_checked(self):
        self.assertFalse(errors_of(Tree(self).check(), "/downloads/"))

    def test_well_formedness(self):
        self.assertEqual(B.scan_html("<div><p>ok</p><img src=x><svg><path d=''/></svg></div>").problems, [])
        self.assertTrue(B.scan_html("<div><p>open</div>").problems)
        self.assertTrue(B.scan_html("<span/>").problems)


class Denylist(unittest.TestCase):
    POSITIVES = [
        ("pipeline(", "Call pipeline(steps) here."),
        ("Keychain", "Keys live in the Keychain."),
        ("Keychain", "keys in the keychain"),
        ("SwarmCode", "Open SwarmCode."),
        ("swarmcode", "Run swarmcode now."),
        ("swarm_code", "The swarm_code module."),
        ("daemon", "The daemon starts."),
        ("spec N", "As spec 74 says."),
        ("pass N", "Since pass 12."),
        ("/Users/", "Look in /Users/me."),
        ("sk-ant-", "key sk-ant-abc"),
        ("sk-proj-", "key sk-proj-abc"),
        ("tvly-", "key tvly-abc"),
        ("LLMOTIONS_API_KEY=", "export LLMOTIONS_API_KEY=x"),
    ]
    NEGATIVES = [
        "Run {{old_cmd}} if you still have it.",
        "A bypass 2 times and a specification 3 are fine.",
        "Pipelines and a pipeline are words, not calls.",
        "<!-- source: D:lib/swarm_code/engine/daemon.ex:1, C:rel/overlays/bin/swarmcode:17 -->",
        "The {{data_dir}} folder.",
    ]

    def scan(self, line, label="docs/cli/x.md"):
        rep = B.Report()
        B.denylist_scan(label, [line], 1, rep, allow_ok=False)
        return rep

    def test_every_term_is_caught(self):
        for term, line in self.POSITIVES:
            with self.subTest(term=term):
                self.assertTrue(errors_of(self.scan(line), repr(term)), line)

    def test_negatives_pass(self):
        for line in self.NEGATIVES:
            with self.subTest(line=line):
                self.assertEqual(self.scan(line).errors, [])

    def test_secrets_are_caught_inside_comments(self):
        self.assertTrue(self.scan("<!-- source: /Users/me/x.ex:1 -->").errors)
        self.assertTrue(self.scan("<!-- tvly-123 -->").errors)

    def test_multi_line_comments_hide_brand_terms_only(self):
        rep = B.Report()
        B.denylist_scan("x.md", ["<!-- source:", "D:lib/swarm_code/a.ex:1 sk-ant-x", "-->", "SwarmCode"], 1, rep, False)
        self.assertEqual(len(errors_of(rep, "'sk-ant-'")), 1)
        self.assertEqual(len(errors_of(rep, "'SwarmCode'")), 1)
        self.assertFalse(errors_of(rep, "'swarm_code'"))

    def test_allow_comment(self):
        rep = B.Report()
        B.denylist_scan("shared/secrets.md", ["Not the Keychain. <!-- allow: Keychain -->"], 1, rep, True)
        self.assertEqual((rep.errors, rep.warnings), ([], []))
        rep = B.Report()
        B.denylist_scan("cli/x.md", ["Not the Keychain. <!-- allow: Keychain -->"], 1, rep, False)
        self.assertEqual(rep.errors, [])
        self.assertTrue(rep.warnings, "an allow outside the two partials is flagged")
        rep = B.Report()
        B.denylist_scan("shared/names.md", ["SwarmCode and swarmcode <!-- allow: SwarmCode -->"], 1, rep, True)
        self.assertEqual(len(rep.errors), 1, "an allow covers only the named term")

    def test_a_page_hit_fails_the_check(self):
        tree = Tree(self, {"content/docs/cli/overview.md": page("O", "It runs as a daemon.")})
        self.assertTrue(errors_of(tree.check(), "denylisted 'daemon'"))

    def test_names_partial_uses_its_allow(self):
        self.assertFalse(errors_of(Tree(self).check(), "denylisted"))

    def test_import_hits_are_reported_for_lane_a(self):
        tree = Tree(self, {"content/import/keybindings.md":
                           "<!-- source: C:docs/keybindings.md -->\n### Keys\n\nRun swarmcode.\n"})
        rep = tree.check()
        self.assertTrue(errors_of(rep, "denylisted 'swarmcode'"))
        self.assertTrue([w for w in rep.warnings if "lane A" in w])


class Partials(unittest.TestCase):
    def test_partial_is_inserted_with_its_headings(self):
        files, rep, _ = Tree(self).build()
        html = files["docs/cli/install/index.html"].decode()
        self.assertIn('<h3 id="approval-modes">', html)
        self.assertIn("A dangerous command always asks.", html)

    def test_missing_partial(self):
        tree = Tree(self, remove=["content/docs/shared/approvals.md"])
        self.assertTrue(errors_of(tree.build()[1], "missing partial shared/approvals"))

    def test_partial_outside_the_fixed_set(self):
        tree = Tree(self, {"content/docs/cli/overview.md": page("O", "{{> shared/cooking}}")})
        self.assertTrue(errors_of(tree.build()[1], "not in the fixed partial set"))

    def test_partials_do_not_nest_and_start_at_h3(self):
        tree = Tree(self, {"content/docs/shared/approvals.md":
                           "## Too high\n\n{{> shared/names}}\n\n<!-- source: D:x:1 -->\n"})
        rep = tree.build()[1]
        self.assertTrue(errors_of(rep, "a partial starts at `###`"))
        self.assertTrue(errors_of(rep, "partials do not nest"))

    def test_partial_without_source_comment(self):
        tree = Tree(self, {"content/docs/shared/approvals.md": "### Modes\n\nText.\n"})
        self.assertTrue(errors_of(tree.build()[1], "no `<!-- source"))

    def test_include_must_be_alone_on_its_line(self):
        tree = Tree(self, {"content/docs/cli/overview.md": page("O", "Text {{> shared/names}}")})
        self.assertTrue(errors_of(tree.build()[1], "alone on its line"))

    def test_import_ref_reaches_the_footer(self):
        files, rep, _ = Tree(self).build()
        self.assertIn("generated from the ncode CLI at <code>0123abc</code>",
                      files["docs/cli/keys/index.html"].decode())

    def test_convert_reference(self):
        text = "# Title\n\nGenerated by `mix x`.\nDo not edit.\n\nIntro.\n\n## A\n\n### B\n\n```sh\n## not a heading\n```\n| `{{` | x |\n"
        out = B.convert_reference(text)
        self.assertTrue(out.startswith("Intro."))
        self.assertIn("### A\n", out)
        self.assertIn("#### B\n", out)
        self.assertIn("## not a heading", out)
        self.assertIn("`\\{{`", out)
        self.assertNotIn("Generated by", out)

    def test_import_cli_writes_both_partials(self):
        tree = Tree(self)
        code, log = tree.run("--import-cli", str(FX / "cli"), "--ref", "abcdef1")
        self.assertEqual(code, 0, log)
        text = (tree.content / "import/settings.md").read_text()
        self.assertIn("<!-- import-ref: abcdef1 -->", text)
        self.assertIn("### Models & effort", text)
        code, log = tree.run("--import-cli", str(FX / "cli"), "--ref", "not-a-sha")
        self.assertEqual(code, 1)


class Names(unittest.TestCase):
    def test_names_everywhere_including_code_fences(self):
        html = Tree(self).build()[0]["docs/cli/install/index.html"].decode()
        self.assertIn("curl -fsSL https://code.llmotions.com/install.sh | sh</code>", html)
        self.assertIn("<code>ncode 0.1.0</code>", html)
        self.assertIn("macOS 15 or later on Apple silicon (arm64)", html)
        self.assertIn("<title>Install · ncode CLI docs</title>", html)

    def test_escaped_braces_stay_literal(self):
        html = Tree(self).build()[0]["docs/cli/install/index.html"].decode()
        self.assertIn("a literal {{cmd}}.", html)
        keys = Tree(self).build()[0]["docs/cli/keys/index.html"].decode()
        self.assertIn("<code>{{</code>", keys)

    def test_unknown_name_is_a_build_error(self):
        tree = Tree(self, {"content/docs/cli/overview.md": page("O", "Run {{nope}}.")})
        code, log = tree.run("--out", str(tree.root / "out"))
        self.assertEqual(code, 1)
        self.assertIn("unknown name {{nope}}", log)
        self.assertFalse((tree.root / "out").exists(), "nothing is written on a build error")


class Placeholders(unittest.TestCase):
    def test_normal_build_renders_nothing(self):
        files, rep, placeholders = Tree(self).build()
        self.assertNotIn('class="ph', files["docs/cli/index.html"].decode())
        self.assertEqual(len(placeholders), 3)

    def test_draft_draws_dashed_boxes_and_noindex(self):
        files = Tree(self).build(draft=True)[0]
        html = files["docs/cli/index.html"].decode()
        self.assertIn('<div class="ph ph-capture" role="note"><span class="ph-kind">Terminal capture · cli/session · 120x36</span>', html)
        self.assertIn('<meta name="robots" content="noindex">', html)
        self.assertIn("Screenshot · desktop/gatekeeper-1.png · owner", files["docs/desktop/install/index.html"].decode())

    def test_check_warns_and_release_fails(self):
        tree = Tree(self)
        code, log = tree.run("--check", "--no-drift")
        self.assertEqual(code, 0, log)
        self.assertIn("warning:", log)
        self.assertIn("capture placeholder left", log)
        code, log = tree.run("--check", "--no-drift", "--release")
        self.assertEqual(code, 1)
        self.assertIn("error:", log)
        self.assertIn("capture placeholder left", log)
        self.assertIn("TBD left in releases.md", log)

    def test_malformed_placeholder(self):
        tree = Tree(self, {"content/docs/cli/overview.md": page("O", "<!-- capture: session | x -->")})
        self.assertTrue(errors_of(tree.build()[1], "capture placeholder must be"))


class Release(unittest.TestCase):
    SHA = "a" * 64
    RELEASE = ("## 0.1.0 — 2026-10-02 {#v0-1-0}\n- cli: ncode-0.1.0-darwin-arm64.tar.gz sha256 %s\n"
               "- desktop: ncode-0.1.0.dmg sha256 %s\n\n- First preview.\n" % ("a" * 64, "b" * 64))

    def tree(self, install, dmg_sha="b" * 64):
        overrides = {"content/releases.md": self.RELEASE}
        for rel in ("content/docs/cli/overview.md", "content/docs/desktop/overview.md",
                    "content/docs/desktop/install.md"):
            text = (FX / rel).read_text()
            overrides[rel] = "\n".join(l for l in text.split("\n") if "capture:" not in l and "shot:" not in l)
        if install is not None:
            overrides["site/install.sh"] = install
        landing = (FX / "site" / "index.html").read_text()
        overrides["site/index.html"] = landing.replace(
            '<h1 id="top">', '<p>ncode 0.1.0 <code id="dmg-sha">%s</code></p><h1 id="top">' % dmg_sha)
        return Tree(self, overrides)

    STAMPED = 'main() {\n  VERSION="${NCODE_VERSION:-0.1.0}"\n  SHA256="%s"\n}\nmain "$@"\n' % ("a" * 64)

    def test_release_passes_when_everything_is_stamped(self):
        code, log = self.tree(self.STAMPED).run("--check", "--no-drift", "--release")
        self.assertEqual(code, 0, log)

    def test_install_sh_pinning_an_older_release_fails(self):
        install = 'VERSION="${NCODE_VERSION:-0.0.9}"\nSHA256="%s"\n' % ("c" * 64)
        code, log = self.tree(install).run("--check", "--no-drift", "--release")
        self.assertEqual(code, 1)
        self.assertIn("do not match the newest release", log)
        code, log = self.tree(install).run("--check", "--no-drift")
        self.assertEqual(code, 0, "a mismatch is a warning outside --release")

    def test_unstamped_install_sh_fails_release(self):
        install = 'VERSION="${NCODE_VERSION:-@VERSION@}"\nSHA256="@SHA256@"\n'
        code, log = self.tree(install).run("--check", "--no-drift", "--release")
        self.assertEqual(code, 1)

    def test_missing_install_sh_warns_and_fails_release(self):
        code, log = self.tree(None).run("--check", "--no-drift")
        self.assertEqual(code, 0, log)
        self.assertRegex(log, r"warning: \S*install\.sh: missing")
        code, log = self.tree(None).run("--check", "--no-drift", "--release")
        self.assertEqual(code, 1, "a release without the installer is not a release")
        self.assertRegex(log, r"error: \S*install\.sh: missing")

    def test_landing_dmg_sha_must_match_releases(self):
        for sha, needle in (("c" * 64, "does not match the newest release"),
                            ("TBD", "does not match the newest release")):
            tree = self.tree(self.STAMPED, dmg_sha=sha)
            code, log = tree.run("--check", "--no-drift")
            self.assertEqual(code, 0, "a warning outside --release: " + log)
            self.assertIn(needle, log)
            code, log = tree.run("--check", "--no-drift", "--release")
            self.assertEqual(code, 1)
            self.assertRegex(log, r"error: \S*index\.html: DMG SHA-256")
        tree = self.tree(self.STAMPED)
        index = tree.site / "index.html"
        index.write_text(index.read_text().replace('<code id="dmg-sha">', "<code>"), encoding="utf-8")
        code, log = tree.run("--check", "--no-drift", "--release")
        self.assertEqual(code, 1)
        self.assertIn('no <code id="dmg-sha">', log)

    def test_landing_version_and_dmg_name_follow_releases(self):
        tree = self.tree(self.STAMPED)
        index = tree.site / "index.html"
        index.write_text(index.read_text().replace("ncode 0.1.0", "ncode 0.0.9")
                         .replace("/downloads/ncode-0.1.0.dmg", "/downloads/ncode-0.0.9.dmg"), encoding="utf-8")
        code, log = tree.run("--check", "--no-drift", "--release")
        self.assertEqual(code, 1)
        self.assertIn("version 0.0.9 is not the newest release 0.1.0", log)
        self.assertIn("no download link to /downloads/ncode-0.1.0.dmg", log)
        tree = self.tree(self.STAMPED)
        names = tree.content / "names.json"
        names.write_text(names.read_text().replace('"ncode-0.1.0.dmg"', '"ncode-0.2.0.dmg"'), encoding="utf-8")
        code, log = tree.run("--check", "--no-drift", "--release")
        self.assertEqual(code, 1)
        self.assertIn("names.json: dmg 'ncode-0.2.0.dmg' differs", log)

    def test_tbd_in_a_hand_written_page(self):
        tree = self.tree(None)
        index = tree.site / "index.html"
        index.write_text(index.read_text().replace("<h1 id=\"top\">", "<p>SHA-256 TBD</p><h1 id=\"top\">"),
                         encoding="utf-8")
        code, log = tree.run("--check", "--no-drift")
        self.assertEqual(code, 0, log)
        self.assertIn("TBD left in a hand-written page", log)
        code, log = tree.run("--check", "--no-drift", "--release")
        self.assertEqual(code, 1)

    def test_newest_release(self):
        info = B.newest_release(self.RELEASE + "\n## 0.0.1 — 2026-01-01\n- cli: old sha256 dead\n")
        self.assertEqual(info["version"], "0.1.0")
        self.assertEqual(info["cli"], ("ncode-0.1.0-darwin-arm64.tar.gz", self.SHA))

    def test_releases_page(self):
        html = Tree(self).build()[0]["releases/index.html"].decode()
        self.assertIn('<h2 id="v0-1-0">0.1.0 — 2026-10-XX', html)
        self.assertIn("The first developer preview of ncode.", html)


class Structure(unittest.TestCase):
    def test_page_not_in_nav(self):
        tree = Tree(self, {"content/docs/cli/extra.md": page("Extra", "Text.")})
        self.assertTrue(errors_of(tree.build()[1], "page is not in _nav.txt"))

    def test_nav_entry_without_page(self):
        tree = Tree(self, remove=["content/docs/cli/keys.md"])
        self.assertTrue(errors_of(tree.build()[1], "entry 'keys' has no page"))

    def test_bad_slug_and_missing_overview(self):
        tree = Tree(self, {"content/docs/cli/_nav.txt": "# G\nInstall | Install\ninstall | Install\nkeys | Keys\n"})
        rep = tree.build()[1]
        self.assertTrue(errors_of(rep, "is not lowercase"))
        self.assertTrue(errors_of(rep, "needs an `overview` page"))

    def test_page_without_source_comment(self):
        tree = Tree(self, {"content/docs/cli/overview.md": page("O", "Text.", source=False)})
        self.assertTrue(errors_of(tree.build()[1], "no `<!-- source"))

    def test_front_matter(self):
        tree = Tree(self, {"content/docs/cli/overview.md":
                           "---\ntitle: O\nauthor: me\ndescription: %s\n---\n\nx\n<!-- source: D:x:1 -->\n" % ("d" * 161)})
        rep = tree.build()[1]
        self.assertTrue(errors_of(rep, "allows only `title:` and `description:`"))
        self.assertTrue(errors_of(rep, "at most 160"))

    def test_urls_prev_next_sidebar_and_toc(self):
        files = Tree(self).build()[0]
        html = files["docs/cli/install/index.html"].decode()
        self.assertIn('<a class="d-prev" rel="prev" href="/docs/cli/">', html)
        self.assertIn('<a class="d-next" rel="next" href="/docs/cli/keys/">', html)
        self.assertIn('<a href="/docs/cli/install/" aria-current="page">Install</a>', html)
        self.assertIn('<details class="d-menu">', html)
        self.assertIn('<li><a href="#uninstall-2">Uninstall</a><ul><li><a href="#approval-modes">', html)
        self.assertIn('<a href="/docs/cli/" aria-current="true">CLI</a>', html)
        self.assertNotIn("site.js", html)
        self.assertNotIn("three", html)
        self.assertNotIn("reveal", html)
        self.assertIn('class="skip" href="#main"', html)
        self.assertIn("docs/cli/overview/index.html" not in files and "docs/cli/index.html", files)

    def test_hub_search_sitemap_robots(self):
        files = Tree(self).build()[0]
        hub = files["docs/index.html"].decode()
        self.assertIn('<a href="/docs/desktop/">ncode Desktop</a>', hub)
        self.assertIn('<a href="/docs/cli/keys/">Keyboard reference</a>', hub)
        import json
        index = json.loads(files["docs/cli/search.json"])
        self.assertEqual(index["product"], "cli")
        self.assertEqual([p["u"] for p in index["pages"]], ["/docs/cli/", "/docs/cli/install/", "/docs/cli/keys/"])
        self.assertIn(["First launch", "first-launch",
                       "Open the DMG and drag ncode.app to Applications. Open System Settings → Privacy & "
                       "Security and choose Open Anyway. Warning: Only open a DMG you downloaded from "
                       "code.llmotions.com."],
                      json.loads(files["docs/desktop/search.json"])["pages"][1]["s"])
        sitemap = files["sitemap.xml"].decode()
        self.assertIn("<loc>https://code.llmotions.com/docs/desktop/install/</loc>", sitemap)
        self.assertIn("Sitemap: https://code.llmotions.com/sitemap.xml", files["robots.txt"].decode())

    def test_assets_are_copied_and_stamped(self):
        files = Tree(self).build()[0]
        self.assertEqual(files["assets/llm.css"], (FX / "assets/llm.css").read_bytes())
        self.assertIn("assets/brand/favicon.png", files)
        sha = B.sha8((FX / "site/assets/docs.css").read_bytes())
        self.assertIn('href="/assets/docs.css?v=%s"' % sha, files["docs/cli/index.html"].decode())
        self.assertIn('href="/assets/docs.css?v=%s"' % sha, files["index.html"].decode(),
                      "hand-written pages get fresh stamps")

    def test_usage_errors(self):
        for args in (["--release"], ["--check", "--draft"], ["--no-drift"], ["--ref", "abc1234"]):
            with self.subTest(args=args), redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as ctx:
                    B.main(args)
                self.assertEqual(ctx.exception.code, 2)


class Markdown(unittest.TestCase):
    def render(self, text):
        rep = B.Report()
        src = B.Source()
        src.extend(text.split("\n"), "t.md", 1)
        doc = B.render_markdown(B.preprocess(src, {"cmd": "ncode"}, rep), rep)
        return "\n".join(doc.parts), doc, rep

    def test_anchor_ids(self):
        html, doc, rep = self.render("## Hello, World!\n## Hello world\n### `ncode --help` & more\n## Custom {#mine}\n## ⌘")
        self.assertEqual([h[3] for h in doc.headings], ["hello-world", "hello-world-2", "ncode-help-more", "mine", "section"])

    def test_inline(self):
        html, _, rep = self.render("A **b** *c* `d <e>` [[⌘K]] [f](/docs/cli/) ![g](/assets/shots/cli/x.png) a * b")
        self.assertIn("A <strong>b</strong> <em>c</em> <code>d &lt;e&gt;</code> <kbd>⌘K</kbd> "
                      '<a href="/docs/cli/">f</a> <img src="/assets/shots/cli/x.png" alt="g" loading="lazy"> a * b', html)

    def test_raw_html_is_escaped_and_warned(self):
        html, _, rep = self.render("Hi <script>alert(1)</script>")
        self.assertIn("&lt;script&gt;", html)
        self.assertTrue(rep.warnings)

    def test_lists(self):
        html, _, _ = self.render("- a\n  - b\n  - c\n- d\n  continued\n\n1. one\n2. two")
        self.assertIn("<ul><li>a<ul><li>b</li><li>c</li></ul></li><li>d continued</li></ul>", html)
        self.assertIn("<ol><li>one</li><li>two</li></ol>", html)

    def test_term_fence_and_code_fence(self):
        html, _, rep = self.render("```term\n│ {{cmd}} │\n```\n\n```sh\n{{cmd}} --version\n```\n\n```\nno lang\n```")
        self.assertIn('<div class="term"><pre>│ ncode │</pre></div>', html)
        self.assertIn('<button type="button" class="copy" hidden>Copy</button></div><pre><code class="language-sh">ncode --version</code>', html)
        self.assertTrue(errors_of(rep, "needs a language"))

    def test_callouts(self):
        html, _, rep = self.render("> **Tip** Use it.\n\n> **Warning** Careful\n> here.\n\n> plain")
        self.assertIn('<div class="callout callout-tip" role="note"><p><strong class="callout-label">Tip</strong> Use it.</p></div>', html)
        self.assertIn("Careful here.", html)
        self.assertTrue(rep.warnings)

    def test_table_cells(self):
        self.assertEqual(B.split_cells("| `a|b` | c \\| d | e |"), ["`a|b`", "c | d", "e"])

    def test_comments_vanish(self):
        html, _, _ = self.render("one\n<!-- source: x -->\ntwo <!-- allow: Keychain -->\n<!--\nmulti\n-->\nthree")
        self.assertEqual(html, "<p>one two three</p>")

    def test_h1_in_body_is_an_error(self):
        _, _, rep = self.render("# Title")
        self.assertTrue(errors_of(rep, "no `#` heading"))


if __name__ == "__main__":
    unittest.main()
