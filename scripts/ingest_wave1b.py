#!/usr/bin/env python3
"""Wave 1B: librarian / court clerk / parks maintenance worker.

Note many court clerks are state-employed not city; mark those as out of scope
rather than filling with bad data.
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data.json"

P = {
    # ---- librarian ----
    ("New York", "librarian"): {
        "entry_base": 47135, "top_base": 58906, "years_to_top": 7,
        "max_with_longevity": 67934,
        "comparison_basis": "post_progression_base", "employer_type": "library_system",
        "source_url": "https://local1321.org/system/files/2025-09/2025_07_01_local_1321_members_salaries.pdf",
        "cba_url": "https://local1321.org/salaries",
        "source_type": "union_wage_chart",
        "effective_date": "2025-07-01", "union": "Queens Library Guild Local 1321 (DC 37)",
        "notes": "Queens Public Library Librarian (MLS-required). NYPL/BPL use DC 37 Local 1930 (separate scale, not pulled here). Max-with-longevity ~$67,934 after 20yrs incl. increment payments."
    },
    ("Chicago", "librarian"): {
        "entry_base": 65328, "top_base": 95592, "years_to_top": 8,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.chicago.gov/content/dam/city/depts/dol/general/2025-Classification-and-Pay-Plan.pdf",
        "source_type": "city_pay_plan_schedule",
        "effective_date": "2025-01-01", "union": "AFSCME Council 31",
        "notes": "Class 0501 Librarian I, Schedule G Grade 4. Chicago Public Library is a city department."
    },
    ("Houston", "librarian"): {
        "entry_base": 45500, "top_base": 83434,
        "comparison_basis": "approximate", "employer_type": "city",
        "source_url": "https://www.houstontx.gov/hr/hrfiles/compensation/list_job_classifications_abc.pdf",
        "source_type": "city_classification_page",
        "effective_date": "2025", "union": None,
        "notes": "Class 902.2 Librarian I, Grade 16. Open-range biweekly $1,750-$3,209 × 26."
    },
    ("Phoenix", "librarian"): {
        "entry_base": 42661, "top_base": 93122, "years_to_top": 16,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.phoenix.gov/content/dam/phoenix/hrsite/documents/class-and-comp-study/Salary-Range-Report.pdf",
        "source_type": "city_salary_range_report",
        "effective_date": "2025", "union": None,
        "notes": "Class 30210 Librarian I, Range 053. 17 steps $20.51-$44.77/hr."
    },
    ("San Antonio", "librarian"): {
        "entry_base": 45553, "top_base": 68329,
        "comparison_basis": "approximate", "employer_type": "city",
        "source_url": "https://www.sanantonio.gov/Portals/0/Files/EmployeeInformation/Compensation/PayPlan.pdf",
        "source_type": "city_pay_plan",
        "effective_date": "2025-10-01", "union": None,
        "notes": "Class 954 Librarian I, Pay Plan B Range 803."
    },
    ("San Diego", "librarian"): {
        "entry_base": 68266, "top_base": 82243, "years_to_top": 4,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.sandiego.gov/sites/default/files/saltable.pdf",
        "source_type": "city_salary_schedule",
        "effective_date": "2026-01-01", "union": None,
        "notes": "Class 1571 Librarian 1. 5 steps A-E hourly $32.82-$39.54 × 2080."
    },
    ("San Francisco", "librarian"): {
        "entry_base": 103558, "top_base": 125892, "years_to_top": 4,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://careers.sf.gov/classifications/?classCode=3630",
        "cba_url": "https://sfdhr.org/mous",
        "source_type": "city_classification_page",
        "effective_date": "2026-01-03", "union": "SEIU Local 1021",
        "notes": "Class 3630 Librarian I. SF combined library system is city-county dept."
    },
    # ---- court clerk ----
    ("Houston", "court_clerk"): {
        "entry_base": 37856, "top_base": 65494,
        "comparison_basis": "approximate", "employer_type": "city",
        "source_url": "https://www.houstontx.gov/hr/hrfiles/compensation/list_job_classifications_abc.pdf",
        "source_type": "city_classification_page",
        "effective_date": "2025", "union": None,
        "notes": "Class 591.2 Deputy Courts Clerk Grade 11. Houston Municipal Court is a city dept."
    },
    ("Phoenix", "court_clerk"): {
        "entry_base": 31845, "top_base": 60029, "years_to_top": 13,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.phoenix.gov/content/dam/phoenix/hrsite/documents/class-and-comp-study/Salary-Range-Report.pdf",
        "source_type": "city_salary_range_report",
        "effective_date": "2025", "union": None,
        "notes": "Class 00510 Court/Legal Clerk I. Phoenix Municipal Court is a city dept."
    },
    ("San Antonio", "court_clerk"): {
        "entry_base": 43986, "top_base": 54087,
        "comparison_basis": "approximate", "employer_type": "city",
        "source_url": "https://www.sanantonio.gov/Portals/0/Files/EmployeeInformation/Compensation/PayPlan.pdf",
        "source_type": "city_pay_plan",
        "effective_date": "2025-10-01", "union": None,
        "notes": "Class 2292 Municipal Court of Record Clerk, Range 508."
    },
    ("San Diego", "court_clerk"): {
        "entry_base": 49692, "top_base": 59782, "years_to_top": 4,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.sandiego.gov/sites/default/files/saltable.pdf",
        "source_type": "city_salary_schedule",
        "effective_date": "2026-01-01", "union": None,
        "notes": "Class 1386 Court Support Clerk 1, hourly $23.90 step A → $28.76 step E. SD Superior Court is state, but City has Court Support Clerk class for City Attorney's office."
    },
    ("San Francisco", "court_clerk"): {
        "entry_base": 68068, "top_base": 96668,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://careers.sf.gov/classifications/?classCode=1406",
        "source_type": "city_classification_page",
        "effective_date": "2026-01-03", "union": "SEIU Local 1021",
        "notes": "Class 1406 Senior Clerk used as closest city analog (SF Superior Court is state-employed). 10 steps."
    },
    # ---- parks worker ----
    ("Houston", "parks_worker"): {
        "entry_base": 35880, "top_base": 46150,
        "comparison_basis": "approximate", "employer_type": "city",
        "source_url": "https://www.houstontx.gov/hr/hrfiles/compensation/list_job_classifications_abc.pdf",
        "source_type": "city_classification_page",
        "effective_date": "2025", "union": None,
        "notes": "Class 511.9 Park Maintenance Aide, Grade 5. Open-range biweekly $1,380-$1,775 × 26."
    },
    ("Phoenix", "parks_worker"): {
        "entry_base": 32427, "top_base": 55806, "years_to_top": 11,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.phoenix.gov/content/dam/phoenix/hrsite/documents/class-and-comp-study/Salary-Range-Report.pdf",
        "source_type": "city_salary_range_report",
        "effective_date": "2025", "union": None,
        "notes": "Class 40060 Groundskeeper, Range 132. 12 steps $15.69-$26.83/hr."
    },
    ("San Antonio", "parks_worker"): {
        "entry_base": 37440, "top_base": 38953,
        "comparison_basis": "approximate", "employer_type": "city",
        "source_url": "https://www.sanantonio.gov/Portals/0/Files/EmployeeInformation/Compensation/PayPlan.pdf",
        "source_type": "city_pay_plan",
        "effective_date": "2025-10-01", "union": None,
        "notes": "Class 7579 Maintenance Worker, Pay Plan A Range 500. Closest non-supervisor parks/grounds title."
    },
    ("San Diego", "parks_worker"): {
        "entry_base": 49629, "top_base": 58635, "years_to_top": 4,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://www.sandiego.gov/sites/default/files/saltable.pdf",
        "source_type": "city_salary_schedule",
        "effective_date": "2026-01-01", "union": None,
        "notes": "Class 1467 Grounds Maintenance Worker 1. Hourly $23.78-$28.19 (steps A-E)."
    },
    ("San Francisco", "parks_worker"): {
        "entry_base": 80080, "top_base": 97422, "years_to_top": 4,
        "comparison_basis": "post_progression_base", "employer_type": "city",
        "source_url": "https://careers.sf.gov/classifications/?classCode=3417",
        "cba_url": "https://sfdhr.org/mous",
        "source_type": "city_classification_page",
        "effective_date": "2026-01-03", "union": "Laborers Local 261",
        "notes": "Class 3417 Gardener. Steps 1-5."
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
    print(f"Ingested {n} Wave 1B cells")


if __name__ == "__main__":
    main()
