---
title: Install on macOS
description: Download the ncode disk image, check it, move the app to Applications and open it for the first time on macOS 15 or later.
---

{{product}} {{version}} is a developer preview. It runs on a Mac with {{arch}} and macOS {{min_macos}} or later. Installing takes a few minutes; the only unusual step is the first launch, because the app is not yet notarized by Apple.

## Download

Download [{{dmg}}]({{dmg_url}}).

Then check that the file is intact and is the one we published. Open Terminal and run:

```sh
shasum -a 256 ~/Downloads/{{dmg}}
```

Compare the long number it prints with the line for `{{dmg}}` in [SHA256SUMS]({{sums_url}}). They must match exactly. If they do not, delete the file and download it again.

## Move to Applications

1. Double-click `{{dmg}}` in your Downloads folder. A window opens with the {{product}} app in it.
2. Drag **{{product}}** into your **Applications** folder.
3. Eject the disk image (the eject button next to it in the Finder sidebar) and delete `{{dmg}}` if you like.

## First launch {#first-launch}

Open {{product}} from Applications. The first time, macOS stops it with a message that begins **"Apple could not verify…"**, because the app is not notarized (see below). Click **Done**, not **Move to Trash**.

<!-- shot: desktop/gatekeeper-1.png | owner | the macOS dialog "Apple could not verify “ncode” is free of malware…" on first launch, with the Done and Move to Trash buttons -->

Then allow it once:

1. Open **System Settings** and choose **Privacy & Security** in the sidebar.
2. Scroll down to **Security**. You will see a line saying {{product}} was blocked, with an **Open Anyway** button. Click **Open Anyway**.
3. Confirm with your password or Touch ID, then click **Open** in the dialog that follows.

<!-- shot: desktop/gatekeeper-2.png | owner | System Settings → Privacy & Security, scrolled to Security, showing the “ncode” was blocked line and the Open Anyway button -->
<!-- shot: desktop/gatekeeper-3.png | owner | the confirmation dialog after Open Anyway, with the Open button, before the password prompt -->

You only do this once. From then on, {{product}} opens like any other app.

> **Note** On macOS {{min_macos}} and later, Control-clicking the app and choosing Open no longer skips this check; System Settings is the way.

### From Terminal instead

If you prefer, remove the download mark from the app before the first launch:

```sh
xattr -dr com.apple.quarantine /Applications/{{app}}
```

> **Tip** If the app still does not open after this command, use the System Settings steps above.

## Why ncode is not notarized

Apple notarizes apps from developers with a paid Apple Developer ID. {{product}} does not have one yet, so the app is signed on the build machine only ("ad-hoc"). That is why macOS asks you to confirm it once. The checksum in the Download step is how you know the file is the one we published.

## First steps

When {{product}} opens, add your model provider key and a project: follow the [Quickstart](/docs/desktop/quickstart/).

## Updating

There is no automatic update yet. To update:

1. Quit {{product}} (**⌘Q**, then confirm).
2. Download the new disk image and check it as above.
3. Drag the new {{product}} into Applications and choose **Replace**.

Your conversations, projects, settings and keys are not inside the app, so they stay. The first launch of a new version may ask for the System Settings step again.

## If you had {{old_app}}

{{product}} is the same app under a new name, and it uses the same data folder, so nothing needs moving. Quit {{old_app}}, drag it to the Trash, then install {{app}} as above. Your conversations, projects and keys appear as before.

## Uninstalling

1. Quit {{product}}.
2. Drag {{app}} from Applications to the Trash.

This leaves your data in place, so a later install picks up where you left off. To remove the data too, delete the folder `{{data_dir}}`.

> **Warning** The `{{cmd}}` terminal app uses the same folder. Deleting it removes the conversations, settings and keys of both.

Projects you opened keep their own `{{project_dir}}` folder (memory, commands, workflows). Delete it from a project if you no longer want it. [Update and uninstall](/docs/desktop/update/) lists every folder {{product}} uses.

<!-- source: D:deps/desktop_deployment/lib/package/macos.ex:197-210, D:deps/desktop_deployment/lib/package/macos.ex:336-345, D:mix.exs:7,34-45, D:lib/swarm_code/desktop.ex:492-495, D:config/runtime.exs:21-29, D:lib/swarm_code_web/components/quit_modal.ex:70-80; no updater: grep -rli 'sparkle|check_for_update|updater' D:lib finds only an icon name; requirements and first-launch steps: owner decision (plan §3, §4.5) and Apple's macOS 15 Gatekeeper behaviour (inv-docs §9) -->
