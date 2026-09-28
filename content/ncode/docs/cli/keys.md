---
title: Keyboard reference
description: Every key of the terminal session, by context, generated from the key table the program itself uses.
---

The session is keyboard-first and built around the composer. A few rules explain most of the table below:

- **Letters always type.** In the composer a letter is text, never a command. Commands start with `/`. Single-letter keys act where no text is being typed, such as select mode, pickers and dialogs, or on an approval card while your draft is empty.
- **[[Esc]] stops or closes.** It stops the streaming turn, or closes the top layer; it never moves the focus.
- **[[Ctrl]]+[[C]] never surprises you.** It closes a layer, else clears the draft ([[Ctrl]]+[[Z]] restores it), else stops the turn. Only two presses with nothing left to cancel, within 1.5 seconds, quit.
- **Help is on screen.** [[F1]] (or `?` outside a text field) shows the keys of the place you are in.

## Terminal notes

- Nothing essential needs [[Alt]], because Alt is unreliable in some macOS terminals (Ghostty in particular). [[Alt]]+[[Enter]] (queue), for example, is also [[Tab]] while a turn runs.
- [[Ctrl]]+[[K]] is never bound, because window managers use it.
- [[Ctrl]]+[[Shift]]+[[Z]] (redo) needs a terminal that reports Ctrl with Shift.
- Any action can be rebound in Settings → Keys & input, or listed from a shell with `{{cmd}} config keys`.

## Vim keys

Set `{{env_prefix}}KEYMAP=vim` before starting, pick **Vim mode** in the [[Ctrl]]+[[P]] palette, or set **Keymap** in Settings → Keys & input. The composer then has vim's NORMAL and VISUAL modes; their keys are the two "vim" contexts below.

## Every key

{{> import/keybindings}}

<!-- source: C:docs/keybindings.md:1-13, C:AGENTS.md:165-177, C:README.md:70-93, C:docs/settings.md:146-155, C:apps/swarm_code_cli/lib/swarm_code_cli/release/config_command.ex:50 -->
