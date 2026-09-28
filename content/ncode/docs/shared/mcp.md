### MCP servers

MCP (Model Context Protocol) servers add their tools to the agents. {{product}} supports two transports:

| Transport | What you give it |
|---|---|
| stdio (a local process) | a command, its arguments, and environment variables (`KEY=VALUE`) |
| http (streamable HTTP) | a URL and request headers (`Name: value`) |

A server is either **global** (every project) or scoped to **one project**. It can be switched off without deleting it, and each of its tools has its own switch: a tool you turn off is not offered to any agent. The environment variables and headers you enter are stored like your other keys.

A tool the server marks as read-only is treated like a read and never asks. Every other MCP tool is treated like a shell command: blocked in Read-only, asked about in Auto, allowed in Full access.

<!-- source: D:lib/swarm_code/mcp/server.ex:12-34, D:lib/swarm_code_web/live/settings_live.html.heex:1725-1785, D:lib/swarm_code/mcp.ex:226-230, D:lib/swarm_code/tools/ref.ex:58-59, D:lib/swarm_code/engine/policy.ex:16-41 -->
