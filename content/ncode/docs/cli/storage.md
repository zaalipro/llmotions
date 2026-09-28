---
title: Storage
description: See how much space ncode's data takes, prune or delete old sessions, reclaim disk space, and how retention works with the desktop app.
---

{{> shared/storage}}

## Storage in the terminal

Open Settings → **Storage**. It measures what {{product}}'s data takes, and runs a cleanup or a vacuum for you. Measuring and cleaning run as a task with its seconds shown; `c` cancels.

Cleaning up changes the shared database, so it runs from one place at a time: from `{{cmd}}` while the desktop app is closed, or from the app.

> **Note** The two retention settings, **Automatically delete sessions older than** and **Prune agent details older than**, can be set here, but only the desktop app applies them, once a day while it is running. With the terminal alone, clean up by hand from this page.

<!-- source: C:README.md:247, C:README.md:258-259, C:README.md:66-68, C:docs/settings.md:164-169, C:apps/swarm_code_daemon/lib/swarm_code/daemon/boot.ex:14 -->
