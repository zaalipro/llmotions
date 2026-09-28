---
title: The session screen
description: What each part of the full-screen session shows, how to read long output, select and copy, scroll, switch conversations and quit.
---

`{{cmd}}` opens one conversation of one project in full screen. The screen is built around the composer: letters always type into your draft, and nothing you type is taken as a command unless it starts with `/`.

<!-- capture: cli/session-annotated | a full frame with five numbered areas: 1 run tabs, 2 transcript, 3 side panel, 4 composer, 5 status line; a chat turn with two tool rows and one worker running | 120x40 -->

## Layout

| Area | What it shows |
|---|---|
| Run tabs | the runs of this conversation; [[Alt]]+[[1]] … [[Alt]]+[[4]] switch to a tab as drawn |
| Transcript | your messages, the assistant's answers, and one row per tool call (a file read, an edit, a command) |
| Side panel | one row per agent at work, most urgent first; [[Ctrl]]+[[B]] cycles full, compact and hidden (see [Agents](/docs/cli/agents/)) |
| Composer | your draft; [[Enter]] sends it (see [Composer](/docs/cli/composer/)) |
| Status line | the project's approval mode (read-only, auto or full access), always, and hints for the keys that work right now |

Under 120 columns the side panel becomes a one-line strip, or disappears. A small 80 × 24 terminal still works.

<!-- capture: cli/session-narrow | the same conversation at 80x24 with the side panel as a strip | 80x24 -->

## Reading long output

A transcript row shows at most 8 KB of a prompt or an answer and 2 KB of a tool's output; the row says how much more there is. To read all of it, move to the row in select mode and press [[Enter]] (or `o`): it opens whole in a pager.

## Select mode

[[Ctrl]]+[[T]] switches from typing to selecting transcript rows:

| Key | Does |
|---|---|
| `j` / `k` | move down / up |
| [[Enter]] | open the row (the whole output, or the agent it belongs to) |
| `y` | copy the row |
| [[Esc]] or [[Ctrl]]+[[T]] | back to typing |

## Scrolling and the mouse

- [[PgUp]] / [[PgDn]] scroll the transcript; on an empty draft [[Ctrl]]+[[U]] / [[Ctrl]]+[[D]] scroll half a page.
- The mouse wheel scrolls the pane under the pointer (the transcript, the side panel, an agent overlay, the pager), three lines a notch.
- To select text with the mouse, hold [[Shift]] while dragging (in Terminal.app and iTerm2, [[Option]]). `/mouse off` hands mouse selection back to the terminal completely; see [Terminal, themes and mouse](/docs/cli/terminal/).

## Switching conversations and finding things

- [[Ctrl]]+[[P]] opens the palette: conversations, runs, the model, and the feature screens: Workflows, Deep Research, Scheduled Tasks, Settings, Usage, Changes, Checkpoints and MCP Servers.
- `/resume` opens a picker of saved conversations by title; `/new` starts a new one and keeps this one saved.
- [[Ctrl]]+[[G]] opens the runs dashboard, [[Ctrl]]+[[R]] the run palette.
- [[F1]] (or `?` outside a text field) shows every key that works where you are. [[F2]] opens [Settings](/docs/cli/settings/).

## Quitting

Press [[Ctrl]]+[[C]] twice within 1.5 seconds with nothing else to cancel. A single [[Ctrl]]+[[C]] first closes an open layer, then clears your draft ([[Ctrl]]+[[Z]] brings it back), then stops the running turn; a press that did one of those never counts towards quitting. When runs are still working, `{{cmd}}` asks:

```term
Stop 2 live runs and quit?
```

Quitting stops this session's runs. Back in your shell, a short summary lists the runs it stopped and the line to reopen the conversation:

```sh
{{cmd}} --resume <conversation-id>
```

A [[Ctrl]]+[[C]] outside the full screen (while it starts, during a `-p` run, or after the summary) simply ends the program.

<!-- capture: cli/session-exit-summary | the shell after quitting a session with one live run: the stopped run and the "--resume <id>" line | 100x12 -->

<!-- source: C:README.md:70-93, C:README.md:115-126, C:README.md:223-228, C:AGENTS.md:171-177, C:AGENTS.md:186-188, C:AGENTS.md:208-213, C:AGENTS.md:219-227, C:AGENTS.md:256-259, C:docs/keybindings.md:6-13,21-38,50-61,81-88, C:apps/swarm_code_core/lib/swarm_code/commands.ex:36-38 -->
