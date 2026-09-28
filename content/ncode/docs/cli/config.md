---
title: ncode config
description: Read and change every setting from scripts, dotfiles and SSH (values, providers, search engines, MCP servers, keys) with the checks of the settings screen.
---

`{{cmd}} config` does what the [settings screen](/docs/cli/settings/) does, from a shell: it goes through the same service and the same checks, so a value it accepts is one the screen would accept. `{{cmd}} config help` lists every command.

```sh
{{cmd}} config list --modified
{{cmd}} config set limits.max_agent_depth 3
{{cmd}} config record add provider --preset deepseek
printf '%s' "$DEEPSEEK_KEY" | {{cmd}} config secret provider:DeepSeek --stdin
{{cmd}} config set models.chat DeepSeek/<model-id>
{{cmd}} config search order tavily,exa
```

Every key is listed in the [settings reference](/docs/cli/settings-reference/).

## Reading

| Command | Prints |
|---|---|
| `list [SECTION] [--modified] [--json]` | the settings of every section, or one; `--modified` only those not at their default |
| `get KEY [--json]` | one setting |
| `keys [--json]` | every key binding |
| `path` | where this terminal's settings file (`cli.json`), the log, and the project's config, memory and instruction files are |

## Changing

```sh
{{cmd}} config set KEY VALUE [--project DIR] [--conversation ID|latest] [--expect VALUE]
{{cmd}} config reset KEY [--project DIR] [--conversation ID|latest]
```

Values are typed as in Settings: `on`/`off`, durations such as `30m` or `90s`, `default`, `null`, lists as `a,b,c`, models as `provider/model`, colours as `#RRGGBB`.

- `--project DIR` changes a project setting for that project (by default, the current folder's).
- `--conversation ID` (or `latest`) changes a setting of one conversation.
- `--expect VALUE` changes the value only if it still is `VALUE`; otherwise the command exits with code `4`, "changed elsewhere". Use it when two scripts or a person may change the same setting.

`reset` puts a setting back to its default.

## Records: providers, search engines and MCP servers {#records}

Providers, search engines and MCP servers are records with fields of their own. `KIND` is `provider`, `search_provider` or `mcp_server`.

```sh
{{cmd}} config records provider
{{cmd}} config record get provider:Anthropic
{{cmd}} config record set provider:Anthropic.base_url https://api.anthropic.com
{{cmd}} config record add provider --preset anthropic [--name "Work Anthropic"]
{{cmd}} config record add mcp_server docs --http https://mcp.example.com/mcp
{{cmd}} config record add mcp_server files --stdio npx -y @modelcontextprotocol/server-filesystem .
{{cmd}} config record delete provider:Anthropic --yes
```

Provider presets are `anthropic`, `openai`, `openrouter`, `deepseek`, `ollama`, `lmstudio` and `other` (see [Providers and models](/docs/cli/providers/)).

## Secrets

Keys are read from standard input only, so they never land in your shell history or the process list. Naming a key as a setting, as in `{{cmd}} config set provider:Anthropic.api_key …` or an MCP server's `env.` or `headers.` slot, is refused with exit code `2` and a sentence that points you to `{{cmd}} config secret … --stdin`.

```sh
printf '%s' "$ANTHROPIC_API_KEY" | {{cmd}} config secret provider:Anthropic --stdin
printf '%s' "$TAVILY_KEY" | {{cmd}} config secret search_provider:tavily --stdin
printf '%s' "$GITHUB_TOKEN" | {{cmd}} config secret mcp_server:github.env.GITHUB_PERSONAL_ACCESS_TOKEN --stdin
printf '%s' "$TOKEN" | {{cmd}} config secret mcp_server:docs.headers.Authorization --stdin
```

Run in a terminal without a pipe, `secret … --stdin` asks you to paste the key and does not echo it. A provider key is tested against the endpoint before it is saved; `--no-test` skips the test.

## Search engines

```sh
{{cmd}} config search enable tavily
{{cmd}} config search disable brave
{{cmd}} config search order tavily,exa,brave
```

Engines are tried in this order; see [Web search](/docs/cli/search/).

## MCP servers

```sh
{{cmd}} config mcp toggle docs
{{cmd}} config mcp reconnect docs
```

## Export and import

```sh
{{cmd}} config export settings.json
{{cmd}} config import settings.json            # changes nothing yet
{{cmd}} config import settings.json --apply    # imports it
```

`export` writes your settings to a file you can keep in dotfiles or move to another Mac. `--no-terminal` leaves out this terminal's own settings, `--no-project` the project's, `--include-records` adds providers, search engines and MCP servers. Keys are never exported.

## Doctor

```sh
{{cmd}} config doctor
```

checks the files and the environment {{product}} relies on (the same checks as Settings → Files & environment); `--json` for scripts.

## While a session is open

While a `{{cmd}}` session is open, settings kept in the shared database can be changed only from that session: `config set` on one of them exits with code `3` and names the process that holds the database. This terminal's own settings (theme, panel, mouse and the other `terminal.*` keys, kept in `cli.json`) can always be set.

While the desktop app is open, `{{cmd}} config` refuses with code `3` like every other `{{cmd}}` command; see [Works with the desktop app](/docs/cli/desktop/).

## Exit codes

| Code | Meaning |
|---|---|
| `0` | done |
| `1` | failed |
| `2` | usage, or a value the setting does not accept |
| `3` | startup refused (the database is held by a session or the app) |
| `4` | changed elsewhere (`--expect` did not match) |

<!-- source: C:apps/swarm_code_cli/lib/swarm_code_cli/release/config_command.ex:38-75, C:apps/swarm_code_cli/lib/swarm_code_cli/release/config_command.ex:79-82, C:apps/swarm_code_cli/lib/swarm_code_cli/release/config_command.ex:295-329,308-329,766-768,799-821, C:README.md:255-258, C:README.md:264-281, C:rel/overlays/bin/swarmcode:124-145, C:apps/swarm_code_cli/lib/swarm_code_cli/release/config_command.ex:165,191,230-240,1161-1172, C:docs/settings.md:1-9, C:apps/swarm_code_core/lib/swarm_code/settings/registry/actions.ex:8-70, C:apps/swarm_code_daemon/lib/swarm_code/daemon/service/settings/providers.ex:1062-1089 -->
