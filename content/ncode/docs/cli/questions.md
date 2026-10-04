---
title: Questions from agents
description: When an agent asks you something, how to pick, tick or type an answer with the keyboard, leave a question for later, and what happens in headless runs.
---

The assistant, and the lead agent of a swarm, can stop and ask you a question when a choice is yours to make: which of two designs, which files to leave alone, whether a finding matters. Worker agents cannot ask; they report to their lead.

## When an agent asks

The question opens by itself over the conversation as one note, with every question of that call in it. Each question offers a list of answers and an **other** field for an answer of your own. Some questions let you tick several answers.

For a moment after the note opens, your keys keep typing into the draft, so a sentence you are writing is never taken as an answer.

![ncode interview note on question 1 of 2, showing three interface choices and an other option, with Keyboard hints and Progress detail selected for the second question.](/assets/shots/cli/question-note.webp)

## Answering

| Key | Does |
|---|---|
| `1` … `9` | pick that answer (in a multi-select question, tick or untick it) |
| [[Space]] | tick or untick the highlighted answer (multi-select only) |
| [[Tab]] | move between the list and the **other** field |
| [[←]] / [[→]] | go to the previous or next question |
| [[Enter]] | confirm this question and go to the next; on the last one, send all the answers |

Nothing is sent until the final [[Enter]], so you can go back and change an earlier answer first.

## Leaving a question for later

[[Esc]] puts the note aside and keeps the answers you have given so far. The agent keeps waiting. [[Ctrl]]+[[N]] brings the note back, and it also opens the next approval or question when several are waiting.

## Questions in headless runs

In a [headless run](/docs/cli/headless/) nobody can answer, so a question stops the run. Give a headless task the context it needs up front, or run it in the full screen, where you can answer.

<!-- source: C:AGENTS.md:189-192, C:README.md:103-107, C:README.md:159-165, C:docs/keybindings.md:48, D:lib/swarm_code/tools.ex:49-51 -->
