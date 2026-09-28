---
title: Composer: send, steer, queue
description: How to write and send messages, steer a running turn, queue the next message, start runs side by side, attach an image and stop work.
---

The composer is the text field at the bottom of the session. It always has the keyboard: letters type, [[Enter]] sends, and only a leading `/` turns a line into a command.

## Sending

Type and press [[Enter]]. If the conversation is still loading, [[Enter]] keeps the message and sends it once the conversation has loaded (unless you changed the draft in the meantime).

- **A new line** without sending: [[Ctrl]]+[[O]], [[Ctrl]]+[[J]] or [[Shift]]+[[Enter]] (the last needs a terminal that reports it).
- **A bigger composer:** [[Ctrl]]+[[↑]] adds a row, [[Ctrl]]+[[↓]] takes one back.
- **Your editor:** [[Ctrl]]+[[X]] opens the draft in `$VISUAL`, else `$EDITOR`, else `vi`. Save and quit to bring the text back.
- **Earlier prompts:** on an empty draft, [[↑]] and [[↓]] walk the prompts you sent in this conversation.
- **Editing:** [[Ctrl]]+[[A]] and [[Ctrl]]+[[E]] jump to the start and end of the line, [[Ctrl]]+[[W]] deletes a word, [[Ctrl]]+[[U]] deletes to the start of the line, [[Ctrl]]+[[Z]] undoes.

## Slash commands and file paths

Typing `/` lists every command above the composer, and the list narrows as you type. [[Tab]] completes the highlighted command. [[Enter]] takes it too: a command without an argument runs at once (`/com` then [[Enter]] runs `/compact`); one that needs text waits for it after `/<name> `.

[[Tab]] also completes a file path after `@`, so you can point the assistant at a file by name: `explain @lib/app/router.ex`.

The full list is on [Slash commands](/docs/cli/commands/).

## While a turn runs

Nothing is refused because work is running.

- **Steer.** A message you send while this conversation's chat turn is working goes to that turn. The transcript marks it `→ to the running turn`, and the running turn receives it.
- **Queue.** [[Tab]] or [[Alt]]+[[Enter]] queues the draft instead: it waits under the live turn, marked `queued`, and is sent when the turn ends. `/queue <text>` does the same.
- **Start something beside it.** `/swarm`, `/plan <task>`, `/consensus`, `/create-workflow`, a workflow or a goal start their own run at once, next to the running one.

`/compact` sent during a turn, and a message sent while the conversation is being compacted, wait their turn in the queue.

<!-- capture: cli/composer-steer-queue | a live chat turn with one steered message marked "→ to the running turn" and one queued message drawn under the turn | 120x30 -->

## Attaching an image

```text
/attach docs/screenshot.png
```

stages an image file from inside the project for your next message; it is sent with that message.

## Messages that name a workflow

When a message talks about a *workflow*, the word is highlighted and [[Enter]] sends the message as `/create-workflow <your text>`, so the assistant writes a workflow for you (see [Workflows](/docs/cli/workflows/)). To send it as an ordinary message instead, press [[Ctrl]]+[[S]]. A word inside backticks is not highlighted.

## Stopping

- [[Esc]] stops the turn that is streaming, or the one you just sent. It first closes an open list or dialog. Your draft stays.
- [[Ctrl]]+[[C]] closes an open layer, else clears your draft ([[Ctrl]]+[[Z]] brings it back), else stops the turn.
- `/stop` stops everything running in this conversation.

<!-- source: C:README.md:74-85, C:README.md:216-219, C:AGENTS.md:171-192, C:AGENTS.md:241-249, C:docs/keybindings.md:41-49,63-88, C:apps/swarm_code_core/lib/swarm_code/commands.ex:25,33, C:apps/swarm_code_cli/lib/swarm_code_cli/ui/keymap.ex:165-196 -->
