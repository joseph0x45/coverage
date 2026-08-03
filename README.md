# coverage

Test-case coverage tracking for SQM/DVS service flows, tracked as a
decision graph instead of a flat list of Bugzilla test-case titles.

Replaces `fig` (nested JSON decision trees) and `atlas` (per-service
markdown page docs + a separate `test-cases.md` language/login/AGS policy
tracker). This tool intentionally does **not** track language, login
method, or AGS — those don't change which branch of the service flow gets
exercised, so they aren't "coverage" in the sense this tool cares about.
What it tracks is: which decisions in the actual flow have been exercised,
and by which choice.

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
  with the `choice` that takes you there.
- Non-branching steps in between (enter a date, enter a duration, fill a
  field) are **not** modeled as nodes — they don't fork, so there's nothing
  to cover. They get folded into the edge/leaf label instead. Only model a
  node when the flow actually forks or terminates.
- **Test cases** are a `path`: the list of edges that test case's run
  actually walked, including edges crossed incidentally on the way to
  whatever the test case's "main point" was — that's what makes edge
  coverage numbers meaningful rather than only counting deliberate targets.

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
  - {from: some_id, to: other_id, choice: "Answer that leads here"}

test_cases:
  - id: TC-101                # Bugzilla ID
    bugzilla: "<original title, for reference>"
    path: [[some_id, other_id], ...]   # every edge this test case walks
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
decision points where some but not all outgoing choices have been
exercised by any test case — the thing a flat list hides completely.

## Workflow

1. Walk a service's real flow once; each fork becomes a `decision` node,
   each terminal outcome a `leaf`, each choice an `edge`.
2. Map existing Bugzilla test cases onto `test_cases` entries: an `id` and
   a `path` of every edge that test case's run crosses.
3. Run `build.py` to get edge coverage % and the branch-gap table.
4. Use the gap table to decide what new test cases to actually write —
   coverage-driven rather than ad hoc.
5. As new Selenium tests get written or existing ones change, update the
   same YAML file's `nodes`/`edges`/`test_cases` so the doc and the test
   code never drift apart.

## Status

`services/at-neb.yaml` and `services/at-erw.yaml` have real, accurate
`nodes`/`edges` (migrated from the old `fig` JSON trees), but empty
`test_cases` — filling those in from the real Bugzilla test-case list is
the next real task, one service at a time, same as any other file-by-file
pass in this project.
