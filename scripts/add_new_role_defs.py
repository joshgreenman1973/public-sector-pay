#!/usr/bin/env python3
"""Add 4 new role definitions and reorder rank_order in 'Other public sector'."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data.json"

NEW_OTHER_ORDER = [
    ("dispatcher_911",          "911 dispatcher / public safety telecommunicator"),
    ("librarian",               "Public librarian"),
    ("building_inspector",      "Building inspector"),
    ("code_enforcement_officer","Code enforcement officer"),
    ("civil_engineer",          "Civil engineer (city)"),
    ("court_clerk",             "Court / municipal clerk"),
    ("public_health_nurse",     "Public health nurse"),
    ("accountant_auditor",      "Accountant / auditor (city)"),
    ("it_analyst",              "IT analyst / systems administrator"),
    ("recreation_supervisor",   "Parks & Recreation supervisor"),
    ("city_plumber",            "City plumber (journey-level)"),
    ("parks_worker",            "Parks maintenance worker"),
]


def main():
    data = json.loads(DATA.read_text())
    for i, (key, label) in enumerate(NEW_OTHER_ORDER, start=1):
        data["role_definitions"][key] = {
            "label": label, "category": "Other public sector", "rank_order": i,
        }
    DATA.write_text(json.dumps(data, indent=2))
    print(f"Wrote {len(NEW_OTHER_ORDER)} 'Other' role definitions in canonical order")


if __name__ == "__main__":
    main()
