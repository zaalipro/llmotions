### What takes space

{{product}} keeps its own data in one local database plus a few folders: your sessions (conversations and their runs), the details of every agent step (tool output, prompts), rewind snapshots, workflow journals and research reports. Cleaning up touches only this data, never your project files or the `{{project_dir}}` folder in a project.

### Two ways to shrink it

- **Delete** removes whole sessions, snapshots, journals or reports for good.
- **Prune** keeps every session and its transcript, tokens, cost and timings, and drops only the bulky details of finished runs: tool output and prompts. A pruned run still reads the same in the transcript; its agent steps just no longer show their full output.

Nothing is ever removed from a session that is pinned, open in a window or still running.

### Retention

Retention does the same work on a schedule, once a day, while the desktop app is running:

- delete sessions older than 30, 60, 90 or 180 days (off by default);
- prune agent details older than 14, 30 or 90 days (off by default).

### Reclaiming disk space

Deleting rows frees space inside the database file, not on the disk. Reclaiming the space (SQLite's `VACUUM`) rewrites the file so it shrinks; it deletes nothing, and the sweep never does it on its own.

<!-- source: D:lib/swarm_code_web/components/storage_section.ex:30-35,60-64,147-186,424-476,541-567,700-711, D:lib/swarm_code/settings/setting.ex:105-107, D:lib/swarm_code/scheduler.ex:46,72-86 -->
