---
title: Headless runs
description: Run one turn from a script with ncode -p, read the prompt from stdin, get JSON back, continue a conversation, and handle approvals and exit codes.
---

`{{cmd}} -p` runs one turn without the full screen: it sends your prompt, prints the answer as it streams, and exits. Use it from scripts, shell aliases and editor tasks.

## One prompt

```sh
{{cmd}} -p "summarise the open TODOs in lib/" > todos.md
```

The project is the current folder, or the one you name: `{{cmd}} ~/dev/app -p "…"`. `-p` also has the long forms `--prompt` and `--print`.

Each `-p` run starts a **new conversation**, so it does not carry the context of the one you were working in. The conversation is saved like any other, and you can open it later in the full screen.

## Reading the prompt from stdin

`-p -` reads the prompt from standard input:

```sh
{{cmd}} -p - < review-request.md
git diff | {{cmd}} -p - --model Anthropic/<model-id>
```

`--model` answers with another model for this run only; nothing is written to your providers or the conversation.

## JSON output

`--json` prints one JSON object at the end instead of the streamed answer:

| Field | Meaning |
|---|---|
| `conversation_id` | the conversation the run belongs to |
| `run_id` | the run |
| `state` | how the run ended |
| `text` | the answer |
| `error` | what went wrong, if anything |
| `denied` | the approvals that were denied because nobody could give them |
| `exit_code` | the same code the command exits with |

```sh
{{cmd}} -p "run the tests and fix what fails" --json | jq -r '.state, .text'
```

## Continuing a conversation

Add `-c` (`--continue`) to continue the project's latest conversation, or `--resume <conversation-id>` for a given one:

```sh
{{cmd}} -p "now add a test for the empty case" -c
```

`--resume` needs the whole conversation id; the id is in the JSON output and in the summary printed when you quit a session.

## Approvals and questions

A headless run has nobody to ask, so the project's [approval mode](/docs/cli/approvals/) decides everything:

- whatever the mode allows runs;
- anything that would still need a person is **denied**, and a line on stderr says what (in full access, the line says that nothing asks);
- a question from an agent **stops** the run.

A new project is read-only until you trust it, so in a project you have never opened, a headless run can read but not change anything. Open it once with `{{cmd}}` and type `/trust` first. From a script, `{{cmd}} config set project.trusted on --project ~/dev/app` does the same, once {{product}} has opened the folder at least once (a `-p` run counts); before that, `config` answers that the folder is not a project yet.

## Exit codes

| Code | Meaning |
|---|---|
| `0` | the run finished |
| `1` | the run failed or was stopped |
| `2` | usage: a flag or value the command does not accept |
| `3` | startup refused: another session or the desktop app holds the database, no provider is set up, or the database is from an incompatible version; one line on stderr says which |

Usage mistakes are caught before anything starts: `--json` goes only with `-p`, `-p` and `--plain` do not go together, and `-p` needs a prompt that is not empty.

## A script example

```sh
#!/bin/sh
cd ~/dev/app || exit 1
if {{cmd}} -p "update CHANGELOG.md for the commits since the last tag" --json > run.json; then
  jq -r .text run.json
else
  code=$?
  echo "the run did not finish (exit $code)" >&2
  exit "$code"
fi
```

> **Note** The database is shared with the desktop app and with interactive sessions, so a headless run exits with code `3` while either of them is open. See [Works with the desktop app](/docs/cli/desktop/).

<!-- source: C:README.md:155-177, C:rel/overlays/bin/swarmcode:29-44, C:rel/overlays/bin/swarmcode:171-199, C:rel/overlays/bin/swarmcode:224-230, C:rel/overlays/bin/swarmcode:244-246, C:AGENTS.md:40, C:AGENTS.md:45-51, C:AGENTS.md:127-129, C:docs/settings.md:108, C:docs/research/2026-09-23-pass70-outcome.md:47, C:apps/swarm_code_core/lib/swarm_code/settings/registry/project.ex:22-32, C:apps/swarm_code_cli/lib/swarm_code_cli/release/config_command.ex:470-496, C:apps/swarm_code_daemon/lib/swarm_code/daemon/service/settings/headless.ex:20-28, C:apps/swarm_code_daemon/lib/swarm_code/daemon/service/settings/values.ex:978-992, C:apps/swarm_code_daemon/lib/swarm_code/domain/projects.ex:145-150, C:apps/swarm_code_daemon/lib/swarm_code/daemon/service/session_selection.ex:65-69, C:apps/swarm_code_daemon/lib/swarm_code/daemon/service/session_configuration.ex:137-160 -->
