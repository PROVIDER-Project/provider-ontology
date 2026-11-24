#!/usr/bin/env python3
"""Normalize official codes without numeric coercion; fail on duplicate/empty labels."""
import csv, json, re, sys
rows = []
with open(sys.argv[1], encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f):
        code = row["Field1"]
        if code == "CPC Ver. 2.1 Code":
            continue
        if not re.fullmatch(r"[0-9]{1,5}", code):
            raise ValueError("Unexpected CPC code: " + code)
        rows.append((code, row["Field2"], code[:-1]))
codes = {row[0] for row in rows}
if not rows or len(codes) != len(rows):
    raise ValueError("Empty or duplicate code list")
for code, label, parent in rows:
    if not label.strip() or (parent and parent not in codes):
        raise ValueError("Missing label or parent for " + code)
writer = csv.writer(sys.stdout, lineterminator="\n")
writer.writerow(("code", "label", "parent"))
writer.writerows(rows)
