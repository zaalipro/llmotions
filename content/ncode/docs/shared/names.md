### Names you may still see

{{product}} had a different name before this release. The app and the command are new, but a few places keep the earlier name so your data, your projects and your scripts keep working. You do not need to rename anything.

| What | Name that stays |
|---|---|
| The app's data folder | `{{data_dir}}` |
| The database | `{{db_file}}` |
| The per-project folder | `{{project_dir}}` in each project |
| Your own agent definitions | `~/{{project_dir}}/agents/` |
| The earlier app | `{{old_app}}` (replace it with `{{app}}`) |
| The earlier terminal command | `{{old_cmd}}` (still works, as an alias of `{{cmd}}`) |
| Environment variables | `{{env_prefix}}…` are read first; the older `{{old_env_prefix}}…` names still work |

Two more paths still carry the earlier name:

- Deep research writes each research to `~/.swarmcode/research/<id>/`. <!-- allow: swarmcode -->
- The app's logs are in `~/Library/Logs/SwarmCode/`. <!-- allow: SwarmCode -->

<!-- source: D:lib/swarm_code/desktop.ex:125-142,492-495, D:config/runtime.exs:21-29, D:lib/swarm_code/project_config.ex:9, D:lib/swarm_code/agents.ex:251-252, D:lib/swarm_code/research.ex:17, D:mix.exs:34-45 -->
