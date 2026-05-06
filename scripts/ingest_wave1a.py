#!/usr/bin/env python3
"""Wave 1A: 911 dispatcher / civil engineer / city plumber."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data.json"

P = {
    # 911 dispatcher
    ("Los Angeles", "dispatcher_911"): {
        "entry_base": 58484, "top_base": 103272,
        "comparison_basis": "approximate", "employer_type": "city",
        "source_url": "https://personnel.lacity.gov/jobs/position-information/index.cfm?job_id=2207",
        "cba_url": "https://cao.lacity.gov/mous/",
        "source_type": "city_classification_page",
        "effective_date": "2024-07-01", "union": "Coalition of LA City Unions / EAA",
        "notes": "Police Service Representative (Class 2207). Range from official LA Personnel job spec; exact MOU step schedule not yet pulled from CAO MOU PDF."
    },
    ("Chicago", "dispatcher_911"): {
        "entry_base": 53340, "top_base": 94368, "years_to_top": 25,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.chicago.gov/content/dam/city/depts/dol/general/2025-Classification-and-Pay-Plan.pdf",
        "source_type": "city_pay_plan_schedule",
        "effective_date": "2022-01-01", "union": "Public Safety Employees Union - Unit II (Schedule I)",
        "notes": "Police Communications Operator I (title 8601, grade I13). Step 1 $53,340 → Step 12 (25 yrs) $94,368. Schedule I dated 1/1/2022 in current pay plan; may be retro-adjusted by current CBA."
    },
    ("Houston", "dispatcher_911"): {
        "entry_base": 41106, "top_base": 76310,
        "comparison_basis": "approximate", "employer_type": "city",
        "source_url": "https://www.houstontx.gov/hr/hrfiles/compensation/list_job_classifications_abc.pdf",
        "source_type": "city_classification_page",
        "effective_date": "2025-07-01", "union": "non-union (Texas)",
        "notes": "Job code 644.2 9-1-1 Telecommunicator, Grade 14. Houston pay grade is open range (no step schedule)."
    },
    ("Phoenix", "dispatcher_911"): {
        "entry_base": 36858, "top_base": 80454,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.phoenix.gov/content/dam/phoenix/hrsite/documents/class-and-comp-study/Salary-Range-Report.pdf",
        "source_type": "city_salary_range_report",
        "effective_date": "2026-04-27", "union": "AFSCME Local 2384 (Unit 003)",
        "notes": "Job code 01830 Police Comm Operator. 17-step grid, $17.72-$38.68/hr × 2080. Trainee class 01740 starts at $35,110."
    },
    ("San Diego", "dispatcher_911"): {
        "entry_base": 82896, "top_base": 99948, "years_to_top": 4,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.sandiego.gov/sites/default/files/saltable.pdf",
        "source_type": "city_salary_schedule",
        "effective_date": "2026-01-01", "union": "Municipal Employees Association (MEA)",
        "notes": "Class 1714 Police Dispatcher. 5 steps A-E, monthly $6,908-$8,329 × 12."
    },
    # civil engineer
    ("Houston", "civil_engineer"): {
        "entry_base": 61568, "top_base": 117390,
        "comparison_basis": "approximate", "employer_type": "city",
        "source_url": "https://www.houstontx.gov/hr/hrfiles/compensation/list_job_classifications_abc.pdf",
        "source_type": "city_classification_page",
        "effective_date": "2025-07-01", "union": "non-union",
        "notes": "Job code 778.2 Engineer-in-Training, Grade 22 ($61,568-$117,390). Houston has no city-titled 'Civil Engineer I' — graduate engineers enter as EIT."
    },
    ("Phoenix", "civil_engineer"): {
        "entry_base": 47029, "top_base": 102669,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.phoenix.gov/content/dam/phoenix/hrsite/documents/class-and-comp-study/Salary-Range-Report.pdf",
        "source_type": "city_salary_range_report",
        "effective_date": "2026-04-27", "union": "Unit 007 (Supervisors/Professionals)",
        "notes": "Job code 20210 Civil Engineer I, 17-step grid $22.61-$49.36/hr."
    },
    ("San Diego", "civil_engineer"): {
        "entry_base": 100560, "top_base": 121116, "years_to_top": 4,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.sandiego.gov/sites/default/files/saltable.pdf",
        "source_type": "city_salary_schedule",
        "effective_date": "2026-01-01", "union": "Municipal Employees Association (MEA)",
        "notes": "Class 1153 Asst Engineer-Civil (entry licensed civil engineer). Steps A-E monthly $8,380-$10,093. Jr Engineer-Civil (1546) is sub-licensed: $86,904-$105,168."
    },
    # city plumber
    ("Houston", "city_plumber"): {
        "entry_base": 45500, "top_base": 83434,
        "comparison_basis": "approximate", "employer_type": "city",
        "source_url": "https://www.houstontx.gov/hr/hrfiles/compensation/list_job_classifications_abc.pdf",
        "source_type": "city_classification_page",
        "effective_date": "2025-07-01", "union": "non-union",
        "notes": "Job code 524.2 Plumber, Grade 16 ($45,500-$83,434). Open-range, no step."
    },
    ("Phoenix", "city_plumber"): {
        "entry_base": 38688, "top_base": 84469,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.phoenix.gov/content/dam/phoenix/hrsite/documents/class-and-comp-study/Salary-Range-Report.pdf",
        "source_type": "city_salary_range_report",
        "effective_date": "2026-04-27", "union": "AFSCME Local 2960 / Laborers",
        "notes": "Job codes 74833/74834 Building Maint Wrkr*Plumber, 17-step grid $18.60-$40.61/hr. Phoenix has no standalone 'Plumber' class — role is Building Maint Worker w/ Plumber endorsement."
    },
    ("San Diego", "city_plumber"): {
        "entry_base": 77412, "top_base": 92916, "years_to_top": 4,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.sandiego.gov/sites/default/files/saltable.pdf",
        "source_type": "city_salary_schedule",
        "effective_date": "2026-01-01", "union": "MEA",
        "notes": "Class 1675 Plumber, steps A-E monthly $6,451-$7,743 × 12."
    },
}


def main():
    data = json.loads(DATA.read_text())
    cities_by_name = {c["city"]: c for c in data["cities"]}
    n = 0
    for (city, role), payload in P.items():
        cities_by_name[city]["roles"][role] = payload
        n += 1
    DATA.write_text(json.dumps(data, indent=2))
    print(f"Ingested {n} Wave 1A cells")


if __name__ == "__main__":
    main()
