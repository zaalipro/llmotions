---
title: Troubleshooting
description: What to do when ncode refuses to start, cannot be found, draws oddly, closes a session, or macOS blocks it.
---

`{{cmd}}` says what went wrong in one sentence and what to do in a second one. This page collects those sentences, and a few problems that come from the terminal or macOS.

## It refuses to start (exit code 3) {#exit-3}

### The app is open

```term
The {{product}} app is open, and only one of them can use your conversations at a time.
Quit the {{product}} app, then run {{cmd}} again.
```

The desktop app is running under your user account. Quit it with [[⌘Q]] (closing its window is not enough) and run the command again. Only `{{cmd}} --version` and `{{cmd}} --help` work while the app runs. See [Works with the desktop app](/docs/cli/desktop/).

### Another session is open

```term
Another {{cmd}} (process 48213, since 09:41) is already using your conversations.
Close it first (Ctrl-C twice, and once more if it asks), then run {{cmd}} again.
```

Another `{{cmd}}` session, in another terminal window or tab, holds the database. Close it, or continue your work there. This also applies to `{{cmd}} -p` and to `{{cmd}} config set` on a setting stored in the database.

### No provider

```term
No model provider is set up yet.
```

Add one with `{{cmd}} settings providers`; see the [Quickstart](/docs/cli/quickstart/#add-a-model-provider).

### The database needs the app, or a newer `{{cmd}}`

```term
This {{product}} database needs an upgrade that only the {{product}} app makes.
```

Open the desktop app once, quit it, and run `{{cmd}}` again.

```term
This {{product}} database was upgraded by a newer {{product}} app than this {{cmd}} supports.
```

Update `{{cmd}}` by re-running the [installer](/docs/cli/install/#update). In both cases nothing in the database was changed.

### The data folder

```term
{{cmd}} could not safely open its private data folder.
```

`{{data_dir}}` must belong to you and have mode `0700`. Check it with `ls -ld` and fix it with `chmod 700` on that folder.

### It cannot tell whether the app is running

```term
{{cmd}} could not check whether the {{product}} app is running.
```

Re-run the [installer](/docs/cli/install/#update), as the message says.

### Other database messages

`{{cmd}}` also stops when it cannot use the database file. The second line of each message says what to do:

- **"The file where your conversations database belongs is not an {{product}} database."** or **"Your conversations database failed SQLite's integrity check."** The file `{{db_file}}` was replaced or is damaged, and nothing was changed. Move it aside, or restore it from a verified backup, then run `{{cmd}}` again. The backups `{{cmd}}` makes before it upgrades the database are in the `backups` folder beside it.
- **"Your conversations database comes from an {{product}} version this {{cmd}} does not know."** Update `{{cmd}}` by re-running the [installer](/docs/cli/install/#update), or open the desktop app once to upgrade the database.
- **"{{cmd}} could not make a verified backup before upgrading the database, so it changed nothing."** Free some disk space and run `{{cmd}}` again.
- **"{{cmd}} could not upgrade the database; it was left as it was."** The verified backup is in the `backups` folder beside the database. Open the desktop app, or report the problem with the lines from `cli.log` (see [A session closed on its own](#a-session-closed-on-its-own)).
- **"{{cmd}} could not open your conversations database."** Close other `{{cmd}}` windows and run it again.

## `command not found: {{cmd}}`

`~/.local/bin` is not on your `PATH`. Add it as shown in [Install](/docs/cli/install/#path), then open a new terminal window.

## macOS blocks it, or a `dyld` error names a macOS version

- **"cannot be opened because the developer cannot be verified"**, or a similar Gatekeeper message: {{product}} {{version}} is a [developer preview that is not notarized](/docs/cli/install/#developer-preview), so macOS blocks it when the archive carries a quarantine mark, which browsers add and `curl` does not. Remove the mark as shown in [Install the release by hand](/docs/cli/install/#manual-install); the one-line installer is not affected.
- **A `dyld` error that names a macOS version** means the Mac runs an older macOS than {{product}} was built for. {{product}} {{version}} needs macOS {{min_macos}} or later on {{arch}}.

## Keys do something unexpected

- **Option does not work as Alt** in some terminals (Ghostty on macOS in particular). Nothing essential needs Alt: queue with [[Tab]] instead of [[Alt]]+[[Enter]], and use [[Ctrl]]+[[G]] for the runs dashboard instead of the Alt run-tab keys.
- **A letter answered nothing:** approval letters work only while your draft is empty; clear the draft ([[Ctrl]]+[[C]]) first.
- **Mouse selection does not work:** hold [[Shift]] while dragging ([[Option]] in Terminal.app and iTerm2), or type `/mouse off`.

## The screen looks wrong

- **Boxes or symbols are misaligned:** set **Ambiguous-width characters** to the other value in Settings → Appearance.
- **Symbols are missing or show as question marks:** start with `{{env_prefix}}ASCII=1 {{cmd}}`, or set **Glyphs** in Settings → Appearance.
- **Colours are wrong:** `NO_COLOR=1 {{cmd}}` gives a monochrome screen. The richest glyphs need a truecolor terminal (see [Terminal, themes and mouse](/docs/cli/terminal/)).

## A session closed on its own

The reason is in `cli.log`; `{{cmd}} config path` prints where it is. When you report a problem, include the lines around the time it closed.

## [[Ctrl]]+[[C]] ended the program

That is expected outside the full screen: while it starts, during a `-p` run, or after the exit summary, [[Ctrl]]+[[C]] simply ends `{{cmd}}`.

## Check the setup

```sh
{{cmd}} config doctor
```

checks the files and the environment {{product}} relies on and says what is wrong.

<!-- source: C:apps/swarm_code_cli/lib/swarm_code_cli/release/persisted_session.ex:955-1040,1100-1121, C:apps/swarm_code_daemon/lib/swarm_code/daemon/schema/refusal.ex:12-52, C:apps/swarm_code_daemon/lib/swarm_code/daemon/platform/paths.ex:31-39, C:README.md:122-126, C:README.md:66-68, C:AGENTS.md:52-55, C:AGENTS.md:165-168, C:AGENTS.md:178-188, C:apps/swarm_code_cli/lib/swarm_code_cli/release/config_command.ex:64,230-240, C:docs/settings.md:128-130, C:docs/keybindings.md:35-38,46,55 -->
<!-- notes: sentences quoted in their post-rename form (ncode/A 8a70a02 persisted_session.ex:975-976,1001-1002,1008-1013,1018-1031,1038,1116; schema/refusal.ex:18,29-30,40-41,51; the backups folder is <data>/backups, C:…/platform/paths.ex:39). Pending lane F: the dyld wording and the macOS floor (plan-v2 §4.6 build target 15.0); the Gatekeeper sentence is macOS's own, GUESSED wording. The process id and time in the lease example are made up. -->
