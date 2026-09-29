---
title: MCP servers
description: Connect Model Context Protocol servers over stdio or HTTP, scope them to a project, and turn single tools on or off for your agents.
---

MCP servers give agents new tools: a database browser, an issue tracker, a design tool, a company API. {{product}} connects to them and offers their tools to every agent in scope, next to the built-in ones.

{{> shared/mcp}}

## Adding a server

1. Open **Settings → MCP servers** and click **Add MCP server**.
2. Fill in:
  - **Name**, for example `filesystem`.
  - **Transport**: **stdio (local process)** or **http (streamable)**.
  - For stdio: **Command** (for example `npx`), **Arguments (one line, shell-quoted)** and **Environment (KEY=VALUE per line)**.
  - For http: **URL** and **Headers (Name: value per line)**, for example `Authorization: Bearer …`.
  - **Scope**: **Global**, or one of your projects.
3. Save. {{product}} starts or connects to the server and lists its tools.

Example: a stdio server that exposes one folder.

| Field | Value |
|---|---|
| Name | `filesystem` |
| Transport | stdio (local process) |
| Command | `npx` |
| Arguments | `-y @modelcontextprotocol/server-filesystem /path/to/notes` |

![The tavily server card in Settings → MCP servers: ready over http, global, its tools shown as chips with 3 of 5 enabled; tavily_crawl and tavily_research are switched off.](/assets/shots/desktop/mcp-card.webp)

## Managing servers

Each server's card shows its status (ready, connecting, stopped, or the error it reported) and has:

- a switch to turn the whole server on or off;
- **Reconnect**, after you fix a problem or change the server;
- **Edit** and delete (its tools disappear from every agent in scope);
- the tool list: open it and click a tool to switch it off or on. A tool that is off is never offered to an agent;
- **Recent output**: what the server itself reported (for a local server, also what it printed as errors), to see why it does not start.

## Keys and safety

- The environment variables and headers you enter often contain tokens. They are stored in the local database with your other keys; see [Data and privacy](/docs/desktop/privacy/).
- A stdio server is a program running on your Mac with your permissions. Add only servers you trust.
- Tools a server does not mark as read-only need approval like shell commands, unless the project is in Full access.

<!-- source: D:lib/swarm_code/mcp/server.ex:11-34, D:lib/swarm_code/mcp.ex:220-230, D:lib/swarm_code/tools/ref.ex:58-59, D:lib/swarm_code_web/live/settings_live.html.heex:999-1150,1720-1790, D:lib/swarm_code_web/live/settings_live.ex:2199-2202, D:lib/swarm_code_web/live/settings_live.html.heex:1114-1142 -->
