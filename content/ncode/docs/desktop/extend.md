---
title: Commands, agents and skills
description: Add your own slash commands, see and write agent definitions, and add skills, for one project or for every project.
---

Three kinds of Markdown files extend what {{product}} does: **custom commands** (your own slash commands), **agent definitions** (specialists agents can start by name) and **skills** (instructions and assets an agent loads for one job). The file formats are in the reference on [Instructions, memory and project config](/docs/desktop/instructions/#custom-commands); this page shows how to add them from the app.

## Adding a custom command

1. Open **Settings → Commands**. (The project it works on is the one picked in **Settings → Memory**.)
2. Click **New command**. {{product}} creates `new-command.md` from a template, in the project's `{{project_dir}}/commands/` folder (or your global one if no project is picked), and opens the folder in the Finder.
3. Rename the file to the command you want (`release-notes.md` becomes `/release-notes`) and edit it, for example:

```markdown
---
description: Draft release notes since a tag
mode: plan
---
Read `git log $ARGUMENTS..HEAD` and draft release notes grouped by feature, fix and chore.
```

Then type `/` in the composer: the command appears in the list with its description. `/release-notes v1.2.0` runs it with `v1.2.0` in place of `$ARGUMENTS`.

**Open project commands** and **Open global commands** open the two folders in the Finder. Commit the project folder to share commands with your team.

## Agent definitions

**Settings → Agents** lists every agent definition {{product}} found, with its tier (bundled, yours or the project's), its model, effort and tools. Agents can start a sub-agent from one of these definitions by name.

The three bundled definitions:

| Name | What it is for |
|---|---|
| `scout` | a read-only explorer that searches code and reports what it finds |
| `reviewer` | a code reviewer that reads changes and reports issues |
| `implementer` | writes and edits code to complete a task |

To add your own, create a `.md` file in `{{project_dir}}/agents/` in the project (or `~/{{project_dir}}/agents/` for every project). The bundled `scout` shows the format:

```markdown
---
name: scout
description: Read-only explorer that searches code and reports findings
tools: read_file,grep,find_files,web_fetch,lsp
effort: low
prewalk: false
max_turns: 20
---
You are a scout. Your job is to explore the codebase, find relevant code,
and report your findings. You must not change any files.
```

A project definition with the same name replaces yours, and yours replaces a bundled one.

## Skills

A skill is a folder with a `SKILL.md` file and any assets it needs, for example a report template. {{product}} bundles one, `html-report`. Add your own in `{{project_dir}}/skills/` in the project, or in `skills` inside `{{data_dir}}` for every project. A project skill with the same name wins over yours, and yours over a bundled one.

<!-- source: D:lib/swarm_code_web/live/settings_live.html.heex:1259-1325,1386-1415, D:lib/swarm_code_web/live/settings_live.ex:1813-1841,2204-2207, D:lib/swarm_code/commands.ex:1-31,68-73, D:lib/swarm_code/agents.ex:1-10,135-152,251-252, D:priv/agents/scout.md:1-10, D:lib/swarm_code/skills.ex:1-25,60-66, D:priv/agents/reviewer.md:1-4, D:priv/agents/implementer.md:1-4 -->
