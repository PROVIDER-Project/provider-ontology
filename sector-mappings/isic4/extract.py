#!/usr/bin/env python3
"""Normalize official codes without numeric coercion; fail on duplicate/empty labels."""
import csv, json, re, sys
rows = []
section = ""
with open(sys.argv[1], encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f):
        code = row["Code"]
        if re.fullmatch(r"[A-U]", code):
            section = code
            parent = ""
        elif re.fullmatch(r"[0-9]{2,4}", code):
            parent = section if len(code) == 2 else code[:-1]
        else:
            raise ValueError("Unexpected ISIC code: " + code)
        rows.append((code, row["Description"], parent))
codes = {row[0] for row in rows}
if not rows or len(codes) != len(rows):
    raise ValueError("Empty or duplicate code list")
for code, label, parent in rows:
    if not label.strip() or (parent and parent not in codes):
        raise ValueError("Missing label or parent for " + code)
writer = csv.writer(sys.stdout, lineterminator="\n")
writer.writerow(("code", "label", "parent"))
writer.writerows(rows)
