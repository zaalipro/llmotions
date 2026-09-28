---
title: Slash commands
description: Every slash command of the terminal session, with its arguments and what it does.
---

Type `/` in the composer to list every command; the list narrows as you type, and [[Tab]] or [[Enter]] takes the highlighted one. A command that needs no argument runs at once. Commands work while other runs are working.

## Conversation

| Command | What it does |
|---|---|
| `/new` (also `/clear`) | start a new conversation; this one stays saved |
| `/resume` | pick a saved conversation by title |
| `/resume <id or title>` | open that conversation |
| `/resume-run` | resume the last stopped run of this conversation |
| `/stop` | stop everything running in this conversation |
| `/queue <text>` | queue a message behind the running turn |
| `/compact [focus]` | summarise the conversation so far and continue from the summary |
| `/goal <text>` | set the conversation goal every agent keeps in mind; alone, show it |
| `/search <words>` | search the messages of your conversations |
| `/export [file]` | write this conversation as Markdown |
| `/cost` | tokens and cost of this conversation, by model |
| `/attach <image-path>` | stage an image file from the project for the next message |
| `/deep_research [id]` | attach a finished [deep research](/docs/cli/research/) to the next message |

## Runs and modes

| Command | What it does |
|---|---|
| `/swarm <task>` | start a swarm of agents on a task |
| `/plan [task]` | turn plan mode on or off; with a task, plan it now as a read-only run |
| `/consensus [task]` | switch to Consensus mode; with a task, run this turn as a judged plan |
| `/review` | review the uncommitted changes and report problems |
| `/ultra` | turn Ultra on or off: big tasks become workflows |
| `/workflow <name> [key=value…]` | launch a workflow |
| `/workflow pause\|resume\|stop\|save <run>` | control a workflow run |
| `/workflows` | open the workflow library and runs |
| `/create-workflow [what it should do]` | write a new workflow with the assistant |
| `/rewind` | restore files to how they were before an earlier turn |
| `/agents` | the agent definitions a swarm can use |

See [Modes and run types](/docs/cli/modes/) and [Workflows](/docs/cli/workflows/).

## Model and effort

| Command | What it does |
|---|---|
| `/model [model]` | switch this conversation's chat model; alone, a picker |
| `/swarm_model [model]` | switch the model the sub-agents use |
| `/effort <level>` | reasoning effort of the chat model |
| `/swarm_effort <level>` | reasoning effort of the sub-agent model |

## Approvals

| Command | What it does |
|---|---|
| `/approval [read-only\|auto\|full]` | set the project's approval mode; alone, a picker |
| `/trust` | trust this project: read its instructions and allow edits |

## Screen and settings

| Command | What it does |
|---|---|
| `/panel full\|compact\|hidden` | size of the side panel |
| `/panel summaries on\|off` | AI status lines in the side panel |
| `/diff on\|off` | tool rows with or without their diffs and previews |
| `/theme [dark\|light]` | switch the colour theme at once |
| `/mouse [on\|off]` | mouse-wheel scrolling on or off |
| `/settings [what]` (also `/config`, `/prefs`) | open [Settings](/docs/cli/settings/), at a section or setting |
| `/help` | the commands and the keys |
| `/quit` (also `/exit`) | leave; running work of this session stops |

`/panel`, `/diff`, `/theme` and `/mouse` are remembered for the next session. To see which files this conversation changed, open **Changes** from the [[Ctrl]]+[[P]] palette (see [Rewind and changes](/docs/cli/rewind/)).

## Your own commands

Custom commands and saved workflows appear in the same `/` list. A Markdown file in the project's `{{project_dir}}/commands/` folder becomes a command of its own; see [Project instructions, memory and config](/docs/cli/project/#custom-commands). If a name is taken twice, a built-in command wins over a workflow, and a workflow over a custom command.

> **Note** On the desktop app `/resume` resumes the last stopped run; in the terminal that is `/resume-run`, and `/resume` opens a conversation.

<!-- source: C:apps/swarm_code_core/lib/swarm_code/commands.ex:13-56, C:apps/swarm_code_cli/lib/swarm_code_cli/ui/keymap.ex:165-201, C:README.md:77, C:README.md:111-118, C:README.md:210-219, C:README.md:223-227, C:apps/swarm_code_core/lib/swarm_code/commands.ex:292-296,478-486, D:lib/swarm_code_web/components/chat.ex:66,130-131 -->
