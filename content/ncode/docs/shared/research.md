### Deep research

A deep research answers one question from the web with its own team of agents: a lead plans the angles, workers search and read pages, and a reporter writes the answer with its sources. It runs in the background, so you can keep working while it does.

It needs at least one search engine with a key (see web search).

| Level | Rounds × agents | Use it for |
|---|---|---|
| Fastest | 1 × 4 | a quick answer in minutes |
| Medium (default) | 2 × 3 | most questions |
| High | 3 × 4 | a wider, deeper sweep |
| Ultra | 4 × 10 | the most thorough answer |

Each research produces a Markdown answer (`result.md`) and a rendered HTML report. A **designed** report, a richer HTML page, is built afterwards in the background: by default after every research except Fastest; you can choose after every research, or only when you ask.

### Research settings

| Setting | Default |
|---|---|
| Agents running at once | 10 |
| Pages read per agent | 5 |
| Only pages newer than N days | off |
| Include or exclude domains | none |
| Time limit per agent | 10 minutes, one retry after a timeout |
| A headline after each round | on |
| Lead, worker and reporter models | the defaults, or one each |

<!-- source: D:lib/swarm_code/research/levels.ex:14-46, D:lib/swarm_code/settings/setting.ex:63-97, D:lib/swarm_code/research.ex:15-47, D:lib/swarm_code_web/live/settings_live.html.heex:211-228,457-472 -->
