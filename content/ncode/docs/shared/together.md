### One machine, one database

The desktop app and the `{{cmd}}` command on the same Mac use the same database, `{{db_file}}`. Your projects, conversations, settings, keys and schedules are the same in both: a conversation started in one can be continued in the other.

Only one of them may have the database open at a time. Three rules keep it safe:

1. **Quit the app before you start a `{{cmd}}` session.** While the app is running under your user account, every `{{cmd}}` command except `--version` and `--help` refuses to start and exits with status 3, naming the running app. Starting it with a different home folder does not change this.
2. **Exit `{{cmd}}` before you reopen the app.** The app does not check for a running `{{cmd}}` session, so this rule is yours to keep.
3. **Keep both on the same version.** If `{{cmd}}` says the database needs an upgrade, open the app once and quit it. If it says the database is newer than it understands, update `{{cmd}}`.

### What only the app does

Some background work runs only inside the desktop app, and only while it is running:

- **Scheduled tasks fire only in the app.** `{{cmd}}` can list, create, edit, switch on or off and "run now" a task, but a schedule never fires from the terminal.
- **Storage retention** (deleting or pruning old sessions on a schedule) runs once a day in the app. The settings are shared, but `{{cmd}}` does not apply them.
- Workflow runs left behind by a crash are tidied up by the app.

<!-- source: C:README.md:66-68,122-124, C:native/platform_identity/README.md:30, C:apps/swarm_code_daemon/lib/swarm_code/daemon/foundation_gate.ex:531-541, C:native/platform_identity/main.m:92-127, C:AGENTS.md:133-137, C:apps/swarm_code_daemon/lib/swarm_code/daemon/boot.ex:14, C:apps/swarm_code_daemon/lib/swarm_code/domain/runtime.ex:4, C:apps/swarm_code_daemon/lib/swarm_code/domain/feature_catalog.ex:212-250, C:docs/settings.md:164-169, D:lib/swarm_code/scheduler.ex:1-19,72-86 -->
