---
title: Environment variables
description: The environment variables ncode reads, what each one does, which win over settings, and the older names that still work.
---

Most of {{product}} is set up in [Settings](/docs/cli/settings/). Environment variables are for the first run on a new Mac, for a single launch, and for scripts.

> **Note** Every `{{env_prefix}}…` variable below also works under its older name with `{{old_env_prefix}}` in front (`{{old_env_prefix}}MODEL`, `{{old_env_prefix}}THEME`, …). When both are set, the `{{env_prefix}}` one wins.

## Provider (first run only)

These create a provider only when the database has **no usable provider** yet, and only when a model and an endpoint are given; a key alone does nothing. Afterwards they are ignored: the providers in Settings decide, and environment variables never add providers or change a conversation's model. See the [Quickstart](/docs/cli/quickstart/#from-the-environment).

| Variable | Meaning |
|---|---|
| `{{env_prefix}}PROVIDER` | `openai` (the default, for any OpenAI-compatible endpoint) or `anthropic` |
| `{{env_prefix}}MODEL` | the model id; `OPENAI_MODEL` or `ANTHROPIC_MODEL` also work |
| `{{env_prefix}}BASE_URL` | the endpoint; OpenAI-compatible URLs end in `/v1`, Anthropic URLs do not. `OPENAI_BASE_URL` or `ANTHROPIC_BASE_URL` also work |
| `{{env_prefix}}API_KEY` | the key; wins over `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`. May be empty for a local server |
| `{{env_prefix}}EFFORT` | the reasoning effort for that first setup (`medium` if unset) |

## Where they are loaded from

`{{cmd}}` uses what you exported in your shell. When no provider key is exported, it also reads `~/.secrets`, or the file named by `{{env_prefix}}ENV_FILE`, but only provider variables, such as `{{env_prefix}}…`, `{{old_env_prefix}}…`, `OPENAI_…` and `ANTHROPIC_…`; a GitHub, npm or other token in the same file never reaches `{{cmd}}`. An exported key, even an empty one, skips the file.

| Variable | Meaning |
|---|---|
| `{{env_prefix}}ENV_FILE` | the shell file to read instead of `~/.secrets` |

## Session

| Variable | Meaning | Wins over |
|---|---|---|
| `{{env_prefix}}CONVERSATION` | `latest` (default), `new`, or a conversation id | Settings → Session & startup; the flags `--new`, `--continue` and `--resume` win over it |
| `{{env_prefix}}THEME` | `dark` or `light` | `/theme` and the desktop app's mode |
| `{{env_prefix}}MOUSE` | `0` turns wheel scrolling off, `1` on | `/mouse` |
| `{{env_prefix}}KEYMAP` | `vim` for vim keys in the composer | Settings → Keys & input |
| `{{env_prefix}}ASCII` | `1` draws plain ASCII glyphs | Settings → Appearance |
| `{{env_prefix}}SHELL` | the shell agents' commands run in | Settings → Agents & limits → Shell |

The older name of `{{env_prefix}}SHELL` is `{{old_env_prefix}}CODE_SHELL`.

## Standard variables

| Variable | Meaning |
|---|---|
| `NO_COLOR` | a monochrome screen |
| `VISUAL`, `EDITOR` | the editor [[Ctrl]]+[[X]] opens (else `vi`) |
| `TERM`, `COLORTERM` | which glyph set the terminal gets (see [Terminal, themes and mouse](/docs/cli/terminal/)) |

## Not used by `{{cmd}}`

`{{old_env_prefix}}PROJECT_ROOT` is ignored: `{{cmd}}` opens the directory you name, or the one you run it from, so a value left in `~/.secrets` does not open one project from everywhere.

<!-- source: C:README.md:13-18, C:README.md:29-37, C:README.md:179-203, C:rel/overlays/bin/swarmcode:46-62, C:rel/overlays/bin/swarmcode:206-222, C:apps/swarm_code_daemon/lib/swarm_code/daemon/service/session_configuration.ex:24,196-218, C:apps/swarm_code_daemon/lib/swarm_code/daemon/runtime/configuration.ex:11-17, C:docs/settings.md:101,127-129,150-153,161, C:apps/swarm_code_core/lib/swarm_code/settings/registry/limits.ex:171-177 -->
<!-- notes: post-rename: ncode/A rel/overlays/bin/ncode:46-60 (NCODE_* help, SWARM_* still work, NCODE wins) and :89-100 (NCODE_X copied over SWARM_X for MODEL BASE_URL API_KEY PROVIDER EFFORT CONVERSATION KEYMAP ASCII COMPANION THEME MOUSE APPROVAL ENV_FILE, CONFIG_DIR->CODE_CONFIG_DIR, SHELL->CODE_SHELL). Left out: COMPANION (visual companion out, D13), APPROVAL (unsaved live launcher only), CONFIG_DIR (moves the global folder away from the desktop app's), MODEL_OVERRIDE, RELEASE_TUI, USER_UMASK (internal). The ~/.secrets loader passes SWARM_/NCODE_/OPENAI_/ANTHROPIC_ (ncode/A scripts/dev/load_provider_env.sh); the page says "such as". -->
