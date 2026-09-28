### Approval modes

Every project has one approval mode. It decides what an agent may do without asking you first.

| Mode | Reads and searches | File writes | Shell commands | Fetching a local or private address |
|---|---|---|---|---|
| Read-only | allowed | blocked | blocked | asks |
| Auto | allowed | allowed | a *safe* command runs; any other command asks | asks |
| Full access | allowed | allowed | allowed | allowed |

Three rules sit on top of the table:

- A command {{product}} classifies as **dangerous** always asks, even in Full access, and "always allow" can never cover it.
- A command classified as **safe** (for example `ls`, `git status` or `cat notes.txt | grep todo`) runs without asking in Auto and Full access.
- Reading a page on `localhost`, a private range such as `10.x` or `192.168.x`, or a link-local address asks in Read-only and Auto. Public pages never ask.

### Project trust

A folder you add is **untrusted** and starts in Read-only. Until you trust it:

- its instruction files (`AGENTS.md` and friends) reach no prompt;
- its hooks do not run.

Trusting a project records your consent and moves it to Auto. A project you already put in Full access stays in Full access.

### Remembered commands

When you allow a command family "always", {{product}} stores that prefix with the project, so the next matching command in any conversation of that project runs without asking. Dangerous commands are never remembered, and a conversation without a project remembers nothing. You can review and forget remembered prefixes later.

<!-- source: D:lib/swarm_code/engine/policy.ex:16-41, D:lib/swarm_code/projects/project.ex:18,29, D:lib/swarm_code/projects.ex:175-189, D:lib/swarm_code/engine/project_context.ex:108-116, D:lib/swarm_code/hooks.ex:12-16, D:lib/swarm_code/engine/run_server.ex:1823-1832,4936-4952, D:lib/swarm_code/tools/web_fetch.ex:67-90, D:lib/swarm_code_web/live/settings_live.ex:1426-1432 -->
