---
title: Plain mode (experimental)
description: The line-by-line presenter for pipes, SSH and terminals where the full screen cannot draw, with one command per input line and optional NDJSON output.
---

Plain mode drives a saved session one line at a time: you write commands on standard input, and it writes what happens as plain, append-only lines on standard output. It is meant for pipes, SSH sessions, CI logs and terminals where the full-screen view cannot draw.

> **Note** Plain mode is experimental in {{version}}. Its commands and output may change; for scripts, prefer [headless runs](/docs/cli/headless/) (`{{cmd}} -p`), whose `--json` output is one documented object.

## When it is used

- `{{cmd}} --plain` starts it on purpose.
- It is chosen by itself when standard input or standard output is not a terminal, or `TERM` is `dumb`. `{{cmd}}` then says so on stderr: `not a terminal, so the plain presenter answers (--plain).`

It opens the same saved conversation the full screen would: the project's latest, unless you add `--new` or `--resume <conversation-id>`.

## Commands

One command per line. `help` prints the list with its arguments.

| Command | Does |
|---|---|
| `send -- <text>` | send a message; `send -- /swarm …` sends a slash command |
| `queue -- <text>` | queue a message behind the running turn |
| `answer <id>@<rev> <option>` | answer a waiting approval or question |
| `pause <run>` / `continue <run>` | pause or continue a run |
| `stop <run>` | stop a run |
| `retry <run>@<rev>` | retry a failed run |
| `stop-agent <run> <agent>@<rev>` | stop one agent |
| `go conversation <id>` | switch to another conversation |
| `activity` | the activity view |
| `inspect <run> [overview\|agents\|timeline\|changes]` | one view of a run |
| `detail <ref>`, `detail next`, `detail retry` | the full text of an item |
| `back` | back from a detail view |
| `detach` | leave the session |
| `help` | the command list |

## Holding stdin open

The session ends when standard input ends. A command list that ends right after `send` therefore closes before the answer arrives. Keep stdin open for as long as you want to see output, or end the list with `detach` once you have what you need:

```sh
printf 'send -- inspect this project\ndetach\n' | {{cmd}} --plain
```

```sh
{ echo 'send -- list the failing tests'; sleep 120; echo detach; } | {{cmd}} --plain
```

## NDJSON output

`--ndjson` (only with `--plain`) prints one JSON object per output record instead of text lines:

```sh
{{cmd}} --plain --ndjson < commands.txt > session.ndjson
```

The record format is not documented yet and may change between releases.

<!-- capture: cli/plain-session | a plain session in a pipe: the "not a terminal" notice, a sent message, streamed answer lines and the detach line | 100x24 -->

<!-- source: C:README.md:47-61, C:README.md:166-168, C:rel/overlays/bin/swarmcode:38-40, C:rel/overlays/bin/swarmcode:191-193, C:rel/overlays/bin/swarmcode:259-265, C:AGENTS.md:260, C:apps/swarm_code_cli/lib/swarm_code_cli/plain/session.ex:494-498, C:apps/swarm_code_cli/lib/swarm_code_cli/plain/command.ex:171 -->
