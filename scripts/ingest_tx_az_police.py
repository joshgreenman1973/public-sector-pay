#!/usr/bin/env python3
"""Ingest Texas + Phoenix police rank ladder from Stage 2 agent."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data.json"

PAYLOADS = {
    ("Houston", "police_detective"): {
        "entry_base": 103323, "top_base": 139946, "years_to_top": 12,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.hpdcareer.com/benefits.html",
        "cba_url": "https://hpou.org/wp-content/uploads/2025/07/2025-Meet-Confer-Executed.pdf",
        "source_type": "department_careers_page",
        "effective_date": "2025-07-01", "union": "HPOU",
        "notes": "Senior Police Officer (12+ Years) base range $103,323–$139,946 from HPD official recruiting microsite hpdcareer.com under 2025 'Generational Contract' (10% raise effective 7/1/2025). HPD Investigator is an assignment within Officer/Sr Officer ranks, not a separate civil-service class."
    },
    ("Houston", "police_sergeant"): {
        "entry_base": 114645, "top_base": 159928, "years_to_top": 5,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.hpdcareer.com/benefits.html",
        "cba_url": "https://hpou.org/wp-content/uploads/2025/07/2025-Meet-Confer-Executed.pdf",
        "source_type": "department_careers_page",
        "effective_date": "2025-07-01", "union": "HPOU",
        "notes": "Sergeant (5+ Years) $114,645–$159,928."
    },
    ("Houston", "police_lieutenant"): {
        "entry_base": 129298, "top_base": 177874, "years_to_top": 7,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.hpdcareer.com/benefits.html",
        "source_type": "department_careers_page",
        "effective_date": "2025-07-01", "union": "HPOU",
        "notes": "Lieutenant (7+ Years) $129,298–$177,874."
    },
    ("Houston", "police_captain"): {
        "entry_base": 148100, "top_base": 208363, "years_to_top": 9,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.hpdcareer.com/benefits.html",
        "source_type": "department_careers_page",
        "effective_date": "2025-07-01", "union": "HPOU",
        "notes": "Captain (9+ Years) $148,100–$208,363."
    },
    # Dallas
    ("Dallas", "police_detective"): {
        "entry_base": None, "top_base": 100243, "years_to_top": 4,
        "comparison_basis": "post_progression_base",
        "source_url": "https://dallascityhall.com/departments/humanresources/PublishingImages/Pages/classification_compensation/Attachment%20B-3.pdf",
        "source_type": "city_salary_schedule",
        "effective_date": "2024-10-01", "union": "DPA (no CBA; Ch. 143 civil service)",
        "notes": "Police Senior Corporal (class 46016, Year 4* P-4) $100,243 = Dallas detective/investigator analog. Police Officer top (Year 9* P-9) is $91,734."
    },
    ("Dallas", "police_sergeant"): {
        "entry_base": None, "top_base": 110649, "years_to_top": 3,
        "comparison_basis": "post_progression_base",
        "source_url": "https://dallascityhall.com/departments/humanresources/PublishingImages/Pages/classification_compensation/Attachment%20B-3.pdf",
        "source_type": "city_salary_schedule",
        "effective_date": "2024-10-01", "union": "DPA",
        "notes": "Class 46011, Year 3* P-3 = $110,649."
    },
    ("Dallas", "police_lieutenant"): {
        "entry_base": None, "top_base": 122136, "years_to_top": 3,
        "comparison_basis": "post_progression_base",
        "source_url": "https://dallascityhall.com/departments/humanresources/PublishingImages/Pages/classification_compensation/Attachment%20B-3.pdf",
        "source_type": "city_salary_schedule",
        "effective_date": "2024-10-01", "union": "DPA",
        "notes": "Class 46013, Year 3* P-3 = $122,136."
    },
    ("Dallas", "police_captain"): {
        "entry_base": None, "top_base": 134815, "years_to_top": 3,
        "comparison_basis": "post_progression_base",
        "source_url": "https://dallascityhall.com/departments/humanresources/PublishingImages/Pages/classification_compensation/Attachment%20B-3.pdf",
        "source_type": "city_salary_schedule",
        "effective_date": "2024-10-01", "union": "DPA",
        "notes": "Class 46014, Year 3* S P-3 = $134,815. Schedule states 'Police Captain is an Obsolete Rank' — being phased out; only top-step row shown because all current Captains are at top step."
    },
    # San Antonio
    ("San Antonio", "police_detective"): {
        "entry_base": None, "top_base": 95268, "years_to_top": None,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.sanantonio.gov/Portals/0/Files/Atty/CollectiveBargaining/Police/COSA%20SAPOA%20CBA%20Tentative%20Agreement.pdf",
        "cba_url": "https://www.sanantonio.gov/Portals/0/Files/Atty/CollectiveBargaining/Police/COSA%20SAPOA%20CBA%20Tentative%20Agreement.pdf",
        "source_type": "cba",
        "effective_date": "2025-04-01", "union": "SAPOA",
        "notes": "SAPOA CBA Attachment 2 (4/1/2025): Detective Investigator step D top = $7,939/mo × 12 = $95,268."
    },
    ("San Antonio", "police_sergeant"): {
        "entry_base": None, "top_base": 104088, "years_to_top": None,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.sanantonio.gov/Portals/0/Files/Atty/CollectiveBargaining/Police/COSA%20SAPOA%20CBA%20Tentative%20Agreement.pdf",
        "source_type": "cba",
        "effective_date": "2025-04-01", "union": "SAPOA",
        "notes": "Sergeant top step C $8,674/mo × 12 = $104,088. New scale 4/1/2026 raises to $108,252."
    },
    ("San Antonio", "police_lieutenant"): {
        "entry_base": None, "top_base": 116604, "years_to_top": None,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.sanantonio.gov/Portals/0/Files/Atty/CollectiveBargaining/Police/COSA%20SAPOA%20CBA%20Tentative%20Agreement.pdf",
        "source_type": "cba",
        "effective_date": "2025-04-01", "union": "SAPOA",
        "notes": "Lieutenant top step C $9,717/mo × 12 = $116,604."
    },
    ("San Antonio", "police_captain"): {
        "entry_base": None, "top_base": 133788, "years_to_top": None,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.sanantonio.gov/Portals/0/Files/Atty/CollectiveBargaining/Police/COSA%20SAPOA%20CBA%20Tentative%20Agreement.pdf",
        "source_type": "cba",
        "effective_date": "2025-04-01", "union": "SAPOA",
        "notes": "Captain top step C $11,149/mo × 12 = $133,788."
    },
    # Phoenix
    ("Phoenix", "police_detective"): {
        "entry_base": 74360, "top_base": 107827, "years_to_top": 8,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.phoenix.gov/content/dam/phoenix/hrsite/documents/class-and-comp-study/Salary-Range-Report.pdf",
        "source_type": "city_salary_range_report",
        "effective_date": "2026-04-27", "union": "PLEA",
        "notes": "Phoenix has NO separate Detective civil-service class; detective is an assignment within Officer rank. Same as patrol top-step ($107,827, Class 62210 step 9)."
    },
    ("Phoenix", "police_sergeant"): {
        "entry_base": None, "top_base": 141918, "years_to_top": 6,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.phoenix.gov/content/dam/phoenix/hrsite/documents/class-and-comp-study/Salary-Range-Report.pdf",
        "source_type": "city_salary_range_report",
        "effective_date": "2026-04-27", "union": "PPSLA",
        "notes": "Class 62220 Police Sergeant, 7 steps, top = $68.23/hr × 2080 = $141,918."
    },
    ("Phoenix", "police_lieutenant"): {
        "entry_base": None, "top_base": 171371, "years_to_top": 5,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.phoenix.gov/content/dam/phoenix/hrsite/documents/class-and-comp-study/Salary-Range-Report.pdf",
        "source_type": "city_salary_range_report",
        "effective_date": "2026-04-27", "union": "PPSLA",
        "notes": "Class 62230 Police Lieutenant, 5 steps, top = $82.39/hr × 2080 = $171,371."
    },
    ("Phoenix", "police_captain"): {
        "entry_base": None, "top_base": 219211, "years_to_top": None,
        "comparison_basis": "approximate",
        "source_url": "https://www.phoenix.gov/content/dam/phoenix/hrsite/documents/class-and-comp-study/Salary-Range-Report.pdf",
        "source_type": "city_salary_range_report",
        "effective_date": "2026-04-27", "union": "Unrepresented (executive/management)",
        "notes": "Phoenix has NO Captain rank — Commander (Class 62240) is the next rank above Lieutenant. Range $84.30–$105.39/hr; top of range = $219,211. Range-based not stepped (exempt management)."
    },
}


def main():
    data = json.loads(DATA.read_text())
    cities_by_name = {c["city"]: c for c in data["cities"]}
    n = 0
    for (city, role), payload in PAYLOADS.items():
        cities_by_name[city]["roles"][role] = payload
        n += 1
    DATA.write_text(json.dumps(data, indent=2))
    print(f"Ingested {n} TX/AZ police-rank cells")


if __name__ == "__main__":
    main()
