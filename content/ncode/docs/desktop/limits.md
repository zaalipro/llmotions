---
title: Limits and isolation
description: Set how many agents run at once, how deep and how long, command timeouts and workflow budgets, isolate sub-agents in their own copy, and shape the agents' shell.
---

Limits keep a runaway swarm from spending forever, and isolation keeps parallel agents from editing the same files at once. Both live in **Settings → Limits**; change the fields and click **Save limits**.

## Agent limits

| Setting | Default | What it bounds |
|---|---|---|
| Max concurrent agents | 4 | how many sub-agents of one swarm or one chat turn work at the same time; two runs in two conversations each get this many |
| Max agent depth | 2 | how many levels of agents may start agents |
| Max agent turns | 60 | the steps one agent may take before it must answer |
| Sub-agent time limit (s) | 1800 (30 minutes) | a sub-agent that runs longer is stopped and its partial work reported; 0 means no limit |
| Workflow agent budget | 128 | the most agents one workflow run may start in total |
| Max live workflow agents | 16 | how many of them work at the same time; each one uses memory |
| Command timeout (ms) | 120,000 (2 minutes) | the floor for every shell command; an agent may ask for more for one command, never less |
| Tool timeout (s) | 120 | web fetch, web search and MCP calls |

A command that is still running after 10 seconds is not killed: it moves to the background, the agent gets its output so far and can check on it or stop it later. See [Watching agents work](/docs/desktop/agents/#commands-left-running).

## Isolating sub-agents

With **Isolate sub-agents in git worktrees** on (the default), sub-agents in a git project can work in their own copy of the project, so two agents editing at once never overwrite each other. Their changes wait on a branch until they are merged back into the project, and the **Changes** view shows them under **Branches**.

**Isolation backend**:

- **Auto** (default): an APFS clone when the disk supports it, otherwise a git worktree.
- **APFS clone**: a fast copy-on-write copy of the project folder.
- **Git worktree**: a separate git worktree.

An isolated agent's finished changes are kept as a patch under `{{project_dir}}/isolation/` in the project until they are merged; {{product}} removes the ones nothing needs any more.

## The agents' shell

Commands agents run go through your shell, with a few safeguards:

- **Hide secrets from commands the agent runs** (on): environment variables whose names look like secrets are removed before a command starts. **Keep these variables** lists the exceptions (by default `GITHUB_TOKEN, GH_TOKEN`, so `git` and `gh` keep working).
- **Shell (blank = detect)**: the shell to use; blank uses the shell in your `$SHELL`.
- **Run commands in a login shell** (on): the shell reads your login files (`.zprofile`, `.profile`, `.bash_profile`), not `.zshrc`. Put `PATH` changes for tools such as mise, asdf, nvm or Homebrew there, so `node`, `mix` or `cargo` are found.

{{> shared/tools}}

## Approved commands

The last part of **Settings → Limits** lists the command families you allowed with **Always allow**, per project. See [Approvals and trust](/docs/desktop/approvals/#forgetting-remembered-commands).

<!-- source: D:lib/swarm_code_web/live/settings_live.html.heex:1415-1660, D:lib/swarm_code/settings/setting.ex:33-56,105-115,124, D:lib/swarm_code/tools/run_command.ex:26,697-703, D:lib/swarm_code/engine/isolation.ex:1-25, D:lib/swarm_code_web/components/swarm_pane.ex:3482 -->
