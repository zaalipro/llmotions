### Scheduled tasks

A scheduled task runs a prompt on its own at the times you choose, each time in a fresh conversation.

| Field | Choices |
|---|---|
| Kind | Chat, Swarm or Workflow (a saved workflow with its arguments) |
| Mode | Build or Plan |
| Schedule | once (a date and time), daily (a time of day, 09:00 by default), weekly (days and a time), monthly (a day of the month, 1 to 31) or a cron expression such as `0 9 * * mon-fri` |
| Model and effort | the scheduled defaults, or the task's own |
| Project | the project the task runs in |
| Colour | orange, violet, teal, green, pink or yellow |

### When tasks fire

- Only the desktop app fires schedules. It checks every 30 seconds while it is open, even with its window closed. If the app is not running, nothing fires.
- **Catch up missed runs** is on by default: a run missed while the app was closed runs when the app is back, as long as it is less than 24 hours late. Missed runs at startup start 10 seconds apart.
- With catch-up off, a run more than 2 minutes late is recorded as skipped. A run more than 24 hours late is always skipped.

<!-- source: D:lib/swarm_code/scheduled/task.ex:12-39, D:lib/swarm_code/scheduler.ex:1-19,140-155, D:lib/swarm_code_web/live/scheduled_live.html.heex:310-600 -->
