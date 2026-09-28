---
title: Project instructions, memory and config
description: Tell agents how your project works with AGENTS.md, keep facts in memory, add your own commands, agent definitions and skills, and use the project file.
---

Everything on this page lives in files you can read, edit and commit: instruction files in the project, and a `{{project_dir}}` folder for memory, commands, agent definitions, workflows and the project file. The desktop app reads the same files.

## Instructions and memory

{{> shared/instructions}}

## In the terminal {#in-the-terminal}

- Instructions and hooks take effect only in a trusted project: type `/trust` once (see [Approvals and trust](/docs/cli/approvals/)).
- Settings has a **Memory & instructions** section, and a **Library** section for your custom commands, agent definitions, skills and workflows.
- `/agents` lists the agent definitions a swarm can use.
- `{{cmd}} config path` prints where the project's `config.json`, `MEMORY.md` and instruction file are.

## The project file and hooks

{{> shared/project-config}}

Hooks also receive the same values under their earlier names, `SWARMCODE_EVENT`, `SWARMCODE_PROJECT` and `SWARMCODE_TOOL`, so older hook scripts keep working; read the `{{env_prefix}}` names in new ones.

### The project file in the terminal

The terminal shows the project file in Settings → **Project file**, read-only: edit `{{project_dir}}/config.json` in your editor and commit it. There is no `/profile` command in the terminal; switch a conversation's model and effort with `/model` and `/effort` (see [Modes and run types](/docs/cli/modes/#model-and-effort)).

<!-- source: C:README.md:244-245, C:docs/settings.md:7-9,113-121, C:apps/swarm_code_core/lib/swarm_code/commands.ex:13-50, C:apps/swarm_code_cli/lib/swarm_code_cli/release/config_command.ex:230-240, C:apps/swarm_code_daemon/lib/swarm_code/domain/hooks.ex:145-152, C:apps/swarm_code_daemon/lib/swarm_code/domain/workflows.ex:90-94, D:lib/swarm_code/engine/project_context.ex:108-116, D:lib/swarm_code/hooks.ex:12-16,157-163 -->
<!-- notes: depends on phase 2 (lane A3): the CLI sets only SWARMCODE_EVENT/PROJECT/TOOL today (C:apps/swarm_code_daemon/lib/swarm_code/domain/hooks.ex:147-151, unchanged on ncode/A 8a70a02); A3 adds NCODE_EVENT/PROJECT/TOOL beside them (plan-v2 §4.1 A3, assumption 7), as lane B already does for the desktop (ncode/B lib/swarm_code/hooks.ex:162-168). The shared partial's {{env_prefix}} names are true for 0.1.0 only with A3 merged; listed in lane-D.md. -->
