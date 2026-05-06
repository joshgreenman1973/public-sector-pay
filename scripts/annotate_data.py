#!/usr/bin/env python3
"""Annotate existing cells with comparison_basis and max_with_longevity flags.

Run idempotently — only adds fields that aren't already present, and only for the
police/fire/sanitation/transit cells listed below. Hand-curated based on what each
contract actually represents.
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data.json"

# {city: {role: {comparison_basis, max_with_longevity?, max_years?, pre_raise?, notes?}}}
PATCHES = {
    "New York": {
        "police_officer": {
            "comparison_basis": "post_progression_base",
            "pre_raise": True,  # PBA expired 7/2025; renegotiation pending
            "extra_notes": "Top base step is $85,292 at 5.5 years. NYC keeps longevity OUTSIDE base — paid as separate adders ($350 at 5yr, $1,400 at 10yr, $2,500 at 15yr, $3,600 at 20yr; reflects 2017-25 PBA contract). Plus holiday pay, uniform allowance, night differential. PBA contract EXPIRED 7/31/2025 — successor under negotiation, expected 8-15% retroactive raise.",
        },
        "firefighter": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "$105,146 base reached at 5.5 yrs. FDNY longevity adders paid separately. With holiday pay (5%), night differential (15% of nights), uniform allowance, top firefighter total comp commonly exceeds $130k.",
        },
        "sanitation_worker": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "$92,093 base at 5.5 yrs. DSNY longevity adders separate.",
        },
    },
    "Los Angeles": {
        "police_officer": {
            "comparison_basis": "approximate",
            "extra_notes": "$109k figure is approximate from joinlapd.com (which bundles bonuses). MOU 24 Appendix A has the authoritative step values; not directly extracted here. Top step PO II reached at ~5 yrs of step ladder.",
        },
        "firefighter": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "Top step Firefighter II reached at ~3 yrs of step ladder. UFLAC MOU 23.",
        },
        "sanitation_worker": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "Class 3580 Refuse Collection Truck Operator. Top of 5-step range.",
        },
    },
    "Houston": {
        "police_officer": {
            "comparison_basis": "partial",
            "extra_notes": "Only the first-year base ($81,600) is captured. HPD base scale tops at year 3; longevity continues to 25+ yrs. 5-yr top base + 25-yr longevity not extracted from HPOU base-pay calculator.",
        },
        "firefighter": {
            "comparison_basis": "approximate",
            "pre_raise": True,
            "extra_notes": "FY25 CBA (signed 6/3/2024) included 10% first-year raise; HFD compensation page may not yet reflect post-CBA figures. Likely $59-79k post-raise.",
        },
    },
    "Phoenix": {
        "police_officer": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "Class 62210 Police Officer, Step 9 of 9 = $107,827 at end of step ladder. Phoenix doesn't have a separate longevity step structure for police; specialty pay (FTO, K9, Pilot, etc.) is in separate classifications.",
        },
        "firefighter": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "Class 61010 Firefighter, basic 56-hour schedule, end of step ladder $76,626. With Hazmat/Paramedic certifications, top reaches $93,123 (Class 6101E).",
        },
        "sanitation_worker": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "Solid Waste Equipment Operator Class 72080.",
        },
    },
    "Philadelphia": {
        "police_officer": {
            "comparison_basis": "approximate",
            "pre_raise": True,
            "extra_notes": "Figures from joinphillypd.com may pre-date the 7/1/2024 5% raise; current numbers ~5-8% higher. Aug 2025 Act 111 award added 3% raises FY26 and FY27.",
        },
        "transit_bus_operator": {
            "comparison_basis": "post_progression_base",
        },
    },
    "San Antonio": {
        "police_officer": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "Patrol Officer base range $58,452–$79,620 (post-step). Sergeant ($92,964–$96,708), Lieutenant ($104,112–$108,324), Captain (higher) are separate ranks.",
        },
        "firefighter": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "Monthly base × 12 from SAFD careers page. Plus 3% per 5 yrs longevity to max 18%.",
        },
        "sanitation_worker": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "Solid Waste Collection Truck Driver (Rear Loader). Curbside collection worker is lower; Sr. Equipment Operator higher.",
        },
    },
    "San Diego": {
        "police_officer": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "Police Officer II top step. PO III, Detective, Sergeant, Lieutenant are separate.",
        },
    },
    "Dallas": {
        "police_officer": {
            "comparison_basis": "post_progression_base",
            "pre_raise": True,
            "extra_notes": "Step 9 (year 9+) base $91,734. FY25-26 budget proposes raising start to $81,232. Senior Corporal (Grade 2 P) is a separate rank.",
        },
        "firefighter": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "Fire-Rescue Officer Pay Grade 1 FF, Step 9.",
        },
        "sanitation_worker": {
            "comparison_basis": "partial",
            "extra_notes": "Sanitation Truck Driver entry $20.50/hr × 2,080. Top of grade not extracted from civilian pay schedule.",
        },
        "transit_bus_operator": {
            "comparison_basis": "approximate",
            "extra_notes": "DART/ATU 1338 contract not posted on agency site; figures from public salary aggregators.",
        },
    },
    "San Francisco": {
        "police_officer": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "Q002 Police Officer, Step 7 of 7 = end of step ladder. With POST/longevity bonuses total comp at top step ~$178,394.",
        },
        "firefighter": {
            "comparison_basis": "approximate",
            "extra_notes": "H2 Firefighter Step 1 $93,846 confirmed. Top of 5 H2 steps approx $135,000 — exact appendix figure needs verification.",
        },
        "transit_bus_operator": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "Class 9163 Transit Operator, Step 5 of 5.",
        },
    },
    "Boston": {
        "firefighter": {
            "comparison_basis": "needs_research",
            "extra_notes": "New 4-year CBA 2024-2028 ratified Dec 22, 2025 (8.5% compounded). Salary appendix not yet posted on boston.gov.",
        },
        "transit_bus_operator": {
            "comparison_basis": "approximate",
            "extra_notes": "Entry $30/hr from MBTA announcement; top hourly not in announcement; estimated ~$35-36/hr after 18% cumulative 4-yr increase.",
        },
    },
    "Seattle": {
        "police_officer": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "Step 1 entry $118k under 2025 contract amendment, top step $136,104 at 4.5 yrs. SPOG longevity bonuses paid as separate adders.",
        },
        "firefighter": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "Recruit $102,048 → Step 5 $121,488 at 42 months. CBA Dec 2021 – Dec 2026.",
        },
        "transit_bus_operator": {
            "comparison_basis": "partial",
            "extra_notes": "Entry $27.59/hr; top step not extracted from ATU 587 CBA appendix. ~17% cumulative increase suggests top hourly ~$42-45.",
        },
    },
    "Washington, D.C.": {
        "police_officer": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "FY26 schedule, 4.25% increase Oct 5, 2025. Step 9 of 9 = end of ladder. Post-probation Step 1 $78,601; post-5yr retention Step 1 $82,531 are interim retention bumps.",
        },
        "firefighter": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "Class 01 Private Step 9 = end of ladder $92,113. Through 30-yr longevity Step 9 reaches $110,536.",
            "max_with_longevity": 110536,
            "max_years": 30,
        },
        "transit_bus_operator": {
            "comparison_basis": "post_progression_base",
            "extra_notes": "Entry $29.49/hr. New CBA Jul 2024–Jun 2028: 0%/3%/3%/3.5%.",
        },
    },
}


def main():
    data = json.loads(DATA.read_text())
    for city in data["cities"]:
        patch = PATCHES.get(city["city"], {})
        for role_key, role_patch in patch.items():
            r = city["roles"].get(role_key)
            if not r:
                continue
            for k, v in role_patch.items():
                if k == "extra_notes":
                    # Append to existing notes if not already there
                    if v and v not in (r.get("notes") or ""):
                        r["notes"] = (r.get("notes") or "")
                        r["notes"] = (r["notes"] + " " + v).strip()
                else:
                    r[k] = v
    DATA.write_text(json.dumps(data, indent=2))
    print(f"Patched {DATA}")


if __name__ == "__main__":
    main()
