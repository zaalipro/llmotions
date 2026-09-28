---
title: Update and uninstall
description: Update ncode by replacing the app, move from the earlier app name, and uninstall with or without your data, knowing every folder ncode uses.
---

## Updating

{{product}} does not update itself yet. When a new version is out:

1. Quit {{product}} ([[⌘]]+[[Q]], then **Quit**). If workflows are running, the button reads **Pause & quit**: they pause and resume after the update.
2. Download the new disk image and check its SHA-256 as in [Install](/docs/desktop/install/#download).
3. Drag the new {{product}} into Applications and choose **Replace**.
4. Open it. If macOS stops it again, allow it as in [First launch](/docs/desktop/install/#first-launch).

Your conversations, projects, settings and keys live outside the app, so they stay. A new version may upgrade the database the first time it opens; keep the `{{cmd}}` terminal app on the same version (see [Using with the CLI](/docs/desktop/cli/)).

The versions and their notes are listed on the [releases page](/releases/).

## Moving from {{old_app}}

{{product}} is the same app under its new name. It keeps the same data folder, so there is nothing to export or import:

1. Quit {{old_app}}.
2. Drag {{old_app}} from Applications to the Trash.
3. Install {{app}} as described in [Install](/docs/desktop/install/).

Your conversations, projects, keys and schedules appear as before.

## Uninstalling

1. Quit {{product}}.
2. Drag {{app}} from Applications to the Trash.

That removes the app and keeps your data, so installing again later brings everything back. To remove the data as well, delete these too:

| What | Where |
|---|---|
| Database, keys, attachments, global memory, commands, workflows and skills | `{{data_dir}}` (shared with the `{{cmd}}` terminal app) |
| Deep research reports and logs | the two folders under "Names" below |
| Your agent definitions | `~/{{project_dir}}` |
| A project's memory, commands, workflows and settings | the `{{project_dir}}` folder inside that project |

> **Warning** Deleting `{{data_dir}}` removes your conversations, settings and keys for good, in the app and in `{{cmd}}`. Export conversations you want to keep first.

## Names

{{> shared/names}}

<!-- source: D:lib/swarm_code/desktop.ex:125-142,488-495, D:config/runtime.exs:21-29, D:lib/swarm_code_web/components/quit_modal.ex:84-120, D:lib/swarm_code/projects/workspace.ex:44-53, D:lib/swarm_code/workflows.ex:94, D:lib/swarm_code/skills.ex:62, D:lib/swarm_code/agents.ex:251-252, D:lib/swarm_code/research.ex:17, D:mix.exs:34-45; no updater: grep -rli 'sparkle|check_for_update|updater' D:lib finds only an icon name -->
