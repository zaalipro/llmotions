### What an agent can do

Agents act only through tools. Each tool call is its own step you can watch, and file tools are confined to the project folder.

| Group | Tools | Notes |
|---|---|---|
| Read | `read_file`, `list_dir`, `find_files`, `grep`, `lsp` | `grep` and `find_files` use ripgrep when `rg` is installed |
| Write | `write_file`, `edit_file`, `edit_files`, `move_file`, `delete_file` | a snapshot of each file is taken before it changes; `edit_files` changes several files all or nothing |
| Run | `run_command` | a command still running after 10 seconds moves to the background, where it can be checked or stopped |
| Git | `git_status`, `git_diff`, `git_log`, `git_commit` | |
| Web | `web_search`, `web_fetch` | search uses the engines you enabled, in your order |
| Memory | `remember` | adds a dated line to the project's memory file |
| Team | `spawn_agent`, `message_agent`, `inbox`, `wait_for_message`, `agent_result`, `integrate_agent`, `start_swarm` | sub-agents, messages between agents, merging an isolated agent's changes |
| Ask | `ask_user` | the assistant and a lead may ask you a question; workers may not |
| Plans | `submit_plan`, `write_spec` | only in judged (consensus) runs |
| Workflows | `workflow_list`, `workflow_smoke_check`, `workflow_save`, `workflow_run`, `workflow_control` | only the top-level assistant |
| MCP | every tool of every enabled MCP server | per-tool switches let you turn single tools off |

`run_command` keeps up to 160,000 characters of output by default (an agent may ask for up to 512,000). Whether a write or a command needs your approval depends on the project's approval mode.

<!-- source: D:lib/swarm_code/tools.ex:12-60, D:lib/swarm_code/tools/run_command.ex:26,628-632,697-703, D:lib/swarm_code/tools/background_procs.ex:1-30, D:lib/swarm_code/checkpoints.ex:1-7, D:lib/swarm_code/mcp/server.ex:21 -->
