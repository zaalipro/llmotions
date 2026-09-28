---
title: Keyboard shortcuts
description: The ncode desktop shortcuts, the fixed keys of the composer and research page, and how to change them in Settings → Keybindings.
---

## App shortcuts

These nine shortcuts work anywhere in the window, and you can change every one of them:

| Action | Default |
|---|---|
| Toggle panel (show or hide the sidebar) | [[⌘]]+[[B]] |
| New chat | [[⌘]]+[[N]] |
| Search conversations | [[⌘]]+[[K]] |
| Settings | [[⌘]]+[[,]] |
| Quit | [[⌘]]+[[Q]] |
| Toggle side chat | [[⌘]]+[[Shift]]+[[S]] |
| Resize panes left | [[Shift]]+[[⌥]]+[[←]] |
| Resize panes right | [[Shift]]+[[⌥]]+[[→]] |
| File finder | [[⌘]]+[[P]] |

[[⌘]]+[[Q]] and [[⌘]]+[[,]] also work while you are typing in a text field.

## Fixed keys

| Where | Key | Action |
|---|---|---|
| Composer | [[Return]] | send |
| Composer | [[Shift]]+[[Return]] | new line |
| Composer | [[Shift]]+[[Tab]] | switch between Build and Plan |
| Composer | [[/]] as the first character | open the command list |
| Deep research | [[⌘]]+[[Return]] | start the research |

## Changing a shortcut

1. Open **Settings → Keybindings**.
2. Click **Edit** next to an action. The row says *Press a key combo...*
3. Press the new combination (it needs at least one modifier key). It is saved at once. Click **Cancel** to keep the old one.

**Reset all to defaults** restores the nine defaults.

<!-- source: D:lib/swarm_code/settings.ex:98-110, D:lib/swarm_code_web/live/settings_live.ex:2614-2641,2059-2090, D:lib/swarm_code_web/live/settings_live.html.heex:1325-1386, D:assets/js/hooks.js:679-690,720-730,853-860,879-882, D:lib/swarm_code_web/components/chat.ex:5783, D:lib/swarm_code_web/live/research_live.html.heex:197, D:lib/swarm_code/settings/setting.ex:343-371 -->
