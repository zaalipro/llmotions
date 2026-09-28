### Web search and page reading

Agents search the web with `web_search` and read pages with `web_fetch`. Search needs at least one search engine with your own key; nothing is preconfigured.

- **Engines** answer searches: Tavily, Exa, Brave and Serper.
- **Readers** turn a web page into clean text: Jina and Firecrawl. Without a reader, pages are read directly.

Engines are tried in the order you arrange them. The first enabled engine that returns results answers; an engine that fails or finds nothing hands over to the next one. Each engine has its own key, an optional base URL and an on/off switch.

Reading a page on your own machine or network (`localhost`, private and link-local addresses) is allowed, but asks for approval unless the project is in Full access.

<!-- source: D:lib/swarm_code/search.ex:3-8,18-34, D:lib/swarm_code/search/search_provider.ex:18-22, D:lib/swarm_code/settings/setting.ex:170, D:lib/swarm_code_web/live/settings_live.html.heex:230-307, D:lib/swarm_code/engine/policy.ex:29 -->
