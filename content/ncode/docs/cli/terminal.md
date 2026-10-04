---
title: Terminal, themes and mouse
description: Which terminals draw the richest screen, dark and light themes, plain glyphs and monochrome, the mouse, vim keys, and layout settings.
---

`{{cmd}}` runs in any terminal on macOS and adapts to what the terminal can show. Everything on this page is a setting of **this terminal**, kept in `cli.json` beside the database, so the desktop app is not affected.

## Supported terminals

The full glyph set, with thin rails and fine progress bars, needs a truecolor terminal whose `TERM` names **Ghostty**, **kitty**, **WezTerm** or **iTerm**. Everywhere else, including Terminal.app and inside tmux or GNU screen, `{{cmd}}` draws a plainer glyph set with the same layout and keys.

![The four-agent swarm in the rich truecolor glyph tier: thin transcript rails and tree branches, fine tick-style swarm progress bars, one verification approval waiting, the full side panel, and auto approval mode.](/assets/shots/cli/tier-rich.webp)

![The matching four-agent swarm in the Terminal.app-style measured glyph tier, with plainer tree connectors, wider rails and outlined progress cells, while the approval, agent rows, composer and auto status line keep the same layout.](/assets/shots/cli/tier-plain.webp)

## Dark and light

`/theme dark` and `/theme light` switch at once and are remembered. At launch the theme is chosen in this order:

1. `{{env_prefix}}THEME=dark` or `light`, while it is set;
2. the theme you chose with `/theme` (or in Settings → Appearance);
3. the desktop app's light or dark mode;
4. dark.

![The matching four-agent swarm in ncode's light theme: a pale transcript and panel, coloured agent names, Verify changes waiting for approval, thin rich-tier rails and progress bars, $0.04 spent, and auto approval mode.](/assets/shots/cli/theme-light.webp)

## Plain glyphs and monochrome

- `{{env_prefix}}ASCII=1`, or **Glyphs** in Settings → Appearance, draws plain ASCII glyphs, for a terminal or font without the symbols.
- `NO_COLOR` gives a monochrome screen; **Colours** in Settings → Appearance sets colour too.
- **Ambiguous-width characters** (narrow or wide) fixes misaligned borders in fonts that draw box characters two cells wide.
- **Reduced motion** is a switch on the same page.
- **Accent colour** takes a `#RRGGBB` value.

These apply at the next launch.

![The matching four-agent swarm with ASCII glyphs: S swarm marks, pipe and backtick tree connectors, hyphen progress bars and composer divider, one verification approval waiting, and the full side panel with auto approval mode.](/assets/shots/cli/tier-ascii.webp)

## Mouse and selection

- The mouse wheel scrolls the pane under the pointer, three lines a notch (**Lines per notch** in Settings → Keys & input).
- To select text while the wheel is on, hold [[Shift]] while dragging; in Terminal.app and iTerm2, hold [[Option]].
- `/mouse off` gives the terminal its own mouse selection back; `/mouse on` turns wheel scrolling on again. `{{env_prefix}}MOUSE=0` or `1` wins over both while set.

## Vim keys

`{{env_prefix}}KEYMAP=vim`, **Vim mode** in the [[Ctrl]]+[[P]] palette, or **Keymap** in Settings → Keys & input gives the composer vim's NORMAL and VISUAL modes. See the [keyboard reference](/docs/cli/keys/).

## Layout

In Settings → Layout & transcript:

| Setting | Default |
|---|---|
| Side panel | full |
| Composer height | 3 rows |
| Show diffs | on (`/diff on\|off`) |
| Diff lines shown | 12 |
| AI status lines | on |
| Notices stay for | 6 s |

The editor [[Ctrl]]+[[X]] opens is `$VISUAL`, then `$EDITOR`, then `vi`; **Editor for Ctrl-X** in Settings → Keys & input overrides it.

## Terminal.app and Alt

- Nothing essential needs [[Alt]], so a terminal where Option does not send Alt loses no essential action.
- In Terminal.app, select text with [[Option]]-drag while the wheel is on.
- [[Ctrl]]+[[Shift]]+[[Z]] (redo) needs a terminal that reports Ctrl with Shift.

<!-- source: C:AGENTS.md:165-168, C:AGENTS.md:186-188, C:AGENTS.md:193-202, C:README.md:90-92, C:README.md:115-118, C:README.md:197-200, C:README.md:332-333, C:docs/settings.md:123-155, C:docs/keybindings.md:9-13,77 -->
