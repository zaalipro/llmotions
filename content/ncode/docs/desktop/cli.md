---
title: Using with the CLI
description: Run the ncode desktop app and the ncode terminal app on one Mac: one shared database, one at a time, and what only the app does.
---

{{product}} also comes as a terminal app, `{{cmd}}`, for people who live in the terminal. It runs the same engine and reads and writes the same data as the desktop app, so you can start a conversation in one and continue it in the other.

Install it with one line:

```sh
{{install}}
```

See the [CLI docs](/docs/cli/) for everything about the terminal app.

{{> shared/together}}

## A typical day with both

1. Work in the desktop app during the day; its schedules and retention run while it is open.
2. Before a terminal session (over SSH, in a tmux pane), quit the app with [[⌘]]+[[Q]].
3. Run `{{cmd}}`. Your projects, conversations and keys are all there.
4. When you are done, exit `{{cmd}}`, then open the app again. The conversations you had in the terminal are in the sidebar.

## Differences to expect

The two apps share their features but not their screens:

| In the desktop app | In the terminal app |
|---|---|
| approval buttons on cards | single-key answers |
| the agents pane with tree, grid, timeline and changes | a side panel and an agents overlay |
| settings in the Settings window | settings in a full-screen settings view, and `{{cmd}} config` for scripts |
| schedules fire | schedules can be managed but do not fire |

<!-- source: C:README.md:64-68,122-124, C:AGENTS.md:10-14,122-137, C:native/platform_identity/README.md:30, C:apps/swarm_code_daemon/lib/swarm_code/daemon/boot.ex:14, D:config/runtime.exs:21-29, D:lib/swarm_code/scheduler.ex:1-19 -->
