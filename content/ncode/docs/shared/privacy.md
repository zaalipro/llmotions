### What stays on your Mac

{{product}} is local-first. There is no account to create and no {{product}} server in the middle: everything it keeps is on your Mac.

- One SQLite database, `{{db_file}}`, holds your conversations, runs, agent steps, settings, provider and search keys, MCP settings, schedules and usage. See where your keys are kept.
- Pasted or dropped images are saved as files in `attachments` inside `{{data_dir}}`; global memory and global commands live in the same folder.
- Project memory, custom commands, workflows and agent definitions you add to a project live in its `{{project_dir}}` folder, next to your code.

### What leaves your Mac, and where it goes

Only what the features you set up need:

| Destination | What is sent | When |
|---|---|---|
| Your model provider | the conversation, instructions, and whatever the agents read or produced (file contents, command output) | every model turn |
| The search engines and readers you enabled | search queries and page addresses | when an agent searches or reads a page through a reader |
| Any web page an agent opens | an ordinary web request | when an agent uses `web_fetch` |
| The MCP servers you added | the tool calls agents make to them | when an agent uses one of their tools |

Opening a designed research report may also load web fonts from Google Fonts.

Commands the agents run on your Mac get a cleaned environment by default, so secrets in your shell variables are not handed to them.

<!-- source: D:config/runtime.exs:18-29, D:lib/swarm_code/desktop.ex:488-495, D:lib/swarm_code/projects/workspace.ex:44-53, D:lib/swarm_code/attachments.ex:1-28, D:lib/swarm_code/search.ex:18-34, D:lib/swarm_code_web/controllers/research_controller.ex:14-15, D:lib/swarm_code/settings/setting.ex:110-111 -->
