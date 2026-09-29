---
title: Themes
description: Pick one of eight themes in dark or light mode, reduce motion, and choose how the transcript and window behave.
---

{{product}} comes with eight themes, each in a dark and a light mode. Open **Settings → Appearance** to choose.

## Themes

| Theme | Accent |
|---|---|
| Carbon (default) | orange |
| Obsidian | indigo |
| Graphite & Amber | amber |
| Aurora Glass | teal |
| Ember | burnt orange |
| Fjord | sea blue |
| Dusk | coral |
| Paper | terracotta |

Click a theme to apply it at once. **Mode** switches between **Dark** and **Light**; the sun or moon button in the rail does the same from anywhere.

![The same conversation in all eight themes, dark mode, as a 4 × 2 grid: Carbon, Obsidian, Graphite & Amber, Aurora Glass, Ember, Fjord, Dusk and Paper.](/assets/shots/desktop/themes-grid.webp)
![The same conversation in the Paper theme, light mode.](/assets/shots/desktop/themes-paper-light.webp)

## Motion

**Reduce motion** turns off panel, popover and progress animations everywhere. Progress still updates; it just does not animate.

## Other appearance settings

- **Consensus card**: the default layout of a judged turn's card (Scales, Rail, Spine or Scorecard). See [Consensus](/docs/desktop/consensus/#card-layouts).
- **Bring the window to front when a run finishes** (off): with it off, a finished run only posts a notification and never switches your desktop.
- **Show global scheduled tasks** (on): lists tasks without a project under a **GLOBAL** group in the sidebar.
- **Expand activity & reasoning by default** (off): whether the "Worked for…" and "Thinking" sections of an answer start open.

<!-- source: D:lib/swarm_code/settings.ex:55-65,94, D:lib/swarm_code_web/live/settings_live.ex:52-60, D:lib/swarm_code_web/live/settings_live.html.heex:605-750, D:lib/swarm_code/settings/setting.ex:12-16,90-92, D:lib/swarm_code_web/components/frame.ex:455-463, D:lib/swarm_code/settings/setting.ex:20, D:lib/swarm_code/scheduled/sidebar.ex:296-301 -->
