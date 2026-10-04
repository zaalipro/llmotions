---
title: Approvals and trust
description: The three approval modes, what an untrusted project cannot do, how to answer an approval card with one key, and how headless runs handle approvals.
---

Agents act only through tools, and every tool call that could change something is checked against the project's **approval mode** first. The mode belongs to the project, not to the conversation, and the desktop app uses the same one. It is always shown on the status line.

## The rules

{{> shared/approvals}}

## Changing the mode

```text
/approval auto
```

`/approval read-only`, `/approval auto` and `/approval full` switch the project's mode; `/approval` alone opens a picker of the three with the current one checked. Every change, from here, from Settings or from the desktop app, is said in the chat:

```term
Approvals: auto → full access
```

`/trust` trusts the project: its instruction files are read from then on, its hooks may run, and a read-only project moves to auto. In Settings, **Approvals & trust** shows the mode, the trust switch and the list of always-allowed commands, which you can edit.

## The approval card

When an agent needs your answer, a card opens by itself above the composer. It shows the command in a code block of at most six lines; with your draft empty, [[Enter]] shows every line and [[Enter]] again folds them back.

| Key | Answer |
|---|---|
| `y` | allow once |
| `Y` | allow for the rest of this run |
| `A` | always allow this command family in this project |
| `d` | deny |
| `D` | deny and stop the run |
| `n` | leave this one and show the next thing waiting |

A card offers only the answers that apply to it, and only those letters answer it. Three rules keep you from answering by accident:

- For a moment after a card opens, your keys keep typing into the draft, so a sentence you are in the middle of is never taken as an answer.
- The letters answer only while your draft is empty. Any other letter types, and [[Enter]] with a draft sends the draft; the card stays.
- The same applies to a card you brought back with [[Ctrl]]+[[N]] or `n`.

[[Ctrl]]+[[N]] opens the next approval or question waiting on you. In an [agent overlay](/docs/cli/agents/#the-agent-overlay) the same letters answer that agent's request.

![ncode approval card asking permission to run a three-line mix test command, with once, this run, always, deny, deny-and-stop and next actions beneath it.](/assets/shots/cli/approval-card.webp)

![Long shell-command approval in ncode folded after six lines, with two more lines hidden and an Enter shows all hint.](/assets/shots/cli/approval-folded.webp)

## Approvals in headless runs

A [headless run](/docs/cli/headless/) (`{{cmd}} -p`) has nobody to ask. It uses the project's approval mode as it is: whatever the mode allows runs, and anything that would still need a person is denied, with a line on stderr saying what was denied. In full access the stderr line says that nothing asks. An agent's question stops a headless run.

<!-- source: C:README.md:91, C:README.md:103-121, C:README.md:159-165, C:AGENTS.md:123-129, C:AGENTS.md:178-184, C:docs/keybindings.md:48, C:docs/settings.md:104-111, C:apps/swarm_code_core/lib/swarm_code/commands.ex:41-42, D:lib/swarm_code/engine/policy.ex:14-41, D:lib/swarm_code/projects.ex:175-191 -->
