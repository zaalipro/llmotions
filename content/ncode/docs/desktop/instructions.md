---
title: Instructions, memory and project config
description: Tell agents how your project works with AGENTS.md, keep durable facts in memory, and share hooks and profiles through the project file.
---

Agents start every turn knowing nothing about your project except what you give them. This page covers the three ways to give them context: instruction files, memory, and the project file with its hooks and profiles.

## Editing instructions in the app

Open the **⋯** menu of a project in the sidebar and choose **Edit AGENTS.md**. {{product}} opens the project's instruction file in an editor; save to write it. If the project has none, saving creates `AGENTS.md` in the project root.

A good instruction file is short and concrete: how to build and test, the conventions agents keep breaking, the folders not to touch.

```markdown
# Notes for agents
- Build: `npm run build`. Test: `npm test -- --run`.
- Use the existing `api/` client for HTTP; do not add new HTTP libraries.
- Never edit files under `generated/`; run `npm run codegen` instead.
```

## Editing memory in the app

Open **Settings → Memory**. Pick a project to edit its memory, and edit your global memory below it. **Clear** empties one list. Agents add lines themselves with the `remember` tool when they learn something worth keeping.

{{> shared/instructions}}

{{> shared/project-config}}

### Switching profiles

In a conversation, type `/profile <name>` in full (it is not in the `/` list) to apply a profile from the project file; {{product}} confirms with *Switched to profile: careful*. `/profile` alone lists the available profiles, and with none defined it tells you to add them to `{{project_dir}}/config.json`.

<!-- source: D:lib/swarm_code_web/components/frame.ex:780-819,3362-3375, D:lib/swarm_code_web/live/workspace_live/editor.ex:1-20, D:lib/swarm_code/engine/project_context.ex:66-78, D:lib/swarm_code_web/live/settings_live.html.heex:1150-1258, D:lib/swarm_code_web/live/workspace_live.ex:7494-7556 -->
