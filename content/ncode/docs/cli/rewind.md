---
title: Rewind and changes
description: See which files a conversation changed, and put files back to how they were before an earlier turn.
---

Every file an agent changes with a file tool is saved first, so a turn that went wrong is one command away from undone.

{{> shared/checkpoints}}

## Rewinding

```text
/rewind
```

opens this conversation's checkpoints. Pick the turn to go back to: the files its later turns changed are restored to how they were before, and files those turns created are deleted again. The conversation itself stays as it was; only files change.

**Checkpoints** in the [[Ctrl]]+[[P]] palette opens them too.

> **Warning** Rewind covers file-tool writes only. If an agent ran a command that changed files (a formatter, a generator, `git checkout`), undo that with your own tools, for example Git.

![ncode Checkpoints layer over three file-changing turns, with release_step_2.txt highlighted between release_step_3.txt and release_step_1.txt and a Restore action below its details.](/assets/shots/cli/rewind-list.webp)

## What changed

**Changes** in the [[Ctrl]]+[[P]] palette shows the files this conversation changed.

In the transcript, each file-writing tool row shows its diff under it. `/diff off` draws every tool row on one line instead, and `/diff on` brings the diffs back; **Diff lines shown** in Settings → Layout & transcript sets how many lines a row shows (12 by default).

## Isolated sub-agents

By default a sub-agent works in its own isolated copy of the project, so several agents can edit at once without stepping on each other. Its changes reach your project only when its lead integrates them. **Isolate sub-agents** and **How to isolate** in Settings → Agents & limits control this.

<!-- source: C:README.md:223-227, C:README.md:115-118, C:AGENTS.md:202, C:apps/swarm_code_core/lib/swarm_code/commands.ex:24,43, C:docs/settings.md:97-98,141,144, D:lib/swarm_code/checkpoints.ex:1-16 -->
