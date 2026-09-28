### What a workflow is

A workflow is a small program that runs agents in a fixed, repeatable order: first review, then verify, then report, for example. It is written in Elixir as a single `.exs` file: a `meta` map followed by plain calls.

```elixir
meta = %{
  name: "summarize-changes",
  description: "Summarize the uncommitted changes in plain words",
  phases: ["Read", "Write"],
  budget: 4,
  args: %{base: %{type: :string, default: "", doc: "Git ref to compare with"}}
}

phase("Read")
files = host(:changed_files, base: args.base)
if files == [], do: complete(%{summary: "Nothing changed."})

phase("Write")
summary = agent("Summarize the changes in these files: #{Enum.join(files, ", ")}", name: "writer")
path = write_report("summary.md", summary || "No summary.")
complete(%{summary: "Wrote #{path}"})
```

### The `meta` map

| Key | Meaning |
|---|---|
| `name` | the workflow's name; it also becomes a slash command |
| `description` | one line shown in lists |
| `phases` | the phase titles, in order, shown as the run's progress |
| `budget` | the most agents one run may start |
| `args` | named arguments, each with `type`, `default` and `doc`; the program reads them as `args.<name>` |

### Functions

| Function | What it does |
|---|---|
| `phase(title)` | marks the start of a phase |
| `log(text)` | adds a line to the run log (up to 500 lines) |
| `agent(prompt, opts)` | runs one agent and returns its final text, or `nil` if it failed |
| `panel(items, fun)` | runs `fun` for every item at the same time, one agent each, and returns the results in item order (`nil` for a failed slot) |
| `host(op, opts)` | reads the project safely (see below) |
| `present?(x)` | `true` when `x` is not `nil`; filter panel results with it |
| `budget()` | `%{total:, spent:, remaining:}` agent slots of this run |
| `fingerprint(value)` | a stable 16-character fingerprint, for removing duplicates |
| `json_encode(value)` | the value as compact JSON |
| `write_report(filename, text)` | saves a report in the run's folder and returns its path |
| `read_report(filename)` | reads a report back, or `nil` |
| `last_error()` | the error of the most recent failed agent call, or `nil` |
| `integrate(result)` | merges an isolated agent's changes into the project |
| `await_user(question, opts)` | pauses the run with a question and returns your answer when you resume; `options:` offers choices |
| `pause(kind, message)` | stops the step with a reason, for example `pause(:no_progress, "Every reviewer failed")` |
| `complete(value)` | ends the run successfully with `value` as its result |

`agent/2` options:

- `schema:` a JSON-schema-like map; the agent must answer with a matching object, which you get back as a map;
- `name:` the label shown for the agent;
- `capability:` what the agent may do: `:read_only` (the default), `:read_write` (may edit files), `:execute` (may also run commands) or `:none` (no tools).

### Reading the project with `host`

A workflow never touches files or the shell directly. It asks `host(op, opts)`, and every answer is recorded so a run can be replayed and resumed exactly:

`:changed_files`, `:git_diff`, `:git_log`, `:glob`, `:files`, `:subdirs`, `:read_file`, `:list_dir`, `:exists?`, `:dir?`, `:grep`, `:now`.

### Rules a workflow must follow

Before a workflow is saved or run, a smoke check parses it, checks its arguments and runs the path they select with stand-in agents. It rejects:

- direct file-system and shell access: the `File` module, `System.cmd`, `System.shell`, `:os.cmd`, `Path.expand`, `Path.absname`, `Path.wildcard` (use `host` instead);
- anything that differs between two runs: clocks, random numbers, unique integers, `Process.sleep` (use `host(:now)` for the time);
- a path that finishes without starting a single agent, when checked against a real project.

A running script that grows past 512 MB of memory is stopped.

<!-- source: D:lib/swarm_code/workflows/api.ex:60-460, D:lib/swarm_code/workflows/host.ex:49-63, D:lib/swarm_code/workflows/smoke.ex:1-65, D:lib/swarm_code/tools.ex:231-247, D:lib/swarm_code/engine/run_server.ex:1076-1077, D:lib/swarm_code/workflows/runner.ex:340,542, D:priv/workflows/review-changes.exs:1-82 -->
