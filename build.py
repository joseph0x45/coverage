#!/usr/bin/env python3
import argparse
import pathlib
import sys

import yaml

SERVICES_DIR = pathlib.Path(__file__).parent / "services"


def load(path: pathlib.Path) -> dict:
    data = yaml.safe_load(path.read_text())
    data.setdefault("nodes", {})
    data.setdefault("edges", [])
    data["description"] = data.get("description", "").strip()
    for node in data["nodes"].values():
        node["label"] = node.get("label", "").strip()
    for edge in data["edges"]:
        edge.setdefault("covered", False)
    return data


def edge_coverage(data: dict) -> tuple[int, int]:
    total = len(data["edges"])
    hit = sum(1 for e in data["edges"] if e["covered"])
    return hit, total


def branch_gaps(data: dict) -> list[dict]:
    by_node: dict[str, list[dict]] = {}
    for e in data["edges"]:
        by_node.setdefault(e["from"], []).append(e)

    gaps = []
    for node_id, node in data["nodes"].items():
        if node.get("type") != "decision":
            continue
        outgoing = by_node.get(node_id, [])
        missing = [e["choice"] for e in outgoing if not e["covered"]]
        if missing:
            gaps.append({
                "node": node_id,
                "label": node.get("label", ""),
                "total_choices": len(outgoing),
                "missing_choices": missing,
            })
    return gaps


def print_report(data: dict) -> None:
    hit, total = edge_coverage(data)
    pct = (hit / total * 100) if total else 0.0
    print(f"== {data['service']} ==")
    print(f"{data.get('description', '').strip()}")
    print(f"Edge coverage: {hit}/{total} ({pct:.0f}%)")

    gaps = branch_gaps(data)
    if not gaps:
        if total:
            print("No branch gaps.")
        return

    print("\nBranch gaps (decision points with uncovered choices):")
    for gap in gaps:
        tested = gap["total_choices"] - len(gap["missing_choices"])
        print(f"  - {gap['node']} ({tested}/{gap['total_choices']} covered): "
              f"missing {', '.join(gap['missing_choices'])}")


def to_mermaid(data: dict) -> str:
    lines = ["flowchart TD"]
    for node_id, node in data["nodes"].items():
        label = node.get("label", node_id).replace('"', "'")
        shape = f'{{"{label}"}}' if node.get("type") == "decision" else f'["{label}"]'
        lines.append(f"    {node_id}{shape}")
    for e in data["edges"]:
        style = "-->" if e["covered"] else "-.->"
        choice = e.get("choice", "")
        lines.append(f'    {e["from"]} {style}|"{choice}"| {e["to"]}')
    return "\n".join(lines)


def to_html(data: dict) -> str:
    hit, total = edge_coverage(data)
    pct = (hit / total * 100) if total else 0.0
    mermaid = to_mermaid(data)
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{data['service']} coverage</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<style>
  body {{ font-family: sans-serif; margin: 2rem; }}
  h1 {{ margin-bottom: 0; }}
  p.desc {{ color: #555; margin-top: 0.25rem; }}
  p.stats {{ font-weight: bold; }}
</style>
</head>
<body>
<h1>{data['service']}</h1>
<p class="desc">{data.get('description', '')}</p>
<p class="stats">Edge coverage: {hit}/{total} ({pct:.0f}%) &mdash; solid = covered, dashed = not covered</p>
<pre class="mermaid">
{mermaid}
</pre>
<script>mermaid.initialize({{startOnLoad: true}});</script>
</body>
</html>
"""


def to_markdown(data: dict) -> str:
    hit, total = edge_coverage(data)
    pct = (hit / total * 100) if total else 0.0
    mermaid = to_mermaid(data)
    gaps = branch_gaps(data)
    gap_lines = "\n".join(
        f"- `{gap['node']}` ({gap['total_choices'] - len(gap['missing_choices'])}/{gap['total_choices']} covered): "
        f"missing {', '.join(gap['missing_choices'])}"
        for gap in gaps
    ) or "No branch gaps."
    return f"""# {data['service']}

{data.get('description', '')}

**Edge coverage:** {hit}/{total} ({pct:.0f}%) — solid arrow = covered, dashed = not covered

```mermaid
{mermaid}
```

## Branch gaps

{gap_lines}
"""


def iter_service_files(names: list[str]) -> list[pathlib.Path]:
    if not names:
        return sorted(SERVICES_DIR.glob("*.yaml"))
    return [SERVICES_DIR / f"{name}.yaml" for name in names]


def main() -> None:
    parser = argparse.ArgumentParser(description="Coverage report over service decision graphs")
    parser.add_argument("service", nargs="*", help="service id(s), e.g. at-erw (default: all)")
    parser.add_argument("--mermaid", action="store_true", help="print a Mermaid flowchart instead of the report")
    parser.add_argument("--html", metavar="DIR", help="write a viewable HTML flowchart per service into DIR instead of printing")
    parser.add_argument("--md", metavar="DIR", help="write a Markdown file per service into DIR (renders as a Mermaid diagram on GitHub) instead of printing")
    args = parser.parse_args()

    for path in iter_service_files(args.service):
        if not path.exists():
            sys.exit(f"no such service file: {path}")
        data = load(path)
        if args.html:
            out_dir = pathlib.Path(args.html)
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / f"{data['service']}.html"
            out_path.write_text(to_html(data))
            print(f"wrote {out_path}")
        elif args.md:
            out_dir = pathlib.Path(args.md)
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / f"{data['service']}.md"
            out_path.write_text(to_markdown(data))
            print(f"wrote {out_path}")
        elif args.mermaid:
            print(to_mermaid(data))
        else:
            print_report(data)
            print()


if __name__ == "__main__":
    main()
