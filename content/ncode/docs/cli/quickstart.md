---
title: Quickstart
description: From install to a first answer: add your own provider key, open a project, trust it, send a message, approve a command, quit and come back.
---

This page takes you from a fresh install to a first finished task in a few minutes. You need `{{cmd}}` [installed](/docs/cli/install/) and a key for a model provider: Anthropic, OpenAI, OpenRouter, DeepSeek, or any other OpenAI-compatible endpoint. A local server such as Ollama or LM Studio works without a key.

## Add a model provider

{{product}} ships with no key of its own. Until you add a provider that can answer, a session does not start and says:

```term
No model provider is set up yet.
Run '{{cmd}} settings providers' to add one, or set {{env_prefix}}MODEL, {{env_prefix}}BASE_URL and {{env_prefix}}API_KEY in ~/.secrets (the older {{old_env_prefix}}* names still work).
```

There are two ways to add one.

### In Settings

```sh
{{cmd}} settings providers
```

This opens the settings screen at **Providers**, even with no provider set up.

1. Add a provider and pick a preset: **Anthropic**, **OpenAI**, **OpenRouter**, **DeepSeek**, **Ollama**, **LM Studio**, or **Other** for any OpenAI-compatible endpoint. The preset fills in the kind and the base URL.
2. Paste your key. It is never shown: the row reads `●●●●●●●● set · ends 4f2a`.
3. Press [[Ctrl]]+[[S]]. {{product}} creates the provider, stores the key and tests the connection. A failed test shows on the provider's row; fix the key and test again.
4. Fetch the model list and pick the model you want to chat with.

The same from a shell, for example with Anthropic (the key is read from stdin, so it never lands in your shell history):

```sh
{{cmd}} config record add provider --preset anthropic
printf '%s' "$ANTHROPIC_API_KEY" | {{cmd}} config secret provider:Anthropic --stdin
{{cmd}} config set models.chat Anthropic/<model-id>
```

<!-- capture: cli/quickstart-providers | Settings at Providers with one Anthropic provider added from its preset, its key row masked "●●●●●●●● set · ends 4f2a" and the test result; no other provider rows | 120x40 -->

### From the environment (first run only) {#from-the-environment}

If the database has no usable provider yet, the first launch can create one from environment variables and says that it did. Two of them are required, the model and the endpoint; the kind defaults to `openai`, and the key may be empty for a local server.

```sh
{{env_prefix}}PROVIDER=anthropic \
{{env_prefix}}MODEL=<model-id> \
{{env_prefix}}BASE_URL=https://api.anthropic.com \
{{env_prefix}}API_KEY="$ANTHROPIC_API_KEY" \
{{cmd}}
```

- `{{env_prefix}}PROVIDER` is `anthropic` or `openai` (the default, for any OpenAI-compatible endpoint).
- OpenAI-compatible URLs end in `/v1` (`https://api.openai.com/v1`); Anthropic URLs do not.
- A local server may use an empty key: `{{env_prefix}}API_KEY=`.
- Setting only a key does nothing: without a model and an endpoint no provider is created.

Instead of exporting them, you can put the same lines in `~/.secrets` (one `NAME=value` per line): `{{cmd}}` reads that file when no key is exported. After the first run these variables are ignored: the providers in Settings decide. The older `{{old_env_prefix}}…` names are still read. See [Environment variables](/docs/cli/env/#where-they-are-loaded-from).

## Open a project

```sh
cd ~/dev/app
{{cmd}}
```

`{{cmd}}` opens the folder you run it from (or the one you name, `{{cmd}} ~/dev/app`) as the project, in full screen, with the composer ready for typing. It continues the project's latest conversation; `{{cmd}} --new` starts a fresh one.

<!-- capture: cli/quickstart-first-screen | the session on a new project: empty transcript, composer with the cursor, the status line reading "read-only" | 120x40 -->

## Trust the project

A project you open for the first time is **read-only**: agents can read and search, but not write files or run commands, and the project's `AGENTS.md` is not read. The mode is always on the status line.

When you trust the code in the folder, type:

```text
/trust
```

The project moves to **auto**, and the chat says `Approvals: read-only → auto`. In auto, file edits and safe commands such as `ls` or `git status` run by themselves; other commands ask you first. [Approvals and trust](/docs/cli/approvals/) explains the modes.

## Ask something

Type a request and press [[Enter]]:

```text
Add a --verbose flag to the CLI parser and a test for it.
```

The answer streams into the transcript. Each file the assistant reads or edits and each command it runs is one row you can open with [[Enter]] in select mode ([[Ctrl]]+[[T]]). [[Esc]] stops the turn at any time; your draft stays.

## Approve a command

When the assistant wants to run a command that auto mode does not allow on its own, a card opens above the composer with the command. Answer with one letter:

| Key | Answer |
|---|---|
| `y` | allow it once |
| `Y` | allow it for the rest of this run |
| `A` | always allow this command family in this project |
| `d` | deny it |
| `D` | deny it and stop the run |
| `n` | leave it and go to the next thing waiting |

The letters answer only while your draft is empty, so a sentence you are typing never answers a card by accident.

<!-- capture: cli/quickstart-approval | the approval card above the composer with a three-line command and the keys y Y A d D n | 120x40 -->

## Quit and come back

Press [[Ctrl]]+[[C]] twice within a second and a half. If runs are still working, `{{cmd}}` asks first. After the full screen closes, a short summary lists the runs it stopped and how to reopen the conversation:

```sh
{{cmd}} --resume <conversation-id>
```

Plain `{{cmd}}` in the same folder also reopens the latest conversation. Next: [the session screen](/docs/cli/session/) and [the composer](/docs/cli/composer/).

<!-- source: C:README.md:13-18, C:README.md:236-238, C:README.md:255-258, C:README.md:264-272, C:README.md:188-193, C:README.md:205-208, C:README.md:103-126, C:README.md:155-156, C:AGENTS.md:45-55, C:AGENTS.md:171-181, C:AGENTS.md:127-129, C:apps/swarm_code_core/lib/swarm_code/settings/registry/actions.ex:8-80, C:apps/swarm_code_cli/lib/swarm_code_cli/release/config_command.ex:43-70, C:apps/swarm_code_cli/lib/swarm_code_cli/release/persisted_session.ex:1034-1040, C:apps/swarm_code_cli/lib/swarm_code_cli/ui/settings/sections/providers.ex:8-11,1266-1273, C:scripts/dev/load_provider_env.sh:5-16,26-47, C:apps/swarm_code_daemon/lib/swarm_code/daemon/service/session_configuration.ex:24,98-121,196-218, C:apps/swarm_code_daemon/lib/swarm_code/daemon/runtime/configuration.ex:9-17,37-54, C:apps/swarm_code_daemon/lib/swarm_code/daemon/service/settings/providers.ex:1062-1089, C:rel/overlays/bin/swarmcode:46-50, C:docs/settings.md:15, D:lib/swarm_code/projects.ex:175-191 -->
<!-- notes: post-rename launcher help lists NCODE_MODEL/BASE_URL/API_KEY/PROVIDER (ncode/A rel/overlays/bin/ncode:46-60, NCODE_X copied over SWARM_X at :89-100). The llmotions preset and seeded row are deliberately not mentioned (owner decision). -->
