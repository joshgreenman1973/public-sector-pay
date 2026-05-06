#!/usr/bin/env python3
"""Wave 2: code enforcement / accountant / IT analyst / recreation supervisor.

User chose strict CBA-only quality bar: skip Chicago accountant 'placeholder
approximation' the agent flagged; skip cells the agent labeled needs_research.
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data.json"

P = {
    # ---- code enforcement officer ----
    ("Chicago", "code_enforcement_officer"): {
        "entry_base": 78960, "top_base": 95100, "years_to_top": 5,
        "max_with_longevity": 139224, "max_years": 25,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.chicago.gov/content/dam/city/depts/dol/general/2025-Classification-and-Pay-Plan.pdf",
        "source_type": "city_pay_plan_schedule",
        "effective_date": "2025-01-01", "union": "AFSCME (Schedule B)",
        "notes": "Health Code Enforcement Inspection Analyst (2391, B13). Step 1 (post-6mo) $78,960; Step 5 (5yr top base) $95,100; longevity to Step 12 (25+yr) $139,224. Entrance rate (first 6 mo) $66,612."
    },
    ("Houston", "code_enforcement_officer"): {
        "entry_base": 45500, "top_base": 83434,
        "comparison_basis": "approximate", "employer_type": "city",
        "source_url": "https://www.houstontx.gov/hr/compensation/job-classifications.html",
        "source_type": "city_classification_page",
        "effective_date": "2024-2025", "union": "Non-represented (HOPE)",
        "notes": "Code Enforcement Officer I (795.2, grade 16). Open-range biweekly $1,750–$3,209 × 26."
    },
    ("Phoenix", "code_enforcement_officer"): {
        "entry_base": 42661, "top_base": 93122, "years_to_top": 16,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.phoenix.gov/content/dam/phoenix/hrsite/documents/class-and-comp-study/Salary-Range-Report.pdf",
        "source_type": "city_salary_range_report",
        "effective_date": "2026-04-27", "union": "AFSCME Local 2384 / ASPTEA",
        "notes": "Neighborhood Preservation Inspector (60670, grade 353). 17 steps $20.51-$44.77/hr."
    },
    ("San Antonio", "code_enforcement_officer"): {
        "entry_base": 46185, "top_base": 56791,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.sanantonio.gov/Portals/0/Files/EmployeeInformation/Compensation/PayPlan.pdf",
        "source_type": "city_pay_plan",
        "effective_date": "FY2025", "union": "Classified non-uniform",
        "notes": "Code Enforcement Officer (2116, grade 509). Open range."
    },
    ("San Diego", "code_enforcement_officer"): {
        "entry_base": 63684, "top_base": 76740, "years_to_top": 4,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.sandiego.gov/sites/default/files/saltable.pdf",
        "source_type": "city_salary_schedule",
        "effective_date": "2026-01-01", "union": "MEA / Local 127",
        "notes": "Code Compliance Officer (1356). 5 steps A-E hourly $30.51-$36.77; monthly $5,307-$6,395."
    },
    # ---- accountant / auditor ----
    ("Houston", "accountant_auditor"): {
        "entry_base": 48048, "top_base": 87984,
        "comparison_basis": "approximate", "employer_type": "city",
        "source_url": "https://www.houstontx.gov/hr/compensation/job-classifications.html",
        "source_type": "city_classification_page",
        "effective_date": "2024-2025", "union": "Non-represented",
        "notes": "Accountant (342.1, grade 17). Open-range biweekly $1,848-$3,385 × 26."
    },
    ("Phoenix", "accountant_auditor"): {
        "entry_base": 38688, "top_base": 84469, "years_to_top": 16,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.phoenix.gov/content/dam/phoenix/hrsite/documents/class-and-comp-study/Salary-Range-Report.pdf",
        "source_type": "city_salary_range_report",
        "effective_date": "2026-04-27", "union": "Phoenix Employees Association (Unit 7)",
        "notes": "Accountant I (03210). 17-step $18.60-$40.61/hr."
    },
    ("San Antonio", "accountant_auditor"): {
        "entry_base": 45553, "top_base": 68329,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.sanantonio.gov/Portals/0/Files/EmployeeInformation/Compensation/PayPlan.pdf",
        "source_type": "city_pay_plan",
        "effective_date": "FY2025", "union": "Non-represented",
        "notes": "Accountant (2220, grade 803)."
    },
    ("San Diego", "accountant_auditor"): {
        "entry_base": 79620, "top_base": 96804, "years_to_top": 4,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.sandiego.gov/sites/default/files/saltable.pdf",
        "source_type": "city_salary_schedule",
        "effective_date": "2026-01-01", "union": "MEA",
        "notes": "Accountant 1 (1102). Steps A-E $38.15-$46.38/hr; monthly $6,635-$8,067."
    },
    # ---- IT analyst / systems administrator ----
    ("Chicago", "it_analyst"): {
        "entry_base": 66612, "top_base": 95100, "years_to_top": 5,
        "max_with_longevity": 139224, "max_years": 25,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.chicago.gov/content/dam/city/depts/dol/general/2025-Classification-and-Pay-Plan.pdf",
        "source_type": "city_pay_plan_schedule",
        "effective_date": "2025-01-01", "union": "AFSCME (Schedule B)",
        "notes": "Application/Systems Analyst (06D8, B13). Schedule B Step 1 (post-6mo) $78,960; Step 5 (5yr) top base $95,100; entrance $66,612 first 6 months. Longevity Step 12 (25+yr) $139,224."
    },
    ("Houston", "it_analyst"): {
        "entry_base": 45500, "top_base": 83434,
        "comparison_basis": "approximate", "employer_type": "city",
        "source_url": "https://www.houstontx.gov/hr/compensation/job-classifications.html",
        "source_type": "city_classification_page",
        "effective_date": "2024-2025", "union": "Non-represented",
        "notes": "Programmer Analyst I (452.1, grade 16). Open-range biweekly $1,750-$3,209 × 26."
    },
    ("Phoenix", "it_analyst"): {
        "entry_base": 44803, "top_base": 97781, "years_to_top": 16,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.phoenix.gov/content/dam/phoenix/hrsite/documents/class-and-comp-study/Salary-Range-Report.pdf",
        "source_type": "city_salary_range_report",
        "effective_date": "2026-04-27", "union": "Phoenix Employees Association",
        "notes": "Business Systems Analyst (09810). 17 steps $21.54-$47.01/hr."
    },
    ("San Antonio", "it_analyst"): {
        "entry_base": 47830, "top_base": 71746,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.sanantonio.gov/Portals/0/Files/EmployeeInformation/Compensation/PayPlan.pdf",
        "source_type": "city_pay_plan",
        "effective_date": "FY2025", "union": "Non-represented",
        "notes": "Technical System Specialist (2560, grade 804)."
    },
    ("San Diego", "it_analyst"): {
        "entry_base": 55620, "top_base": 67158, "years_to_top": 4,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.sandiego.gov/sites/default/files/saltable.pdf",
        "source_type": "city_salary_schedule",
        "effective_date": "2026-01-01", "union": "MEA",
        "notes": "Programmer Analyst 1 (1747). Steps A-E $26.64-$32.17/hr; monthly $4,633-$5,595."
    },
    # ---- recreation supervisor ----
    ("Houston", "recreation_supervisor"): {
        "entry_base": 45500, "top_base": 83434,
        "comparison_basis": "approximate", "employer_type": "city",
        "source_url": "https://www.houstontx.gov/hr/compensation/job-classifications.html",
        "source_type": "city_classification_page",
        "effective_date": "2024-2025", "union": "Non-represented",
        "notes": "Recreation Supervisor (976.7, grade 16). Open range."
    },
    ("Phoenix", "recreation_supervisor"): {
        "entry_base": 50627, "top_base": 110510, "years_to_top": 16,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.phoenix.gov/content/dam/phoenix/hrsite/documents/class-and-comp-study/Salary-Range-Report.pdf",
        "source_type": "city_salary_range_report",
        "effective_date": "2026-04-27", "union": "Middle Mgmt Unit 7",
        "notes": "Recreation Supervisor (41170, grade 060). 17 steps $24.34-$53.13/hr."
    },
    ("San Antonio", "recreation_supervisor"): {
        "entry_base": 46185, "top_base": 56791,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.sanantonio.gov/Portals/0/Files/EmployeeInformation/Compensation/PayPlan.pdf",
        "source_type": "city_pay_plan",
        "effective_date": "FY2025", "union": "Classified non-uniform",
        "notes": "Recreation Supervisor (2174, grade 509)."
    },
    ("San Diego", "recreation_supervisor"): {
        "entry_base": 75828, "top_base": 91956, "years_to_top": 4,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.sandiego.gov/sites/default/files/saltable.pdf",
        "source_type": "city_salary_schedule",
        "effective_date": "2026-01-01", "union": "MEA",
        "notes": "Supv Aging Recreation Specialist (1059) — proxy for Rec Supervisor; San Diego doesn't have a class titled simply 'Recreation Supervisor'. Hourly A $36.33 → E $44.06; monthly $6,319-$7,663."
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
    print(f"Ingested {n} Wave 2 cells")


if __name__ == "__main__":
    main()
