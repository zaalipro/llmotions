## 0.2.0 — 2026-10-06 {#v0-2-0}
- desktop: ncode-0.2.0.dmg sha256 57f84ceec543458ea8cb8d1313a73e5c00ee8ecb821aad2b5829b82c249084e9

### What's new in the Mac app

- **Ultra missions.** In Ultra mode the orchestrator plans big work as a mission: a validation contract, features and milestones, an approval card above the message box, parallel isolated workers, scrutiny and user-testing validators, fix rounds, and a Mission Control view. Approving a mission lets its workers run non-dangerous commands without asking. See [Ultra missions](/docs/desktop/missions/).
- **Worker model.** The "Sub agent model" setting is now called Worker model.
- **Validator model.** A new Validator model setting chooses the model that checks a mission's work. By default it is the same as your main model.
- **Speed monitor.** The sidebar shows tokens per second and time to first token next to the memory chip: one row for chat, two rows (Main and Worker) for consensus or swarm runs, and three rows (Orchestrator, Worker and Validator) in Ultra. It shows a live estimate while a reply streams and the exact figure when it finishes.

The command-line app is unchanged and stays at 0.1.0; `install.sh` still installs that version. This developer preview requires macOS 15 or later on Apple silicon. The Mac app is not notarized; follow the [first-launch guide](/docs/desktop/install/#first-launch).

## 0.1.0 — 2026-10-04 {#v0-1-0}
- cli: ncode-0.1.0-darwin-arm64.tar.gz sha256 78585c7667f906e7ef12f6252436213fa17f62da723a857fe46f28d550fd3ed7
- desktop: ncode-0.1.0.dmg sha256 d4634033708c0d7117b15a8110fb761b2c1b66484a93227bb5457c3b4ca1813e

### What's in this preview

- A local-first coding assistant for the terminal and the Mac desktop, sharing conversations and settings on your machine.
- Bring your own Anthropic or OpenAI-compatible provider key and choose models for different roles.
- Work in chat, swarm, consensus, plan or goal mode, with deterministic workflows and multi-step research.
- Keep control with project trust, command approvals, questions and guidance for running agents.
- Connect MCP tools, inspect activity and usage, and rewind file-tool edits to saved checkpoints.

This developer preview requires macOS 15 or later on Apple silicon. The Mac app is not notarized; follow the [first-launch guide](/docs/desktop/install/#first-launch).
