---
title: Quickstart
description: Add your own model provider key, open a project, trust it and send your first message in about five minutes.
---

> **Note** This is a preview of the docs. The download and the one-line installer go live with the 0.1.0 release; until then these steps describe how they will work.

This page takes you from a freshly installed app to a first finished task. You need {{product}} [installed](/docs/desktop/install/) and an API key from a model provider: Anthropic, or any service with an OpenAI-compatible API.

## 1. Add your provider key

1. Open **Settings**: press [[⌘]]+[[,]] or click the gear at the bottom of the narrow bar on the left.
2. Go to **Providers & models** and click **Add provider**.
3. Fill in the form:
  - **Name**: anything you like, for example `anthropic`.
  - **Kind**: **Anthropic** for Anthropic's API; **OpenAI-compatible** for everything else.
  - **Base URL**: for Anthropic `https://api.anthropic.com`; for OpenAI `https://api.openai.com/v1`; for another service, the base URL from its documentation, usually ending in `/v1`.
  - **API key**: paste your key.
4. Click **Save provider**.
5. On your new provider's row, click **Fetch models**. {{product}} asks the endpoint for its model list. If models appear, the key works.

<!-- shot: desktop/quickstart-provider-form.png | Settings → Providers & models with the Add provider form open: Name "anthropic", Kind Anthropic, Base URL https://api.anthropic.com, API key field masked -->

> **Note** A fresh install already lists one provider with an empty key. Ignore it: the steps above add your own, and step 2 below makes new conversations use yours. You can delete that row once your provider works.

> **Tip** A local server such as Ollama (`http://localhost:11434/v1`) or LM Studio (`http://localhost:1234/v1`) works too: choose OpenAI-compatible and leave the key empty.

## 2. Make it the default

1. In Settings, go to **General**. The **Defaults** card lists the models new conversations start with.
2. Pick one of your provider's models as the **Chat model** and the **Sub agent model** (the model helper agents use), then click **Save defaults**.

Each conversation can still switch models later from the composer.

## 3. Open a project

1. Close Settings and click **Add project** (in the sidebar or on the start screen).
2. Click **Choose folder…** and pick a folder with code, or type its path. A git repository works best: it enables isolated agents and the Changes view. File snapshots and rewind work in any folder.
3. Click **Create**.

A banner appears above the message box: the project is read-only until you trust it.

## 4. Trust the project

Click **Trust and allow edits** in the banner. Trusting a folder means:

- agents may write files there, and run commands with your approval;
- its instruction files (such as `AGENTS.md`) and hooks are used.

Only trust folders whose contents you trust. Until you do, agents can only read. See [Approvals and trust](/docs/desktop/approvals/).

## 5. Send a message

Click one of the suggestions, or type a request in the message box, for example:

```text
Explain how this project is organised and where the entry point is.
```

Press [[Return]] to send ([[Shift]]+[[Return]] adds a new line). The answer streams into the transcript, and the agents pane on the right shows each tool call as it happens.

<!-- shot: desktop/quickstart-empty-state.png | the start screen of a newly opened project: the greeting, "Ready when you are — (project name) is open.", and the four suggestion cards -->

## 6. Approve a command

Ask for something that runs a command:

```text
Run the test suite and tell me what fails.
```

When an agent wants to run a command that needs approval, a card appears with the command and these buttons:

- **Approve** runs it once.
- **Deny** refuses it; the agent carries on without it.
- **Deny & stop** refuses it and stops the run.
- **Always allow "…"** runs it and remembers that command family for this project.

<!-- shot: desktop/quickstart-approval.png | an approval card in the transcript for "mix test" with Approve, Deny, Deny & stop and Always allow "mix test" -->

## 7. Try a swarm

For a bigger task, let several agents work at once:

```text
/swarm add input validation to every form in this app
```

A lead agent splits the work, sub-agents do the parts in parallel, and the lead checks and reports. Watch them in the agents pane. See [Swarms](/docs/desktop/swarms/).

## Where your work is saved

- File changes land in your project folder, like edits you make yourself. Every file an agent changes is snapshotted first, so you can [rewind](/docs/desktop/rewind/) a turn.
- Conversations, settings and keys are saved in a local database on your Mac. See [Data and privacy](/docs/desktop/privacy/).

## Next

- [A tour of the window](/docs/desktop/tour/)
- [Composer, modes and goals](/docs/desktop/composer/)
- [Providers, models and web search](/docs/desktop/providers/)

<!-- source: D:lib/swarm_code_web/components/frame.ex:465-471, D:lib/swarm_code_web/live/settings_live.ex:34-48, D:lib/swarm_code_web/live/settings_live.html.heex:57-75,93-99,750-898, D:lib/swarm_code/llm/anthropic.ex:94,229, D:lib/swarm_code/llm/openai.ex:90,439, D:lib/swarm_code_web/live/workspace_live/workspace.html.heex:118-130,236-246,630-652, D:lib/swarm_code/projects.ex:175-189, D:lib/swarm_code_web/components/chat.ex:19-47,330-340,765-812, D:assets/js/hooks.js:880, D:README.md:23-29, D:lib/swarm_code/providers.ex:124-145, D:lib/swarm_code/bootstrap.ex:32,47, D:lib/swarm_code/checkpoints.ex:1-7,196-202 -->
