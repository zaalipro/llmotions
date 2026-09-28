---
title: Settings reference
description: Every setting of the terminal and the shared database, with its key, scope, type, default, when a change applies and what overrides it.
---

This reference is generated from the settings registry of `{{cmd}}` itself, so it lists exactly the keys that [Settings](/docs/cli/settings/) shows and [`{{cmd}} config`](/docs/cli/config/) accepts.

How to read it:

- **Key** is the name for `{{cmd}} config get`, `set` and `reset`, and for `/settings <key>`.
- **Scope** is where the value is kept: `global` (the database the desktop app shares), `project` (this project), `session` (one conversation), `cli` (`cli.json`, this terminal only) or `project_file` (`{{project_dir}}/config.json`, read-only here).
- **Applies** says when a change takes effect, for example `at once`, `next turn`, `next spawn` (the next agent started), `next launch`, or `desktop` when only the desktop app acts on it.
- **Override** names a flag or environment variable that wins while it is set.

{{> import/settings}}

<!-- source: C:docs/settings.md:1-9, C:README.md:249-251, C:apps/swarm_code_cli/lib/swarm_code_cli/release/config_command.ex:43-50 -->
