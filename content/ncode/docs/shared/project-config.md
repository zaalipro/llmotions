### The project file

A project can carry settings in `{{project_dir}}/config.json`, committed with the code so the whole team shares them. {{product}} reads two keys from it: `hooks` and `profiles`.

```json
{
  "hooks": {
    "session_start": [{ "command": "git log --oneline -5" }],
    "pre_tool_use": [{ "matcher": "run_command", "command": "./scripts/guard.sh", "timeout_ms": 5000 }]
  },
  "profiles": {
    "careful": { "effort": "high", "swarm_effort": "high" }
  }
}
```

A project file can never set where requests go or what they cost: provider choices, keys, the monthly budget and the workflow budget are ignored if a file contains them.

### Hooks

Hooks are shell commands that run at three moments:

| Hook | When | What its result does |
|---|---|---|
| `session_start` | once when a chat turn starts | its output is added to the agent's instructions |
| `pre_tool_use` | before a tool runs, after approval | exit code 2 blocks the call; what it printed to stderr is the reason the agent sees |
| `post_tool_use` | after a tool returns | informational only |

Each hook has a `command`, an optional `matcher` (a regular expression tested against the tool name, for example `run_command` or `write_file|edit_file`), a `timeout_ms` between 1 and 30,000 (default 10,000) and an `output_cap` (how much of its output is kept) between 1 and 16,384 (default 4,096).

A hook runs only in a trusted project, with the same cleaned environment agent commands get. It can read these variables: `{{env_prefix}}EVENT` (the hook name), `{{env_prefix}}PROJECT` (the project folder) and, for tool hooks, `{{env_prefix}}TOOL` (the tool name). The same three values are also set under their earlier names, `SWARMCODE_EVENT`, `SWARMCODE_PROJECT` and `SWARMCODE_TOOL`, so existing hook scripts keep working.

### Profiles

A profile is a named set of choices you switch a conversation to in one step. Names are 1 to 32 letters, digits, `_` or `-`. A profile may set `model`, `swarm_model`, `effort` and `swarm_effort`; the conversation keeps its provider, so a model must be one your current provider offers.

<!-- source: D:lib/swarm_code/project_config.ex:9-17,87-96,118-160, D:lib/swarm_code/hooks.ex:1-16,34-56,144-163 (ncode/B lib/swarm_code/hooks.ex:156-169 adds the NCODE_ names; the CLI gets them in phase-2 A3, C:apps/swarm_code_daemon/lib/swarm_code/domain/hooks.ex:147-151), D:lib/swarm_code_web/live/workspace_live.ex:7494-7556, D:lib/swarm_code/engine/project_context.ex:37-50 -->
