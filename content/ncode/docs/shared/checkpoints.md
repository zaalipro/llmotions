### Checkpoints

Right before an agent changes a file with a file tool, {{product}} saves the file's previous content. If the file did not exist yet, it records that, so restoring deletes the new file again. Rewinding a conversation to an earlier turn restores every file its later turns changed.

What a checkpoint does not cover:

- changes made by shell commands the agent ran (a formatter, a code generator, `git checkout`, `rm`): only file-tool writes are snapshotted;
- anything outside the project folder;
- the conversation itself: rewind restores files, it does not delete messages.

<!-- source: D:lib/swarm_code/checkpoints.ex:1-16, D:lib/swarm_code/tools.ex:12-36, D:lib/swarm_code_web/components/chat.ex:63 -->
