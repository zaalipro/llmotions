---
title: Works with the desktop app
description: The CLI and the desktop app share one database on your Mac. How to switch between them, what only the app does, and how the two differ.
---

The `{{cmd}}` command and the {{product}} desktop app are two ways into the same work. If you use both on one Mac, this page is the one to read.

{{> shared/together}}

## When `{{cmd}}` refuses to start

With the app open, every `{{cmd}}` command except `--version` and `--help` stops at once with exit code `3`:

```term
The {{product}} app is open, and only one of them can use your conversations at a time.
Quit the {{product}} app, then run {{cmd}} again.
```

Quit the app ([[⌘Q]], closing its window is not enough), then run the command again. To continue a conversation you started in the app, open it with `/resume` in the session, or `{{cmd}} --resume <conversation-id>`.

On the other side, reopen the app only after you have quit every `{{cmd}}` session ([[Ctrl]]+[[C]] twice).

## Upgrading together

Update both on the same day. The database format changes with the app, and `{{cmd}}` refuses a database it does not understand rather than risk it:

| `{{cmd}}` says | Do this |
|---|---|
| `This {{product}} database needs an upgrade that only the {{product}} app makes.` | open the app once, quit it, run `{{cmd}}` again |
| `This {{product}} database was upgraded by a newer {{product}} app than this {{cmd}} supports.` | update `{{cmd}}`: re-run the [installer](/docs/cli/install/#update) |

Neither message changes anything in the database.

## How the two differ

| Topic | Desktop app | `{{cmd}}` |
|---|---|---|
| Interface | a native window | full-screen terminal, plain line mode, headless `-p` |
| Scheduled tasks | fire on their schedule | can be created, edited and run now; never fire |
| Storage retention | applied once a day | the settings are shared; not applied |
| `/resume` | resumes the last stopped run | opens a conversation (the run is `/resume-run`) |
| Model and approvals | controls in the composer | `/model`, `/swarm_model`, `/approval`, `/trust` |
| Answering approvals | buttons | the keys `y Y A d D n` |
| Provider presets | enter the details yourself | presets for Anthropic, OpenAI, OpenRouter, DeepSeek, Ollama, LM Studio and any OpenAI-compatible endpoint |
| MCP `.mcp.json` import | no | yes |
| Settings from scripts | no | [`{{cmd}} config`](/docs/cli/config/) |
| Themes | several themes, each dark and light | dark and light, with an accent colour |

The desktop documentation has its own page on [using the app with the CLI](/docs/desktop/cli/).

<!-- source: C:apps/swarm_code_cli/lib/swarm_code_cli/release/persisted_session.ex:973-976,990-1003, C:apps/swarm_code_daemon/lib/swarm_code/daemon/schema/refusal.ex:12-52, C:README.md:66-68, C:README.md:111-118, C:AGENTS.md:123-137, C:apps/swarm_code_daemon/lib/swarm_code/daemon/boot.ex:14, C:apps/swarm_code_daemon/lib/swarm_code/domain/runtime.ex:4, C:docs/settings.md:67-83,164-169, C:apps/swarm_code_core/lib/swarm_code/settings/registry/actions.ex:8-80, C:apps/swarm_code_core/lib/swarm_code/commands.ex:22-23,38-42, D:lib/swarm_code_web/components/chat.ex:66 -->
