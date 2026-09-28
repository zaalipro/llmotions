---
title: Workflow language
description: The workflow file format: the meta map, the functions a workflow may call, safe project reads with host, structured answers, the rules and a worked example.
---

This page is the reference for writing workflows by hand. You do not need it to run workflows, and the assistant can write them for you (`/create-workflow`); read it when you want to adjust one or understand what it does.

{{> shared/workflows}}

## Structured answers with `schema:`

Give `agent/2` a `schema:` and it returns a map you can use in the next step, instead of free text. The schema is a map in JSON-schema style: `type`, `properties`, `items`, `required`, `enum`. If the agent fails or cannot produce a matching answer, you get `nil`, so check with `present?/1`:

```elixir
finding_schema = %{
  type: :object,
  properties: %{
    file: %{type: :string},
    title: %{type: :string},
    severity: %{type: :string, enum: ["low", "medium", "high"]}
  },
  required: [:file, :title, :severity]
}

result = agent("Find the riskiest function in lib/payments.ex", schema: finding_schema, name: "scout")
if present?(result), do: log("#{result.severity}: #{result.title} in #{result.file}")
```

## Replay and resume

A workflow run keeps a journal of every `host` read, every agent result and every answer you gave. When a paused or interrupted run resumes, the program runs again from the top, but every recorded step returns its recorded value at once, so only the unfinished part really runs. This is why a workflow must not read the clock or random numbers directly: a replay would see different values and no longer match its journal. `host(:now)` and `budget()` are recorded, so they are safe.

## Worked example: `review-changes`

The built-in `review-changes` workflow in outline:

```elixir
meta = %{
  name: "review-changes",
  description: "Review the uncommitted changes from several angles and keep only findings that survive an adversarial check",
  phases: ["Review", "Verify", "Report"],
  budget: 48,
  args: %{
    base: %{type: :string, default: "", doc: "Git ref to diff against (empty = working tree vs HEAD)"},
    dimensions: %{type: :list, default: ["correctness", "security", "performance", "maintainability"], doc: "Review lenses, one agent each"}
  }
}

phase("Review")
diff = host(:git_diff, base: args.base)
if String.trim(diff) == "", do: complete(%{summary: "No changes to review.", confirmed: []})
files = host(:changed_files, base: args.base)

reviews =
  panel(args.dimensions, fn dim ->
    agent("You review code changes for #{dim} problems only. …",
      schema: findings_schema, capability: :read_only, name: "review:#{dim}")
  end)

if Enum.all?(reviews, &is_nil/1), do: pause(:no_progress, "Every reviewer failed")

phase("Verify")
# one skeptical agent per finding tries to refute it; only findings with quoted evidence survive

phase("Report")
path = write_report("review.md", report)
complete(%{summary: "… see #{path}", confirmed: confirmed, report: path})
```

What it shows:

- **Arguments with defaults**: `/workflow review-changes base=main` overrides `base`; `dimensions` keeps its four lenses.
- **An early exit**: with nothing to review, `complete/1` ends the run successfully at once.
- **A panel**: four reviewers run at the same time, one per lens, all read-only.
- **A deliberate pause**: if every reviewer failed, the run stops with a reason instead of reporting "no problems".
- **A report**: `write_report/2` saves `review.md` in the run's folder and the result points to it.

The full source is in the library: open **Workflows**, select `review-changes` and scroll to **Source**, or **Duplicate to project** to get an editable copy.

<!-- source: D:priv/workflows/review-changes.exs:1-82, D:lib/swarm_code/workflows/api.ex:87-95,104-147,434-452, D:lib/swarm_code/workflows/host.ex:40-63, D:lib/swarm_code/workflows/smoke.ex:1-65, D:lib/swarm_code_web/live/workflows_live.html.heex:320-400 -->
