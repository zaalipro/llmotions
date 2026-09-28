---
title: Install
description: Install {{cmd}} with one line, check it, update it and remove it.
---

Install with one line. It needs macOS {{min_macos}} or later on {{arch}}.

## Install

```sh
{{install}}
```

> **Note** Nothing is installed system-wide.

## Check the install

| Command | Prints |
|---|---|
| `{{cmd}} --version` | `{{cmd}} {{version}}` |
| `a \| b` | a pipe inside code |

Press [[Ctrl]]+[[C]] twice to quit. This is **bold**, this is *italic*, and a literal \{{cmd}}.

```term
╭─ ncode ─────────╮
│ ready           │
╰─────────────────╯
```

## Uninstall {#uninstall}

1. Run the uninstaller:

   ```sh
   {{uninstall}}
   ```

2. Keep or remove `{{data_dir}}`.

## Uninstall

The second heading with the same text gets a numbered id.

{{> shared/approvals}}

<!-- source: C:scripts/install.sh:1-40 -->
