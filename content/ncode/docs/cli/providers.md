---
title: Providers and models
description: Add your own model providers from presets, paste keys, fetch model lists, choose the model and effort per role and per conversation, and track cost.
---

{{> shared/providers}}

## Adding a provider in the terminal

Open Settings at **Providers** (`{{cmd}} settings providers`, or [[F2]] in a session) and add one from a preset. The preset fills in the kind and the base URL:

| Preset | Kind | Base URL |
|---|---|---|
| Anthropic | Anthropic | `https://api.anthropic.com` |
| OpenAI | OpenAI-compatible | `https://api.openai.com/v1` |
| OpenRouter | OpenAI-compatible | `https://openrouter.ai/api/v1` |
| DeepSeek | OpenAI-compatible | `https://api.deepseek.com/v1` |
| Ollama | OpenAI-compatible | `http://localhost:11434/v1` |
| LM Studio | OpenAI-compatible | `http://localhost:1234/v1` |
| Other | OpenAI-compatible | the URL you enter |

The new provider starts as a draft. Paste the key, then press [[Ctrl]]+[[S]]: {{product}} creates it and tests the key against the endpoint. A provider on your own machine or private network (Ollama, LM Studio, a server on your LAN) needs no key.

Then **fetch models**: {{product}} reads the endpoint's model list and shows what is new or gone before it changes anything. Each provider also has its own list of effort levels.

From a shell, the same steps are:

```sh
{{cmd}} config record add provider --preset openrouter
printf '%s' "$OPENROUTER_API_KEY" | {{cmd}} config secret provider:OpenRouter --stdin
{{cmd}} config set models.chat OpenRouter/<model-id>
```

The record takes the preset's name (`Anthropic`, `OpenRouter`, …) unless you give `--name`. See [`{{cmd}} config`](/docs/cli/config/#records).

<!-- capture: cli/settings-providers | Settings at Providers: an OpenRouter provider with its key row masked, the fetched model list with two new models marked, the effort levels row | 120x40 -->

## Choosing models

| Where | Setting or command | Scope |
|---|---|---|
| Default chat model | **Chat model** (`models.chat`) in Models & effort | every new conversation |
| Default sub-agent model | **Sub-agent model** (`models.sub_agent`) | agents started from now on |
| Other roles | `models.scheduled`, `models.workflow`, `models.implementer` | their runs |
| This conversation | `/model`, `/swarm_model` | this conversation, saved |
| This session only | `{{cmd}} --model <model>` or `--model provider/model` | until you quit or use `/model`; nothing is saved |

Until you choose, the chat and sub-agent models are those of the first provider with a key. Effort works the same way: **Default effort** and **Sub-agent effort** in Settings, `/effort` and `/swarm_effort` in a conversation (see [Modes and run types](/docs/cli/modes/#model-and-effort)).

## Cost and budget

- `/cost` shows the tokens and cost of this conversation, by model.
- **Usage** in the [[Ctrl]]+[[P]] palette opens the usage view.
- Settings → **Pricing** holds the price per million tokens of each model.
- Settings → **Budget & usage** sets the monthly budget (`budget.monthly_usd`).

## Setting a provider from the environment

On a Mac where the database has no usable provider yet, the first launch can create one from `{{env_prefix}}PROVIDER`, `{{env_prefix}}MODEL`, `{{env_prefix}}BASE_URL` and `{{env_prefix}}API_KEY`. After that, environment variables never add providers or change a conversation's model. See the [Quickstart](/docs/cli/quickstart/#from-the-environment).

<!-- source: C:apps/swarm_code_core/lib/swarm_code/settings/registry/actions.ex:8-80, C:apps/swarm_code_daemon/lib/swarm_code/daemon/service/settings/providers.ex:1062-1089, C:apps/swarm_code_daemon/lib/swarm_code/daemon/service/session_configuration.ex:107-121, C:README.md:13-18, C:README.md:155-158, C:README.md:223-224, C:README.md:240-241, C:README.md:255-258, C:README.md:264-272, C:docs/settings.md:15-37,171-175, C:apps/swarm_code_core/lib/swarm_code/commands.ex:19-23,44, C:AGENTS.md:45-51 -->
