---
title: Troubleshooting
description: Fixes for the common problems: the first launch is blocked, the model does not answer, agents cannot write or find a command, search or schedules do not work.
---

The problems people meet first, each with the place in the app that fixes it.

## "Apple could not verify ncode…"

The app is not notarized yet, so macOS asks you to allow it once. Follow [First launch](/docs/desktop/install/#first-launch).

## The model does not answer, or every turn fails

Check the provider in **Settings → Providers & models**:

1. Click **Fetch models** on your provider. If it fails, the error message says why: usually a wrong key or a wrong base URL.
2. Check the base URL. For Anthropic it is `https://api.anthropic.com` (without `/v1`). For OpenAI-compatible services it usually ends in `/v1` (without `/chat/completions`).
3. Check that the model the conversation uses belongs to that provider: look at the composer's model chooser, and at **Settings → General → Defaults** for new conversations. Save the defaults after changing them.
4. A local server (Ollama, LM Studio) must be running before you send.

## Agents cannot change files or run commands

- The error says *blocked by Read-only approval mode*: the project is Read-only. Click **Trust and allow edits** in the banner, or switch the approval mode in the composer. See [Approvals and trust](/docs/desktop/approvals/).
- A step waits and nothing happens: look for an approval card or a question in the transcript, or under **Waiting for you** in the menu bar icon. An approval nobody answers expires after 10 minutes and the agent is told it timed out.

## A command works in Terminal but not for agents

Agents' commands run in a login shell, which reads `.zprofile`, `.profile` or `.bash_profile`, not `.zshrc`. Move the lines that put tools like `node`, `mix` or `cargo` on your `PATH` (mise, asdf, nvm, Homebrew) into `.zprofile`. If a command needs a secret from your environment, add the variable's name to **Keep these variables** in **Settings → Limits**. See [Limits and isolation](/docs/desktop/limits/#the-agents-shell).

## Web search fails

*web_search is not configured* means no search engine is enabled. Add a key for Tavily, Exa, Brave or Serper under **Settings → Deep research → Search providers** and switch it on. See [Web search](/docs/desktop/providers/#web-search).

## An MCP server's tools are missing

In **Settings → MCP servers**, check the server's status. Open its **Recent output** to see why it does not start; fix the command, arguments or environment, then click **Reconnect**. Check that the server and the tool are switched on, and that the server's scope includes the project you are in.

## A scheduled task did not run

- Schedules fire only while the app is running. A run missed while it was closed runs when the app is back, if it is less than 24 hours late and **Catch up missed runs** is on. Otherwise it is recorded as skipped.
- Check that the task is not paused (its menu offers **Enable**).
- Use **Run now** in the task's menu to test it.

## The window disappeared

Closing the window only hides it; your runs keep going. Click the {{product}} icon in the Dock or use the menu bar icon to bring it back.

## `{{cmd}}` refuses to start

The terminal app refuses while the desktop app is running under your account, and exits with status 3. Quit the app first. See [Using with the CLI](/docs/desktop/cli/) (and [the CLI's page on it](/docs/cli/desktop/)).

## The database is large

See [Storage and cleanup](/docs/desktop/storage/). Delete or prune old sessions, then reclaim the disk space.

## Reading the log

The app's log is in your Logs folder: see [Names](/docs/desktop/privacy/#names) for the exact path. Open it in Console or any text editor.

<!-- source: D:lib/swarm_code/engine/policy.ex:16-17,31-32, D:lib/swarm_code/engine/operation.ex:310-311, D:lib/swarm_code/providers.ex:150-162, D:lib/swarm_code/llm/anthropic.ex:94, D:lib/swarm_code/llm/openai.ex:90, D:lib/swarm_code/search.ex:144-158, D:lib/swarm_code_web/live/settings_live.html.heex:1040-1100,1560-1618, D:lib/swarm_code/scheduler.ex:140-155, D:lib/swarm_code_web/live/scheduled_live.ex:530-580, D:lib/swarm_code/desktop.ex:45-47,125-142, D:lib/swarm_code/tray_menu.ex:50-60, C:README.md:122-124, C:apps/swarm_code_cli/lib/swarm_code_cli/release/persisted_session.ex:8,41,955-973, D:lib/swarm_code_web/live/settings_live.html.heex:1114-1142 -->
