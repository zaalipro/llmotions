---
title: Settings
description: A map of the ncode Settings window, section by section, with what each one controls and where it is explained in detail.
---

Open Settings with [[⌘]]+[[,]], the gear at the bottom of the rail, or **File → Settings…** in the menu bar. The sections are listed on the left; click one to jump to it. Most changes apply at once; forms with several fields have their own **Save** button.

![The Settings window in Carbon dark at Appearance: the section list on the left with Appearance marked, the eight theme chips with Carbon selected, Dark on, and the layout, window and sidebar options.](/assets/shots/desktop/settings-overview.webp)

## General

The **Defaults** card: which models new conversations start with (**Chat model**, **Worker model**, **Validator model** (blank means **Same as main model**), **Default scheduled model**, **Default workflow model**, **Implementer model (consensus)**) and the default reasoning effort for chat, scheduled tasks, workflows, swarms and the implementer. Click **Save defaults** after changing a model. See [Providers, models and web search](/docs/desktop/providers/).

## Deep research

The **Search providers** used by all web searches (engines and readers, their keys and their order), the default research level, limits, domain filters, the lead, worker and reporter models, and when the designed report is built. See [Providers, models and web search](/docs/desktop/providers/#web-search) and [Deep research](/docs/desktop/research/).

## Appearance

Theme and dark or light mode, **Reduce motion**, the default consensus card layout, **Bring the window to front when a run finishes**, **Show global scheduled tasks**, and whether the "Worked for…" and "Thinking" disclosures start open. See [Themes](/docs/desktop/themes/).

## Providers & models

Your model endpoints: add, edit, delete, **Fetch models**, and the effort levels each provider offers. See [Providers, models and web search](/docs/desktop/providers/).

## Pricing

A price per million tokens for each model (input, output, cache read, cache write) and its context window, so runs show their cost.

## MCP servers

Add MCP servers, scope them to a project, switch them or single tools on and off, reconnect them. See [MCP servers](/docs/desktop/mcp/).

## Memory

Edit a project's memory and your global memory. See [Instructions, memory and project config](/docs/desktop/instructions/).

## Storage

How much space {{product}}'s data takes, **Clean up…**, and retention. See [Storage and cleanup](/docs/desktop/storage/).

## Commands

Your custom slash commands, project and global: **New command**, **Open project commands**, **Open global commands**. See [Commands, agents and skills](/docs/desktop/extend/).

## Keybindings

Change the nine app shortcuts. See [Keyboard shortcuts](/docs/desktop/keys/).

## Agents

The agent definitions {{product}} found (bundled, yours and the project's), read-only. See [Commands, agents and skills](/docs/desktop/extend/).

## Limits

How many agents may run, how deep and how long; command and tool timeouts; workflow budgets; sub-agent isolation; the environment of the agents' shell; and the list of approved commands. See [Limits and isolation](/docs/desktop/limits/) and [Approvals and trust](/docs/desktop/approvals/).

## Budget

**Monthly budget (USD)**: a spend target. The bar on the Usage history page fills against it; nothing is blocked when it runs out.

## Settings from a project

A project can bring hooks and profiles in its own file. See [Instructions, memory and project config](/docs/desktop/instructions/#the-project-file).

<!-- source: D:lib/swarm_code_web/live/settings_live.ex:34-48,52-60, D:lib/swarm_code_web/live/settings_live.html.heex:57-210,211-600,605-760,750-898,899-998,999-1149,1150-1258,1259-1325,1325-1386,1386-1415,1415-1660,1660-1700, D:lib/swarm_code/menu_bar.ex:95-100, D:lib/swarm_code_web/components/frame.ex:465-471, D:lib/swarm_code_web/components/storage_section.ex:51-64 -->
