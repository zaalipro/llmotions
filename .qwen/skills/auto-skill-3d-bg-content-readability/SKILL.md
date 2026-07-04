---
name: 3d-bg-content-readability
description: Keep Three.js/animated 3D backgrounds from destroying text readability on marketing pages
source: auto-skill
extracted_at: '2026-07-04T15:42:18.936Z'
---

# Fixed 3D backgrounds vs. content readability

When a page has a full-screen animated 3D background (Three.js `#bg` canvas, wireframe
torus knots, particle fields) behind normal scrolling content, the recurring failure is
the **3D geometry visually collides with text** — a bright wireframe knot tangles right
through a two-column feature list and makes it unreadable. This project (llmotions:
index.html + cympho.html + cymphony.html sharing assets/llm.css + assets/site.js) hit
this repeatedly.

## Root causes (check all three)

1. **`perspective: NNNpx` on `body`** breaks `position: fixed` for the background canvas —
   the canvas stops being viewport-fixed and disappears/clips as you scroll. Remove
   `perspective` from `body`; put page background color on `html` and make `body`
   `background: transparent` so the fixed `#bg` canvas shows through every section.
2. **Background layers at `z-index: 1`** can sit at or above content. Force all ambient
   layers (`#bg`, `#cursor`, `#particles`) to `z-index: 0`; give content sections a real
   stacking context (`section { position: relative; z-index: 2 }`) and put dense content
   grids at a higher `z-index` (e.g. `.checks { z-index: 10 }`).
3. **The 3D mesh is too bold / too close to the camera.** In `site.js`, the torus knot
   fighting the content was fixed by: lowering `MeshBasicMaterial.opacity` (0.08 → ~0.025),
   pushing it back on Z (`torus.position.z = -18`), and enlarging its radius so curves are
   gentler. Treat hero 3D as faint atmosphere, never a foreground element over text.

## Make content survive on top of any background

Even with a tamed background, transparent glass cards let a busy starfield bleed through.
For content that MUST stay readable, use **near-opaque dark glass**, not light glass:

```css
.checks li {
  background: linear-gradient(135deg, rgba(24,21,40,0.94) 0%, rgba(13,13,24,0.92) 100%);
  border: 1px solid rgba(139,92,246,0.16);
  backdrop-filter: blur(34px) saturate(140%);
  box-shadow: 0 12px 44px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.06);
}
```

0.9+ alpha dark fill + heavy blur keeps text crisp while still reading as "glass".

## Bento pitfall

Don't set `grid-column: span 2` on individual `nth-child` items in a fixed N-column grid
unless the spans actually sum to N per row — mismatched spans overflow and misalign. A
clean `repeat(2, 1fr)` card grid looked better than a broken 4-col bento here.

## Emoji → SVG icons

Replacing emoji (🎨⚡🎯) with inline stroke SVGs (feather/lucide-style, 24×24,
`stroke="currentColor" stroke-width="2"`) gives a consistent monochrome look. Style via
`.ficon svg { width:32px; height:32px; color: rgba(255,255,255,0.85); }` and brighten to
`#fff` on card hover. Note: after editing the file the browser may still show the old
emoji from cache — the on-disk edit is correct; a hard refresh (Cmd+Shift+R) is needed
before judging.

## Image lightbox

A satisfying click-to-zoom modal is cheap: inject one `.modal-overlay` at DOM end, wire
`.shot img, .gallery img` clicks to swap `src` and toggle `.active`, close on button /
backdrop click / Escape, and lock `body { overflow: hidden }` while open. Animate with
`opacity` + `transform: scale(0.9→1)` on the overlay/content.

## Consistency across a multi-page site

Users land on the polished index then click through to sub-pages. Sub-pages here used
classes (`.app-hero`, `.shot`, `.fgrid`, `.checks`, `.steps`, `.roles`, `.install`,
`.code`) that DIDN'T EXIST in the shared CSS, so they rendered as raw unstyled screenshots
dominating the viewport. When sharing one stylesheet, audit that EVERY class used in
sub-pages is actually defined — grep each class name — before calling it done.

## Process lesson

The user repeatedly pushed back with "do you call it done/beautiful?" screenshots. Font +
CSS-bugfix swaps are polish, not the "stunning redesign" that was asked for. When the ask
is visual quality, actually look at the rendered screenshot critically (does 3D overlap
text? are cards readable? do sub-pages match the hero?) instead of declaring success from
the diff.
