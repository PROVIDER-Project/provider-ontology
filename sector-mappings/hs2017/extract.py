#!/usr/bin/env python3
"""Normalize official codes without numeric coercion; fail on duplicate/empty labels."""
import csv, json, re, sys
rows = []
with open(sys.argv[1], encoding="utf-8-sig") as f:
    data = json.load(f)
for item in data["results"]:
    code = item["id"]
    label = item["text"]
    if label.startswith(code + " - "):
        label = label[len(code) + 3:]
    parent = item.get("parent", "")
    rows.append((code, label, "" if parent == "#" else parent))
codes = {row[0] for row in rows}
if not rows or len(codes) != len(rows):
    raise ValueError("Empty or duplicate code list")
for code, label, parent in rows:
    if not label.strip() or (parent and parent not in codes):
        raise ValueError("Missing label or parent for " + code)
writer = csv.writer(sys.stdout, lineterminator="\n")
writer.writerow(("code", "label", "parent"))
writer.writerows(rows)
