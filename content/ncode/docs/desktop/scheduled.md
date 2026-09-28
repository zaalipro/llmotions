---
title: Scheduled tasks
description: Run a prompt, a swarm or a workflow on its own every day, week or month, or on a cron schedule, and understand when missed runs catch up.
---

A scheduled task is a prompt {{product}} runs by itself: a nightly dependency check, a Monday summary of last week's commits, a review of the day's changes every evening. Each time it fires, it opens a fresh conversation in the task's project and runs there, so you can read the result like any other conversation.

> **Note** Schedules fire only while the {{product}} app is running. Closing its window is fine; quitting it is not. The `{{cmd}}` terminal app can manage tasks but never fires them.

## Creating a task

1. Click **Scheduled tasks** in the rail.
2. Click **New scheduled task** (the **+** by the calendar), or **New task from a description** to have the assistant fill in the form from a sentence.
3. Fill in the form:
   - **Name** and **Prompt**: what the task is called and what it should do.
   - **Kind**: **Chat**, **Swarm** or **Workflow** (then pick the workflow and its arguments).
   - **Mode**: **Build**, or **Plan** for a read-only plan.
   - **Project** the task runs in, and optionally a **Model** and **Effort** of its own.
   - **Schedule**: once, daily, weekly, monthly or cron, with its date, time, days or expression.
   - A colour, to tell tasks apart in the calendar and the sidebar.
4. Click **Save task**.

<!-- shot: desktop/scheduled-form.png | the New scheduled task dialog filled in: name "Nightly dependency check", kind Chat, mode Plan, schedule Daily at 02:00, colour teal -->

{{> shared/scheduled}}

## Following a task's runs

The Scheduled tasks page shows a calendar and the tasks of the selected day. Each task's menu has **Run now**, **Edit**, **Pause** (or **Enable** for a paused task) and **Delete**. You can filter the calendar by project and export your tasks as JSON.

In the Chats sidebar, **Scheduled tasks** lists each task with its latest runs underneath; click a run to open its conversation. Tasks are grouped by project; tasks without a project appear under a **Global** group, which you can hide in **Settings → Appearance** (Show global scheduled tasks).

<!-- shot: desktop/scheduled-calendar.png | the Scheduled tasks page with a month calendar showing coloured task dots and the selected day's three tasks listed on the right -->

## Tips

- Use **Plan** mode for tasks that should only report, so nothing changes while you are away.
- A task that changes files still follows the project's approval mode. In Auto, a command that needs approval waits for you (for up to 10 minutes), so let unattended tasks read and report, or give them commands you have already approved with **Always allow**.
- Scheduled runs use the **Default scheduled model** from Settings unless the task has its own.

<!-- source: D:lib/swarm_code_web/live/scheduled_live.html.heex:39-60,130-232,310-600, D:lib/swarm_code_web/live/scheduled_live.ex:530-580,832-840, D:lib/swarm_code_web/components/frame.ex:891-1011,2463, D:lib/swarm_code/desktop.ex:45-47, D:lib/swarm_code/engine/questions.ex:10-13, D:lib/swarm_code_web/live/settings_live.html.heex:93-107,715-730, C:apps/swarm_code_daemon/lib/swarm_code/daemon/boot.ex:14 -->
