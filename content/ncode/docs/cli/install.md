---
title: Install
description: Install the ncode command with one line, check it, put it on your PATH, update it, remove it, or build it from source.
---

> **Note** This is a preview of the docs. The download and the one-line installer go live with the 0.1.0 release; until then these steps describe how they will work.

The `{{cmd}}` command installs into your home folder with one line. It needs no administrator password and touches nothing outside its own folders.

## One-line install

```sh
{{install}}
```

The installer:

1. checks that the Mac runs macOS {{min_macos}} or later on {{arch}}, and stops with a message otherwise;
2. downloads the release for version {{version}} and checks its SHA-256 checksum against the one pinned in the installer; on a mismatch it stops and changes nothing;
3. puts the release in `~/.local/share/{{cmd}}` and a small `{{cmd}}` command in `~/.local/bin`;
4. prints what to run next.

It never touches your conversations, settings or keys: those live in the {{product}} data folder, `{{data_dir}}`, which the desktop app shares.

To install somewhere else, set a prefix. The release then goes to `<prefix>/share/{{cmd}}` and the command to `<prefix>/bin`:

```sh
curl -fsSL {{install_url}} | {{env_prefix}}PREFIX="$HOME/tools" sh
```

<!-- capture: cli/install | the one-line installer's output on a fresh Mac: platform check, download, checksum OK, installed paths, the PATH hint and the next steps | 100x24 -->

## Check that it works

```sh
{{cmd}} --version
```

This prints `{{cmd}} {{version}}`. `{{cmd}} --help` prints every option. Both are answered before anything else starts, so they work even while the desktop app is open.

## Put ~/.local/bin on your PATH {#path}

If your shell says `command not found: {{cmd}}`, the folder is not on your `PATH` yet. The installer tells you when that is the case; it never edits your shell files itself.

For zsh, the default shell on macOS:

```sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

For bash:

```sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

## Update

Run the same line again:

```sh
{{install}}
```

It replaces the release in place. Your conversations, settings and keys stay where they are, so nothing is lost. Quit any running `{{cmd}}` session first.

## Uninstall

```sh
{{uninstall}}
```

This removes the release, the `{{cmd}}` command and the `{{old_cmd}}` alias the installer wrote. By hand, the same is:

```sh
rm -f ~/.local/bin/{{cmd}} ~/.local/bin/{{old_cmd}}
rm -rf ~/.local/share/{{cmd}} ~/.local/share/{{old_cmd}}
```

(The last path is only there if you installed {{product}} under its earlier name.)

> **Warning** Neither way deletes your data. `{{data_dir}}` holds your conversations, settings and provider keys, and the desktop app uses the same folder. Delete it only if you are removing the app too and want everything gone.

## The old command name {#old-command}

{{product}} was called by another name before this release, and its command was `{{old_cmd}}`. The installer also writes `{{old_cmd}}` as an alias: it runs `{{cmd}}` with the same arguments and, in a terminal, prints a one-line note that the name has changed. Scripts that call `{{old_cmd}}` keep working; move them to `{{cmd}}` when you can, because the alias will be removed in a later release. The older `{{old_env_prefix}}…` environment variables are still read too (see [Environment variables](/docs/cli/env/)).

## Developer preview: why it opens without a warning {#developer-preview}

{{product}} {{version}} is a developer preview. It is not notarized by Apple, because notarizing needs a paid Apple Developer ID, which {{product}} does not have yet.

macOS checks an unnotarized program when it carries a *quarantine* mark, which browsers and Mail add to everything they download. `curl` adds no such mark, so a release installed by the one-line installer starts without a Gatekeeper prompt. This holds **only for downloads made with `curl`**. A release downloaded with a browser is quarantined, and macOS refuses to run its programs until the mark is removed (see the manual install below).

## Install the release by hand {#manual-install}

If you prefer not to pipe a script into `sh`, download the release yourself. The asset is on the [GitHub releases]({{cli_repo}}/releases) of the `{{cmd}}` repository, named `ncode-{{version}}-darwin-arm64.tar.gz`:

```sh
cd ~/Downloads
curl -fLO {{cli_repo}}/releases/download/v{{version}}/ncode-{{version}}-darwin-arm64.tar.gz
shasum -a 256 ncode-{{version}}-darwin-arm64.tar.gz
```

Compare the printed checksum with the one on the [releases page](/releases/); stop if they differ. Then unpack it and put it where the installer would:

```sh
tar -xzf ncode-{{version}}-darwin-arm64.tar.gz
mkdir -p ~/.local/share ~/.local/bin
rm -rf ~/.local/share/{{cmd}}
mv ncode-{{version}} ~/.local/share/{{cmd}}
chmod 0600 ~/.local/share/{{cmd}}/releases/COOKIE
ln -sf ~/.local/share/{{cmd}}/bin/{{cmd}} ~/.local/bin/{{cmd}}
```

If you downloaded the archive with a browser instead of `curl`, clear the quarantine mark before the first run, or macOS blocks the programs inside:

```sh
xattr -dr com.apple.quarantine ~/.local/share/{{cmd}}
```

## Build from source {#build-from-source}

For contributors. You need [mise](https://mise.jdx.dev), which installs the pinned Erlang, Elixir and Rust versions, plus a C11 compiler, `python3` and, on macOS, the Xcode command line tools (`clang` and `codesign`).

```sh
git clone {{cli_repo}}.git
cd swarm-code-cli
mise install
mise exec -- mix setup
scripts/install.sh
```

`scripts/install.sh` builds the release (including the native terminal helper) and installs it exactly like the one-line installer, into `~/.local/share/{{cmd}}` and `~/.local/bin`; `{{env_prefix}}PREFIX` changes the prefix. Re-run it after pulling changes.

> **Note** The full contributor gate, `mix precommit`, is for maintainers: it re-derives the shared engine from a checkout of the desktop app's repository at a pinned commit, which is not public. Building, installing and running the tests do not need it.

<!-- source: C:scripts/install.sh:4-37, C:README.md:179-186, C:rel/overlays/bin/swarmcode:66-79,165-168, C:scripts/dev/build_release.sh:9-24, C:AGENTS.md:16-19,25,27,42, C:.tool-versions:1-3 -->
<!-- notes:
carried over (the contributor installer today): C:scripts/install.sh:4-15 (prefix, share and bin paths), C:scripts/install.sh:22-25 (replace in place, COOKIE 0600), C:scripts/install.sh:27-37 (the command shim, the PATH hint), C:scripts/install.sh:7-9 (nothing outside the prefix, conversations survive), C:README.md:179-186 (update = re-run), C:rel/overlays/bin/swarmcode:66-79 (--version prints "<cmd> <vsn>", the launcher follows a symlink), C:rel/overlays/bin/swarmcode:165-168 (--help/--version answered by the launcher), C:scripts/dev/build_release.sh:9-24, C:AGENTS.md:16-19,25,27,42 (toolchain, mix setup, precommit needs the desktop checkout), C:.tool-versions:1-3.
post-rename (lane A branch ncode/A, not yet on main): scripts/install.sh:16-17 (NCODE_PREFIX, SWARMCODE_PREFIX still read, share/ncode), :30-41 (ncode and swarmcode shims), rel/overlays/bin/swarmcode:13-16 (the alias note on a terminal's stderr).
blocked on lane F (phase 3): --check --release must not pass until these are re-read from code/install.sh. Depends on lane F's install.sh (plan-v2 §4.6 steps 3, 5-13), re-verify before release: the macOS/arm64 refusal, the pinned SHA-256 check, --uninstall and what it removes, the tarball name and layout ncode-<v>/bin/ncode, the Releases download URL, the PATH hint wording, NCODE_PREFIX in the one-liner.
No signing claim: the only codesign step is the build's ad-hoc signature of the platform helper (C:apps/swarm_code_daemon/mix.exs:50-65); lane A dropped its 'signed' wording (ncode/A 8a70a02).
K11: quarantine applies to browser downloads, not curl (plan-critique K11; inv-docs §9, GUESSED standard macOS behaviour, not re-tested here).
-->
