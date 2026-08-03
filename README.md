# coverage

Test coverage tracking for SQM/DVS service flows, tracked as a decision
graph instead of a flat list of Bugzilla test-case titles.

Replaces `fig` (nested JSON decision trees) and `atlas` (per-service
markdown page docs + a separate `test-cases.md` language/login/AGS policy
tracker). This tool intentionally does **not** track language, login
method, or AGS — those don't change which branch of the service flow gets
exercised, so they aren't "coverage" in the sense this tool cares about.
It also doesn't know anything about Bugzilla test cases themselves — it
only tracks WHAT paths exist through a service and WHETHER each one is
covered by at least one test case, nothing more.

## Problem

A flat test-case list (`at-neb | German | AGS=09000002 | Bayern UserPwd |
Proxy | Everything else randomized`) can't answer:

1. What haven't we tested? There's no list of "all possible paths" to diff
   the test-case list against.
2. Where are the real gaps? Some services are flat (a handful of
   independent choices). Most branch — picking a "reason for stay" leads to
   different follow-up questions and required documents. A flat list can't
   represent that, and "everything else randomized" hides exactly the deep
   branches worth checking.

## Model

- **Nodes** are either `decision` (a question/fork point in the flow) or
  `leaf` (a terminal outcome — an upload, a submit, a "service blocked"
  message).
- **Edges** connect a `decision` node to whatever it leads to next, labeled
  with the `choice` that takes you there, plus a `covered: true/false`
  flag.
- Non-branching steps in between (enter a date, enter a duration, fill a
  field) are **not** modeled as nodes — they don't fork, so there's nothing
  to cover. They get folded into the edge/leaf label instead. Only model a
  node when the flow actually forks or terminates.
- **`covered` is set by hand**, same as fig's per-node `covered: true/false`
  toggle — flip an edge to `true` once you've written and confirmed a
  Selenium test case actually exercises that choice. Nothing in this repo
  infers coverage automatically from test runs or Bugzilla.

See `services/at-neb.yaml` (flat: one decision, two leaves) and
`services/at-erw.yaml` (branching: a real multi-decision chain with
several "service blocked" dead ends) for worked examples.

## Schema

```yaml
service: <id, matches filename>
description: <one line>

nodes:
  some_id: {type: decision, label: "Question shown to the user"}
  other_id: {type: leaf, label: "Terminal action, e.g. upload doc"}

edges:
  - {from: some_id, to: other_id, choice: "Answer that leads here", covered: false}
```

One YAML file per service under `services/`, not one shared file — keeps
each file small and diffable regardless of how large the whole suite gets.

## Usage

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

.venv/bin/python3 build.py                 # report for every service
.venv/bin/python3 build.py at-erw           # report for one service
.venv/bin/python3 build.py at-erw --mermaid # emit a Mermaid flowchart instead
```

The report prints edge coverage (`hit/total`, %) and a branch-gap table:
decision points where some but not all outgoing choices are marked
`covered: true` — the thing a flat list hides completely. `--mermaid`
renders the same graph as a flowchart (solid arrow = covered, dashed =
not), so there's no separate diagram to keep in sync by hand.

## Workflow

1. Walk a service's real flow once; each fork becomes a `decision` node,
   each terminal outcome a `leaf`, each choice an `edge`.
2. Run `build.py` to see edge coverage % and the branch-gap table.
3. Use the gap table to decide what to test next.
4. Once a Selenium test case is written and confirmed to exercise a given
   choice, flip that edge's `covered` to `true` by hand.
5. If the flow itself changes, update the same YAML file's `nodes`/`edges`
   so the doc and the test code never drift apart.

## Status

`services/at-neb.yaml` and `services/at-erw.yaml` have real, accurate
`nodes`/`edges` (migrated from the old `fig` JSON trees). All edges
currently `covered: false` — flip them by hand as coverage is confirmed
per service, service by service.
