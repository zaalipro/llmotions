### Providers

{{product}} talks to the model endpoints you add. It ships with no key of its own: you bring yours.

A provider has:

- a **kind**: *Anthropic* (the Messages API) or *OpenAI-compatible* (any endpoint that speaks the OpenAI chat API: OpenAI itself, OpenRouter, DeepSeek, or a local server such as Ollama or LM Studio);
- a **base URL**, for example `https://api.anthropic.com` or `https://api.openai.com/v1`;
- an **API key** (a local server may not need one);
- its **models**, typed in or fetched from the endpoint's model list, and a default model.

### Models per role

Different kinds of work can use different models. Each role has its own default, and a conversation can still pick its own chat model and the model for the agents it starts (the helper agents; the desktop app calls it the Worker model):

| Role | Used for |
|---|---|
| Chat | the assistant's turns |
| Sub-agent (desktop: Worker) | the agents a swarm, a mission or the assistant starts |
| Scheduled | tasks that run on a schedule |
| Workflow | agents inside workflow runs |
| Implementer | the agent that carries out a judged plan |
| Judge | the reviewer in a judged (consensus) turn; it falls back to the sub-agent (worker) model |
| Research lead, worker and reporter | the three roles of a deep research |

### Reasoning effort

Effort is how hard a model thinks before it answers. The built-in levels are:

| Level | Meaning |
|---|---|
| `low` | fastest |
| `medium` | balanced |
| `high` | deeper reasoning |
| `xhigh` | coding and agentic work |
| `max` | maximum thinking |

A provider, and each of its models, can carry its own list of levels, so the levels you see are the ones your provider offers.

### Pricing and budget

You can enter a price per million input and output tokens (and cache reads and writes) for each model, so every run shows what it cost. A monthly budget is a spend target you watch; nothing is blocked when it runs out.

<!-- source: D:lib/swarm_code/providers/provider.ex:18-33, D:lib/swarm_code/llm/efforts.ex:3-28, D:lib/swarm_code/providers.ex:150-162,198-230, D:lib/swarm_code/settings/setting.ex:19,43-102, D:lib/swarm_code_web/live/settings_live.html.heex:866-870,935-974,1674-1676 -->
