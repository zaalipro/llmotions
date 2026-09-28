---
title: Data and privacy
description: What ncode keeps on your Mac and where, where your keys are stored, what leaves the machine, and the names you may still see on disk.
---

{{> shared/privacy}}

## What the terminal adds

- **`cli.json`**, beside the database, holds this terminal's own settings (theme, side panel, mouse, keys). It is readable only by you (mode `0600`) and at most 64 KB.
- **A log file**, `cli.log`, in the app's logs folder (see [Names you may still see](#names-you-may-still-see)), readable only by you and rotated. `{{cmd}}` never writes log lines to your terminal. `{{cmd}} config path` prints its exact location.
- Files `{{cmd}}` creates for itself are private to you: it runs with a `077` umask. Commands the agents run in your project keep your own umask, so the files they create look like yours.

{{> shared/secrets}}

Keys reach `{{cmd}}` only by pasting them into Settings or through `{{cmd}} config secret … --stdin`; they are never read from command-line arguments, and never appear on screen, in the log, in undo, in search or in exports.

{{> shared/names}}

<!-- source: C:README.md:249-258, C:README.md:276-278, C:README.md:122-124, C:AGENTS.md:51-55, C:AGENTS.md:213-217, C:AGENTS.md:223, C:apps/swarm_code_cli/lib/swarm_code_cli/release/config_command.ex:230-240, C:apps/swarm_code_cli/lib/swarm_code_cli/release/persisted_session.ex:1137 -->
