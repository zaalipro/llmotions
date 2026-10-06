---
title: Providers, models and web search
description: Add Anthropic or OpenAI-compatible endpoints with your own key, choose models per role, set reasoning effort, prices and budget, and set up web search engines.
---

{{product}} works with the model providers you add. You need at least one, with your own API key: Anthropic, or any endpoint with an OpenAI-compatible API (OpenAI, OpenRouter, DeepSeek, a local Ollama or LM Studio, and many more).

{{> shared/providers}}

## Adding a provider

1. Open **Settings → Providers & models** and click **Add provider**.
2. Fill in **Name**, **Kind**, **Base URL** and **API key** (click **Show** to check what you pasted).
3. Optionally list **Models (one per line)** and a **Default model**; you can also fetch them in the next step.
4. For an Anthropic provider, **Server-side fallback on refusal** is on by default: when the API declines a request, it answers with its recommended substitute model instead of an empty reply.
5. Click **Save provider**.

| Service | Kind | Base URL |
|---|---|---|
| Anthropic | Anthropic | `https://api.anthropic.com` |
| OpenAI | OpenAI-compatible | `https://api.openai.com/v1` |
| OpenRouter | OpenAI-compatible | `https://openrouter.ai/api/v1` |
| DeepSeek | OpenAI-compatible | `https://api.deepseek.com/v1` |
| Ollama on this Mac | OpenAI-compatible | `http://localhost:11434/v1` |
| LM Studio on this Mac | OpenAI-compatible | `http://localhost:1234/v1` |

For an OpenAI-compatible service, the base URL is the part before `/chat/completions` in its documentation.

## Fetching models

Click **Fetch models** on a provider's row, or **Fetch all models from endpoints** at the top, to ask each endpoint for its model list. It is also the quickest test of a key: if the list arrives, the key works. If it fails, the endpoint's error is shown, with your key removed from it.

Deleting a provider asks first; conversations that used it fall back to the default model.

## Default models

**Settings → General → Defaults** sets the model each role starts with: **Chat model**, **Worker model**, **Validator model**, **Default scheduled model**, **Default workflow model** and **Implementer model (consensus)**, plus a default effort for each. Click **Save defaults**. The research roles have their own pickers under **Deep research**.

**Worker model** is the model the agents a conversation starts use (swarm sub-agents, mission workers, workflow agents without a model of their own). **Validator model** is the one that checks a mission's work; leave it blank (**Same as main model**) to use the conversation's main model. A conversation can override its chat, worker and validator models from the composer's model chooser; the validator row shows in Ultra mode ([Ultra missions](/docs/desktop/missions/#the-models)).

## Effort levels per provider

Click **Efforts** on a provider's row to edit which effort levels it offers and how each one reaches its API, for the whole provider or per model. Leave it alone to use the built-in levels for the provider's kind.

## Prices, usage and budget

- **Settings → Pricing** holds a price per million tokens for each model: input, output, cache read and cache write, plus its context window. With prices set, every run, agent and conversation shows what it cost.
- **Usage history** in the rail shows spend over the last 7, 30 or 90 days, run by run.
- **Settings → Budget → Monthly budget (USD)** is a target the usage bar fills against. Nothing stops when it is reached.

![Usage history for 30 days with $15.14 of a $30.00 monthly budget and run costs.](/assets/shots/desktop/providers-usage.webp)

## Web search {#web-search}

{{> shared/web-search}}

### Setting up a search engine

1. Get an API key from one of the engines (Tavily, Exa, Brave or Serper).
2. Open **Settings → Deep research**. The **Search providers** block lists every engine and reader.
3. On the engine's row, paste the key, switch it on and save.
4. Use the up and down arrows to set the order engines are tried in.

A reader (Jina or Firecrawl) is optional: agents read pages directly without one.

<!-- source: D:lib/swarm_code_web/live/settings_live.html.heex:57-210,230-350,750-898,899-998,1660-1700, D:lib/swarm_code_web/live/settings_live.ex:892-904,2612, D:lib/swarm_code/providers.ex:150-162,198-230, D:lib/swarm_code/llm/anthropic.ex:94,224-230, D:lib/swarm_code/llm/openai.ex:90,439, D:lib/swarm_code/providers/provider.ex:18-33, D:lib/swarm_code_web/live/history_live.ex:1-23, D:lib/swarm_code/search.ex:18-34,144-158; OpenRouter, DeepSeek, Ollama and LM Studio URLs: C:apps/swarm_code_core/lib/swarm_code/settings/registry/actions.ex:11-70 -->
