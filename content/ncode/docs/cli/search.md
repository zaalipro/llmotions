---
title: Web search
description: Let agents search the web and read pages: add a search engine with your own key, order the engines, add a reader, and know when fetching asks.
---

{{> shared/web-search}}

## Setting it up in the terminal

Open Settings ([[F2]]) at **Search & web**. The engines are listed in fallback order, each with its key and its switch; the readers are on the same page.

From a shell:

```sh
printf '%s' "$TAVILY_API_KEY" | {{cmd}} config secret search_provider:tavily --stdin
{{cmd}} config search enable tavily
{{cmd}} config search enable exa
{{cmd}} config search order tavily,exa
{{cmd}} config search disable brave
```

The engine names are `tavily`, `exa`, `brave` and `serper`. Keys are read from stdin only, and a key is never shown again: its row reads `●●●●●●●● set · ends …`.

## Fetching local addresses

An agent may read pages on `localhost` or your private network (a dev server, an internal wiki), but in read-only and auto mode each such fetch asks you first, on an [approval card](/docs/cli/approvals/#the-approval-card). Public pages never ask.

<!-- source: C:README.md:241-242, C:README.md:255-257, C:apps/swarm_code_daemon/lib/swarm_code/domain/search.ex:18-22, C:apps/swarm_code_cli/lib/swarm_code_cli/release/config_command.ex:59-60,79-82,184-187,799-811, D:lib/swarm_code/engine/policy.ex:24-29, D:lib/swarm_code/tools/web_fetch.ex:67-90 -->
