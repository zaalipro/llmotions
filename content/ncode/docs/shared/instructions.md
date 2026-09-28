### Project instructions

Instruction files tell agents how your project works: conventions, commands, things to avoid. In every folder of the project down to three levels below the root, {{product}} reads the first of these files that exists:

1. `AGENTS.override.md`
2. `AGENTS.md`
3. `SWARMCODE.md`
4. `CLAUDE.md`

The root's file comes first. At most 12 files and 32,000 characters in total reach the prompt. Instructions are used only after you trust the project.

When you edit instructions from {{product}}, it edits the first of `AGENTS.md`, `SWARMCODE.md` or `CLAUDE.md` that exists in the project root, or creates `AGENTS.md`.

### Memory

Memory is a short list of durable facts, one dated line each (`- [2026-09-01] the API uses SQLite`). Agents add to it with the `remember` tool, and you can edit it yourself.

- Project memory: `{{project_dir}}/MEMORY.md` in the project.
- Global memory: `MEMORY.md` in `{{data_dir}}`, for facts about you that hold in every project.

Both reach every system prompt, capped at 16,000 characters.

### Custom commands

A custom command is a Markdown file that becomes a slash command: `review-api.md` becomes `/review-api`.

- Project commands live in `{{project_dir}}/commands/`; global ones in `commands/` inside `{{data_dir}}`. A project command overrides a global one with the same name.
- Optional front matter: `description`, `swarm` (`true` runs it as a swarm) and `mode` (`plan` or `build`).
- `$ARGUMENTS` in the body is replaced by whatever you type after the command.

```markdown
---
description: Review one API endpoint
swarm: false
---
Review the endpoint $ARGUMENTS for input validation and error handling.
```

If a name is taken twice, a built-in command wins over a workflow, and a workflow wins over a custom command.

### Agent definitions

An agent definition is a Markdown file with front matter (`name`, `description`, `tools`, `model`, `effort`, `prewalk`, `max_turns`); its body is added to that agent's instructions. Agents can pick a definition by name when they start a sub-agent. Definitions are looked up in the project (`{{project_dir}}/agents/`), then your home folder (`~/{{project_dir}}/agents/`), then the three bundled ones: `implementer`, `reviewer` and `scout`.

### Skills

A skill is a folder with a `SKILL.md` file (plus any assets it needs) that an agent can load for a specific job. Project skills win over your own, and yours over the bundled `html-report` skill.

<!-- source: D:lib/swarm_code/engine/project_context.ex:12-26,66-78,108-116, D:lib/swarm_code/memory.ex:1-25, D:lib/swarm_code/projects/workspace.ex:44-53, D:lib/swarm_code/desktop.ex:492-495, D:lib/swarm_code/commands.ex:1-31, D:lib/swarm_code_web/components/chat.ex:119-131, D:lib/swarm_code/agents.ex:1-10,135-140,251-252, D:lib/swarm_code/skills.ex:1-16,60-65 -->
