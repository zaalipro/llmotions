### Where your keys are kept

Provider keys, search-engine keys and the environment variables or headers you give an MCP server are stored in the local {{product}} database on your Mac, `{{db_file}}`. They are not stored in the macOS Keychain. <!-- allow: Keychain -->

What that means for you:

- Protect the database like the rest of your home folder: it holds your keys. Anyone who can read your files can read them.
- The provider list shows a key only in masked form, and when fetching a model list fails, the key is removed from the endpoint's error text before you see it.
- Commands an agent runs get a cleaned environment by default: variables whose names look like secrets are hidden from them. `GITHUB_TOKEN` and `GH_TOKEN` are kept unless you change the list.
- Deleting a provider or an MCP server deletes its stored secrets with it.

<!-- source: D:lib/swarm_code/providers/provider.ex:17,22, D:lib/swarm_code/search/search_provider.ex:19, D:lib/swarm_code/settings/setting.ex:32,110-111, D:lib/swarm_code/mcp/server.ex:11,16,18, D:lib/swarm_code/providers.ex:158-160, D:lib/swarm_code_web/live/settings_live.ex:2612, D:config/runtime.exs:21-29, D:lib/swarm_code_web/live/settings_live.html.heex:1567-1582 -->
