---
title: A tour of the window
description: The rail, the sidebar, the transcript, the agents pane and the side chat: what each part of the ncode window shows and how to move around.
---

The {{product}} window has five parts, from left to right: a narrow **rail**, the **sidebar**, the **transcript** with the message box under it, the **agents pane**, and, when you open it, the **side chat**.

![The full window with its five parts outlined and numbered: 1 rail, 2 sidebar, 3 transcript and composer, 4 side chat, 5 agents pane.](/assets/shots/desktop/tour-annotated.webp)

## The rail

The narrow bar on the far left switches what the sidebar shows:

| Button | Opens |
|---|---|
| Chats | projects and conversations |
| Scheduled tasks | your scheduled tasks and a calendar ([Scheduled tasks](/docs/desktop/scheduled/)) |
| Workflows | the workflow cockpit ([Workflows](/docs/desktop/workflows/)) |
| Deep research | your researches ([Deep research](/docs/desktop/research/)) |
| Usage history | spend over the last 7, 30 or 90 days, against your monthly budget |
| Sun or moon | switches between light and dark mode |
| Gear | Settings ([[⌘]]+[[,]]) |

## The sidebar

In the Chats view the sidebar lists:

- **Pinned** conversations you want to keep at hand (pinned sessions are also never cleaned up);
- **Projects**, each with its conversations. A project's **⋯** menu has **New conversation**, **Edit project…**, **Edit AGENTS.md** and **Remove project…**;
- **Conversations** that belong to no project;
- **Scheduled tasks**, with each task's recent runs under it.

The search box at the top ([[⌘]]+[[K]]) filters conversations by title. Type three or more characters to also see **Message matches** from inside every conversation. [[⌘]]+[[B]] hides and shows the sidebar.

A dot beside a conversation tells you it has something new, is running, is waiting for your answer, has queued messages or failed.

## The transcript

The middle column is the conversation. Your messages and the assistant's answers appear in order, and each run shows as a **card** with its status, its progress, its model, its time and its cost. A run's card has its controls: **Pause**, **Stop**, **Continue** or **Resume**, and **Rewind** when it changed files.

The conversation's header shows its title and a menu with **Export**, **Rename**, **Rewind…** and more. The message box at the bottom is the composer: see [Composer, modes and goals](/docs/desktop/composer/).

## The agents pane

The right-hand pane shows what the agents of the conversation are doing. Its toolbar picks one of three views:

- **Agents**: one card per agent, each with its task, status, progress bar, tokens and cost. Show them as a **Tree** (who started whom) or a **Grid**, with **Full cards** or **Compact cards**.
- **Timeline**: every step of every agent on a time axis. Click a step to inspect it in full.
- **Changes**: the files the conversation changed, with their diffs, and the branches of isolated agents.

See [Watching agents work](/docs/desktop/agents/).

## The side chat

A side chat is a second, narrower column that shows one run on its own, with a small message box of its own. Use it to follow one run, or talk about it, while the main transcript keeps going. Open it with the **Open in side chat** button on a run's card; [[⌘]]+[[Shift]]+[[S]] opens and closes it.

Drag the edges between the columns to resize them, or use [[Shift]]+[[⌥]]+[[←]] and [[Shift]]+[[⌥]]+[[→]].

## The footer

The bottom of the sidebar shows the app version, how much memory {{product}} uses, and a button that lists the keyboard shortcuts.

## Speed monitor

In the conversation view, a few small rows sit just above the footer, next to the memory chip. They show how fast the models of the conversation last wrote, in output tokens per second (for example `45 t/s`). How many rows you see depends on the mode:

| Mode | Rows |
|---|---|
| Ultra | 3: **Orchestrator**, **Worker**, **Validator** ([Ultra missions](/docs/desktop/missions/)) |
| Consensus, an armed `/swarm`, or a conversation whose latest run is a swarm | 2: **Main**, **Worker** |
| Anything else | 1: **Main** |

A row shows `—` until something has been measured. While a model is still writing, its row is marked live and shows an estimate that settles once the call ends; the estimate appears after about a second of streaming. Hover a row for the model's name, the time to its first token and, for a finished call, when it was measured. Each row shows the latest value for that role in this conversation.

## Closing and quitting

- **Closing the window** only hides it. Runs keep going and notifications still arrive. Click the {{product}} icon in the Dock, or use the menu bar icon, to bring it back. The menu bar icon also lists conversations **Waiting for you**.
- **Quitting** ([[⌘]]+[[Q]]) asks first. The dialog says what is still running. Quitting stops running work; paused workflows keep their journal and resume where they stopped.

<!-- source: D:lib/swarm_code_web/components/frame.ex:400-471,608-672,780-819,865-891,1076,1506-1528, D:lib/swarm_code_web/components/swarm_pane.ex:212-295,3482, D:lib/swarm_code_web/components/chat.ex:3318-3385,4325-4336,6367-6370, D:lib/swarm_code_web/components/chat_header.ex:80-92, D:lib/swarm_code_web/components/side_chat.ex:1-10, D:lib/swarm_code_web/live/workspace_live.ex:3179-3193,3692-3696, D:lib/swarm_code/settings.ex:98-110, D:lib/swarm_code/desktop.ex:40-50, D:lib/swarm_code/tray_menu.ex:50-60, D:lib/swarm_code_web/components/quit_modal.ex:70-120, D:lib/swarm_code_web/live/history_live.ex:1-23, D:CHANGELOG.md:302-305 -->
