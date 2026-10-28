#!/usr/bin/env python3
"""Deterministic dry-run role router. Never executes an external agent."""
import argparse
import json
from pathlib import Path

COST_RANK = {"low": 0, "medium": 1, "high": 2, "unknown": 3}
SCOPE_RANK = {"public": 0, "internal": 1, "restricted": 2}

def choose(registry, task):
    eligible = []
    rejections = {}
    for a in registry.get("agents", []):
        reasons = []
        if not a.get("enabled") or a.get("verification") != "verified":
            reasons.append("not enabled and verified")
        if a.get("assurance_tier", 0) < task.get("minimum_assurance_tier", 1):
            reasons.append("insufficient assurance tier")
        if task.get("role") not in a.get("roles", []):
            reasons.append("role not permitted")
        if not set(task.get("required_capabilities", [])).issubset(set(a.get("capabilities", []))):
            reasons.append("missing capabilities")
        if task.get("role") == "reviewer" and not a.get("read_only_enforced", False):
            reasons.append("read-only enforcement missing")
        if task.get("data_scope", "internal") not in a.get("data_scopes", []):
            reasons.append("data scope not permitted")
        if reasons:
            rejections[a.get("id", "<missing>")] = reasons
        else:
            eligible.append(a)
    eligible.sort(key=lambda a: (COST_RANK.get(a.get("cost_class", "unknown"), 3), -a.get("assurance_tier", 0), a.get("id", "")))
    return {"selected_agent": eligible[0]["id"] if eligible else None, "eligible_agents": [a["id"] for a in eligible], "rejections": rejections, "dry_run": True, "executed": False}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--registry", required=True)
    p.add_argument("--task", required=True)
    a = p.parse_args()
    reg = json.loads(Path(a.registry).read_text(encoding="utf-8"))
    task = json.loads(Path(a.task).read_text(encoding="utf-8"))
    print(json.dumps(choose(reg, task), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
