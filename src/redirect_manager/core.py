from __future__ import annotations
import csv, json
from dataclasses import dataclass
from pathlib import Path

ALLOWED_STATUS = {301, 302, 307, 308}

@dataclass(frozen=True)
class RedirectRule:
    source: str
    target: str
    status: int = 301

@dataclass(frozen=True)
class Finding:
    code: str
    message: str
    rule_index: int | None = None

@dataclass(frozen=True)
class ValidationReport:
    findings: tuple[Finding, ...]
    @property
    def ok(self) -> bool:
        return not self.findings
    def as_dict(self) -> dict:
        return {"ok": self.ok, "errors": [f.__dict__ for f in self.findings]}

def _path(value: object, field: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    value = value.strip()
    if not value.startswith("/") or value.startswith("//"):
        raise ValueError(f"{field} must be a site path beginning with one slash")
    if any(ord(c) < 32 for c in value):
        raise ValueError(f"{field} contains control characters")
    return value

def _rule(item: dict, index: int) -> RedirectRule:
    try:
        source = _path(item.get("source"), "source")
        target = _path(item.get("target"), "target")
        raw = item.get("status", 301)
        status = int(raw) if str(raw).strip() else 301
    except (TypeError, ValueError) as exc:
        raise ValueError(f"rule {index}: {exc}") from exc
    return RedirectRule(source, target, status)

def load_rules(path: str | Path) -> list[RedirectRule]:
    path = Path(path)
    if not path.is_file():
        raise ValueError(f"input file does not exist: {path}")
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("input must be UTF-8 text") from exc
    if path.suffix.lower() == ".json":
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON: {exc.msg}") from exc
        if not isinstance(data, list) or not all(isinstance(x, dict) for x in data):
            raise ValueError("JSON root must be an array of rule objects")
        return [_rule(x, i) for i, x in enumerate(data, 1)]
    if path.suffix.lower() == ".csv":
        reader = csv.DictReader(text.splitlines())
        if not reader.fieldnames or not {"source", "target", "status"}.issubset(reader.fieldnames):
            raise ValueError("CSV must contain source,target,status headers")
        return [_rule(x, i) for i, x in enumerate(reader, 1)]
    raise ValueError("unsupported input type; use .csv or .json")

def validate_rules(rules: list[RedirectRule]) -> ValidationReport:
    findings: list[Finding] = []
    seen: dict[str, tuple[int, RedirectRule]] = {}
    for i, rule in enumerate(rules, 1):
        if rule.status not in ALLOWED_STATUS:
            findings.append(Finding("invalid-status", f"unsupported status {rule.status}", i))
        if rule.source == rule.target:
            findings.append(Finding("self-redirect", "source and target are identical", i))
        if rule.source in seen:
            old_i, old = seen[rule.source]
            code = "duplicate-source" if (old.target, old.status) == (rule.target, rule.status) else "conflicting-source"
            findings.append(Finding(code, f"source already appears in rule {old_i}", i))
        else:
            seen[rule.source] = (i, rule)
    mapping = {r.source: r.target for r in rules}
    cycles: set[frozenset[str]] = set()
    for start in mapping:
        order, positions, node = [], {}, start
        while node in mapping:
            if node in positions:
                cycle = order[positions[node]:] + [node]
                key = frozenset(cycle)
                if key not in cycles:
                    findings.append(Finding("redirect-cycle", "cycle: " + " -> ".join(cycle)))
                    cycles.add(key)
                break
            positions[node] = len(order); order.append(node); node = mapping[node]
    return ValidationReport(tuple(findings))

def resolve_chain(rules: list[RedirectRule], source: str, max_hops: int = 20) -> list[str]:
    if max_hops < 1: raise ValueError("max_hops must be at least 1")
    if not validate_rules(rules).ok: raise ValueError("cannot resolve an invalid rule set")
    mapping, chain, current = {r.source: r.target for r in rules}, [source], source
    for _ in range(max_hops):
        if current not in mapping: return chain
        current = mapping[current]; chain.append(current)
    if current in mapping: raise ValueError(f"redirect chain exceeds {max_hops} hops")
    return chain

def export_rules(rules: list[RedirectRule], fmt: str) -> str:
    if not validate_rules(rules).ok: raise ValueError("refusing to export an invalid rule set")
    lines = []
    for r in rules:
        if fmt == "netlify": lines.append(f"{r.source} {r.target} {r.status}")
        elif fmt == "apache": lines.append(f"Redirect {r.status} {r.source} {r.target}")
        elif fmt == "nginx": lines.append(f"location = {r.source} {{ return {r.status} {r.target}; }}")
        else: raise ValueError("format must be nginx, apache, or netlify")
    return "\n".join(lines) + ("\n" if lines else "")
