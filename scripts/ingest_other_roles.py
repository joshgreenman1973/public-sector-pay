#!/usr/bin/env python3
"""Ingest 'other public-sector roles' agent output. Mostly SF + NYC verified;
rest mark needs_research with the correct source URL for follow-up.
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data.json"

CITY_KEY_MAP = {
    "NewYork": "New York", "LosAngeles": "Los Angeles", "Chicago": "Chicago",
    "Houston": "Houston", "Phoenix": "Phoenix", "Philadelphia": "Philadelphia",
    "SanAntonio": "San Antonio", "SanDiego": "San Diego", "Dallas": "Dallas",
    "SanFrancisco": "San Francisco", "Boston": "Boston", "Seattle": "Seattle",
    "WashingtonDC": "Washington, D.C.",
}

# Verified cells only (everything else gets a needs_research stub built dynamically)
VERIFIED = {
    "dispatcher_911": {
        "New York": {
            "entry_base": 42976, "top_base": 58189, "years_to_top": 5,
            "comparison_basis": "post_progression_base",
            "source_url": "https://www.nyc.gov/site/nypd/careers/civilians/police-communications-technicians.page",
            "source_type": "department_careers_page",
            "effective_date": "2024", "union": "CWA Local 1180 / DC 37",
            "notes": "Police Communications Technician. Top step ~5 yrs; base only, excludes night-shift differential."
        },
        "San Francisco": {
            "entry_base": 113516, "top_base": 144872, "years_to_top": 5,
            "comparison_basis": "post_progression_base",
            "source_url": "https://careers.sf.gov/classifications/?classCode=8238",
            "source_type": "city_classification_page",
            "effective_date": "2026-01-03", "union": "SEIU Local 1021",
            "notes": "Public Safety Communications Dispatcher (8238). 6 steps; biweekly $4,366 entry → $5,572 top."
        },
        "Seattle": {
            "entry_base": 67000, "top_base": 90000,
            "comparison_basis": "approximate",
            "source_url": "https://www.seattle.gov/human-resources/compensation",
            "source_type": "department_careers_page",
            "notes": "Police Communications Dispatcher I. Range from City job postings; needs cross-check vs current pay schedule."
        },
    },
    "civil_engineer": {
        "San Francisco": {
            "entry_base": 106210, "top_base": 129064, "years_to_top": 5,
            "comparison_basis": "post_progression_base",
            "source_url": "https://careers.sf.gov/classifications/?classCode=5201",
            "source_type": "city_classification_page",
            "effective_date": "2026", "union": "IFPTE Local 21",
            "notes": "Junior Engineer (Civil) (5201). Civil specialty range; mech/env specialties slightly higher."
        },
    },
    "city_plumber": {
        "San Francisco": {
            "entry_base": 124566, "top_base": 151450, "years_to_top": 4,
            "comparison_basis": "post_progression_base",
            "source_url": "https://careers.sf.gov/classifications/?classCode=7388",
            "source_type": "city_classification_page",
            "effective_date": "2026-01-03", "union": "UA Plumbers & Pipefitters Local 38",
            "notes": "Utility Plumber (7388). Per MOU, new hires enter at Step 5; 5-step ladder."
        },
    },
}

# For unverified cells, populate a stub with source URL so the cell still
# shows in the UI as 'needs_research' with the right link for follow-up.
ALL_ROLES = ["dispatcher_911", "librarian", "building_inspector", "civil_engineer",
             "court_clerk", "public_health_nurse", "city_plumber", "parks_worker"]
ALL_CITIES = list(CITY_KEY_MAP.values())

# A single best-known source URL per (role, city) so the gap rows still link to a starting point.
DEFAULT_URLS = {
    "dispatcher_911": {
        "New York": "https://www.nyc.gov/site/nypd/careers/civilians/police-communications-technicians.page",
        "Los Angeles": "https://personnel.lacity.gov/jobs/position-information/index.cfm?job_id=2207",
        "Chicago": "https://www.chicago.gov/content/dam/city/depts/dol/general/2025-Classification-and-Pay-Plan.pdf",
        "Houston": "https://www.houstontx.gov/hr/compensation/job-classifications.html",
        "Phoenix": "https://www.phoenix.gov/content/dam/phoenix/hrsite/documents/class-and-comp-study/Salary-Range-Report.pdf",
        "Philadelphia": "https://www.phila.gov/departments/office-of-human-resources/careers/pay-ranges/",
        "San Antonio": "https://www.sanantonio.gov/Portals/0/Files/EmployeeInformation/Compensation/PayPlan.pdf",
        "San Diego": "https://www.sandiego.gov/sites/default/files/saltable.pdf",
        "Dallas": "https://dallascityhall.com/departments/humanresources/PublishingImages/Pages/classification_compensation/Civilian%20Pay%20Schedule%2001.01.25.pdf",
        "Boston": "https://www.boston.gov/departments/human-resources",
        "Washington, D.C.": "https://dchr.dc.gov/page/fiscal-year-2025-union-salary-schedules",
    },
}

# Use NYC DCAS, LA personnel, Chicago Pay Plan, etc. as the default fallback URL for any role.
GENERIC_DEFAULT = {
    "New York": "https://www.nyc.gov/site/dcas/employees/wage-schedules.page",
    "Los Angeles": "https://cao.lacity.gov/mous",
    "Chicago": "https://www.chicago.gov/content/dam/city/depts/dol/general/2025-Classification-and-Pay-Plan.pdf",
    "Houston": "https://www.houstontx.gov/hr/compensation/job-classifications.html",
    "Phoenix": "https://www.phoenix.gov/content/dam/phoenix/hrsite/documents/class-and-comp-study/Salary-Range-Report.pdf",
    "Philadelphia": "https://www.phila.gov/departments/office-of-human-resources/careers/pay-ranges/",
    "San Antonio": "https://www.sanantonio.gov/Portals/0/Files/EmployeeInformation/Compensation/PayPlan.pdf",
    "San Diego": "https://www.sandiego.gov/sites/default/files/saltable.pdf",
    "Dallas": "https://dallascityhall.com/departments/humanresources/PublishingImages/Pages/classification_compensation/Civilian%20Pay%20Schedule%2001.01.25.pdf",
    "San Francisco": "https://careers.sf.gov/classifications/",
    "Boston": "https://www.boston.gov/departments/human-resources",
    "Seattle": "https://www.seattle.gov/human-resources/compensation",
    "Washington, D.C.": "https://dchr.dc.gov/page/fiscal-year-2025-union-salary-schedules",
}


def main():
    data = json.loads(DATA.read_text())
    cities_by_name = {c["city"]: c for c in data["cities"]}

    ingested = 0
    stubbed = 0
    for role in ALL_ROLES:
        verified_for_role = VERIFIED.get(role, {})
        for city in ALL_CITIES:
            c = cities_by_name[city]
            if role in c["roles"]:
                continue  # don't overwrite existing
            if city in verified_for_role:
                c["roles"][role] = verified_for_role[city]
                ingested += 1
            else:
                # stub
                url = DEFAULT_URLS.get(role, {}).get(city) or GENERIC_DEFAULT.get(city, "")
                c["roles"][role] = {
                    "entry_base": None, "top_base": None,
                    "comparison_basis": "needs_research",
                    "source_type": "needs_research",
                    "source_url": url,
                    "notes": "Data not yet extracted. Click source link to look up in city's pay schedule."
                }
                stubbed += 1

    print(f"Ingested {ingested} verified cells; stubbed {stubbed} cells with source URLs.")
    DATA.write_text(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
