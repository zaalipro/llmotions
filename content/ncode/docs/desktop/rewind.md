---
title: Rewind
description: Undo the file changes of an earlier turn, restore single files, or fork a conversation from any message, and know what a rewind cannot undo.
---

Agents change real files in your project. {{product}} keeps a snapshot of every file an agent is about to change, so you can put files back the way they were.

{{> shared/checkpoints}}

## Rewinding a turn

1. Open the rewind list: click **Rewind** on a run's card, choose **Rewind…** in the conversation's header menu, or type `/rewind` and press [[Return]].
2. The **Rewind** dialog lists each turn that changed files, with its number, how many files it changed and when. Click a turn to see its files.
3. Click **Restore** beside one file, or **Restore files to before this turn**, then confirm.

{{product}} puts the files back and adds a note to the conversation, for example *Rewound 3 file(s) to before turn 4.* If a file cannot be restored, it stops and says which one and how far it got; fix the cause and rewind again.

![Rewind dialog with two turns, the second expanded to three project-relative files and restore controls.](/assets/shots/desktop/rewind-dialog.webp)

Edits you saved yourself in the Changes view appear as a separate **Manual edits** group, restorable file by file.

## Restoring from the Changes view

The **Changes** view of the agents pane shows the same snapshots next to their diffs. Use it to look at exactly what changed before you restore anything.

## Going back in the conversation

Rewind restores files and keeps every message. To continue from an earlier point of the conversation instead, hover a message and choose **Fork from here**: {{product}} opens a new conversation with the messages before that one, and puts the message itself back in the composer so you can edit and resend it.

## Before you rely on it

- Commit often. Rewind covers file-tool writes inside the project; git covers everything.
- Commands an agent ran are not undone: if an agent ran a migration, installed a package or deleted files with a shell command, rewind cannot bring that back.
- Rewind is per conversation: it lists only the changes made in the conversation you are in.

<!-- source: D:lib/swarm_code/checkpoints.ex:1-16,500-600,654-684, D:lib/swarm_code/tools/write_file.ex:49, D:lib/swarm_code/tools/edit_file.ex:195, D:lib/swarm_code/tools/edit_files.ex:187, D:lib/swarm_code/tools/file_ops.ex:26, D:lib/swarm_code_web/live/workspace_live/changes.ex:543, D:lib/swarm_code_web/live/workspace_live/workspace.html.heex:505-570, D:lib/swarm_code_web/components/chat.ex:63,1118,2777,4325-4336, D:lib/swarm_code_web/components/chat_header.ex:80-92, D:lib/swarm_code_web/live/workspace_live.ex:4924-5000 -->
