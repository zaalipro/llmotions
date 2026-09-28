---
title: MCP servers
description: Give agents more tools by adding MCP servers - local stdio processes or HTTP endpoints - from Settings or from a script, and switch single tools off.
---

{{> shared/mcp}}

## Adding a server in Settings

Open Settings ([[F2]]) at **MCP servers**. There you can:

- add a **stdio** server (a command, its arguments and `KEY=VALUE` environment variables) or an **HTTP** server (a URL and `Name: value` headers);
- **import** the servers of a `.mcp.json` file, the format other coding tools use;
- switch a server, or single tools of it, on and off;
- **reconnect** a server after you changed or restarted it.

Environment values and headers are masked on screen. Probing a server runs as a task with its seconds shown; `c` cancels it.

<!-- capture: cli/settings-mcp | Settings at MCP servers with one HTTP and one stdio server, the HTTP server's tools listed with one switched off, a header value masked | 120x40 -->

## Adding a server from a script

```sh
{{cmd}} config record add mcp_server docs --http https://mcp.example.com/mcp
printf '%s' "$DOCS_TOKEN" | {{cmd}} config secret mcp_server:docs.headers.Authorization --stdin

{{cmd}} config record add mcp_server files --stdio npx -y @modelcontextprotocol/server-filesystem .
{{cmd}} config record add mcp_server github --stdio github-mcp-server stdio
printf '%s' "$GITHUB_TOKEN" | {{cmd}} config secret mcp_server:github.env.GITHUB_PERSONAL_ACCESS_TOKEN --stdin
```

Header and environment values that are secrets go through `config secret … --stdin`, never the command line. Then:

```sh
{{cmd}} config mcp toggle docs       # switch the server off or on
{{cmd}} config mcp reconnect docs    # reconnect it
{{cmd}} config records mcp_server    # list your servers
```

<!-- source: C:README.md:242-243, C:README.md:255-260, C:apps/swarm_code_cli/lib/swarm_code_cli/ui/settings/sections/mcp.ex:1143-1154, C:apps/swarm_code_cli/lib/swarm_code_cli/release/config_command.ex:52-61,79-82,799-821, D:lib/swarm_code/mcp/server.ex:11-18 -->
