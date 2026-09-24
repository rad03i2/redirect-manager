from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from .core import export_rules, load_rules, resolve_chain, validate_rules

VERSION = "1.0.0"

def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="redirect-manager", description="Validate, resolve, and export redirect rules.")
    p.add_argument("--version", action="version", version=f"Redirect Manager {VERSION} — Radwan Abdulhadi Ahmed / @rad03i2")
    sub = p.add_subparsers(dest="command", required=True)
    v = sub.add_parser("validate", help="validate a CSV or JSON rule file")
    v.add_argument("file"); v.add_argument("--json", action="store_true", dest="as_json")
    r = sub.add_parser("resolve", help="show the chain for one source path")
    r.add_argument("file"); r.add_argument("source"); r.add_argument("--max-hops", type=int, default=20)
    e = sub.add_parser("export", help="export validated rules")
    e.add_argument("file"); e.add_argument("--format", required=True, choices=["nginx", "apache", "netlify"]); e.add_argument("--output")
    return p

def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        rules = load_rules(args.file)
        if args.command == "validate":
            report = validate_rules(rules)
            if args.as_json:
                print(json.dumps(report.as_dict(), ensure_ascii=False, indent=2))
            elif report.ok:
                print(f"OK: {len(rules)} redirect rules validated; no errors found.")
            else:
                for f in report.findings:
                    where = f"rule {f.rule_index}: " if f.rule_index else ""
                    print(f"ERROR [{f.code}] {where}{f.message}")
            return 0 if report.ok else 1
        if args.command == "resolve":
            print(" -> ".join(resolve_chain(rules, args.source, args.max_hops)))
            return 0
        text = export_rules(rules, args.format)
        if args.output:
            Path(args.output).write_text(text, encoding="utf-8")
            print(f"Wrote {len(rules)} rules to {args.output}")
        else:
            sys.stdout.write(text)
        return 0
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__": raise SystemExit(main())
