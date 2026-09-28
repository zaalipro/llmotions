---
title: Storage and cleanup
description: See how much space ncode's data takes, clean up old sessions, snapshots and reports safely, prune agent details, and set retention.
---

{{product}} keeps every conversation, every agent step and every file snapshot, so the database grows as you use it. **Settings → Storage** shows where the space goes and lets you take it back without losing what matters.

{{> shared/storage}}

## The storage bar

The bar shows the total size and how it splits: **Sessions**, **Agent details**, **Rewind snapshots**, **Workflow journals**, **Research**, and **Index & free space**. Hover a part to see its size.

<!-- shot: desktop/storage-bar.png | Settings → Storage with the storage bar of a seeded database, each coloured part labelled, and the Clean up… and Retention controls below -->

## Cleaning up

Click **Clean up…**. The dialog has three tabs:

- **Quick**: one-click presets: *Delete sessions older than 30 days*, *Keep only the last 2 weeks*, *Prune agent details older than 14 days*, *Delete rewind snapshots older than 30 days* and *Reclaim disk space*.
- **Sessions**: every session with its size, messages and runs, sortable, so you can pick exactly which to delete. Pinned sessions are excluded unless you tick them here.
- **Advanced**: separate ages for rewind snapshots, workflow journals of finished runs, agent details and research reports, whether to delete empty sessions, and **Reclaim disk space afterwards (VACUUM)**.

Then click **Review**. The review step lists what will be removed, what will be kept back and why (pinned, open in a window, still running), and warns that deleted sessions, snapshots and reports cannot be recovered. Confirm to run it. When it is done you can **Reclaim disk space now**.

<!-- shot: desktop/storage-review.png | the Clean up dialog's Review step for the "Delete sessions older than 30 days" preset, with counts, a Kept back list and the irreversible-delete warning -->

## Retention

Under **Retention**, pick **Automatically delete sessions older than** (30, 60, 90 or 180 days) and **Prune agent details older than** (14, 30 or 90 days). The app then applies them by itself once a day while it runs. The line under them says when the last sweep ran.

> **Tip** Pin the conversations you want to keep for ever: pinned, open and running sessions are never touched by a cleanup or by retention.

<!-- source: D:lib/swarm_code/storage.ex:236-258,374-416, D:lib/swarm_code_web/components/storage_section.ex:30-35,51-190,200-310,420-570,700-711, D:lib/swarm_code/scheduler.ex:72-86 -->
