---
title: Data and privacy
description: What ncode stores on your Mac, where your API keys are kept, what is sent to which service, and the names of the folders involved.
---

{{product}} has no account and no cloud of its own. This page says exactly what it keeps, where, and what leaves your Mac.

{{> shared/privacy}}

{{> shared/secrets}}

## Logs

The app writes a log file for troubleshooting: up to three files of 5 MB each in your Logs folder (see the names below). It records the app's own events and errors. If you share it when reporting a problem, read it through first.

## Removing your data

- **One conversation**: delete it from the sidebar.
- **Old data in bulk**: see [Storage and cleanup](/docs/desktop/storage/).
- **Everything**: quit {{product}} and delete `{{data_dir}}`, plus the research and log folders listed under [Names](/docs/desktop/privacy/#names). This also removes the data of the `{{cmd}}` terminal app, which shares it.
- **A project's own files**: delete the `{{project_dir}}` folder in that project.

## Names {#names}

{{> shared/names}}

<!-- source: D:config/runtime.exs:18-29, D:lib/swarm_code/desktop.ex:125-142,488-495, D:lib/swarm_code_web/components/frame.ex:1210-1220, D:lib/swarm_code_web/components/storage_section.ex:60-64, D:lib/swarm_code/research.ex:17 -->
