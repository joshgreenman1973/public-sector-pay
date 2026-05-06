#!/usr/bin/env python3
"""Expand data schema for Stages 2-3:
- Add role_definitions registry (label, category, rank_order)
- Ingest East Coast police rank ladder results from Agent 1
- Set up empty stubs for cells the other agents will fill
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data.json"

# All role keys with category + display label + sort order within category.
ROLE_DEFINITIONS = {
    # Police category
    "police_officer": {"label": "Police: patrol officer (rank-and-file)", "category": "Police", "rank_order": 1},
    "police_detective": {"label": "Police: detective", "category": "Police", "rank_order": 2},
    "police_sergeant": {"label": "Police: sergeant", "category": "Police", "rank_order": 3},
    "police_lieutenant": {"label": "Police: lieutenant", "category": "Police", "rank_order": 4},
    "police_captain": {"label": "Police: captain", "category": "Police", "rank_order": 5},
    # Fire
    "firefighter": {"label": "Fire: firefighter (rank-and-file)", "category": "Fire", "rank_order": 1},
    # Sanitation
    "sanitation_worker": {"label": "Sanitation worker (city-employed)", "category": "Sanitation", "rank_order": 1},
    # Transit
    "transit_bus_operator": {"label": "Transit bus operator (regional authority)", "category": "Transit", "rank_order": 1},
    # Education
    "teacher": {"label": "K-12 public school teacher", "category": "Education", "rank_order": 1},
    # Other public sector
    "dispatcher_911": {"label": "911 dispatcher / public safety telecommunicator", "category": "Other public sector", "rank_order": 1},
    "librarian": {"label": "Public librarian", "category": "Other public sector", "rank_order": 2},
    "building_inspector": {"label": "Building inspector", "category": "Other public sector", "rank_order": 3},
    "civil_engineer": {"label": "Civil engineer (city)", "category": "Other public sector", "rank_order": 4},
    "court_clerk": {"label": "Court / municipal clerk", "category": "Other public sector", "rank_order": 5},
    "public_health_nurse": {"label": "Public health nurse", "category": "Other public sector", "rank_order": 6},
    "city_plumber": {"label": "City plumber (journey-level)", "category": "Other public sector", "rank_order": 7},
    "parks_worker": {"label": "Parks maintenance worker", "category": "Other public sector", "rank_order": 8},
}

# Police rank ladder data from East Coast agent (Stage 2). Each entry is
# (city_name, rank_key, fields...).
EAST_COAST_POLICE = {
    # Chicago — all 4 ranks fully sourced from Schedule D/E of 2025 Pay Plan
    ("Chicago", "police_detective"): {
        "entry_base": None, "top_base": 142962, "years_to_top": 20,
        "max_with_longevity": 152004, "max_years": 30,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.chicago.gov/content/dam/city/depts/dol/general/2025-Classification-and-Pay-Plan.pdf",
        "cba_url": "https://www.chicago.gov/content/dam/city/depts/dol/general/2025-Classification-and-Pay-Plan.pdf",
        "source_type": "city_pay_plan_schedule",
        "effective_date": "2025-01-01", "union": "FOP Lodge 7",
        "notes": "Schedule D Grade 3 Detective. Step 9 (20yr) = $142,962 max rate. Longevity: Step 10 (25yr) $147,582; Step 11 red-circle (30yr svc before 1/1/2006) $152,004."
    },
    ("Chicago", "police_sergeant"): {
        "entry_base": None, "top_base": 136230, "years_to_top": 20,
        "max_with_longevity": 144852, "max_years": 30,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.chicago.gov/content/dam/city/depts/dol/general/2025-Classification-and-Pay-Plan.pdf",
        "cba_url": "https://www.chicago.gov/content/dam/city/depts/dol/general/2025-Classification-and-Pay-Plan.pdf",
        "source_type": "city_pay_plan_schedule",
        "effective_date": "2025-01-01", "union": "PBPA Unit 156A",
        "notes": "Schedule E Grade 3 Sergeant (titles 9171/9176). Step 9 (20yr) max rate $136,230. Longevity Step 10 (25yr) $140,640; Step 11 red-circle $144,852."
    },
    ("Chicago", "police_lieutenant"): {
        "entry_base": None, "top_base": 153240, "years_to_top": 20,
        "max_with_longevity": 161910, "max_years": 30,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.chicago.gov/content/dam/city/depts/dol/general/2025-Classification-and-Pay-Plan.pdf",
        "cba_url": "https://www.chicago.gov/content/dam/city/depts/dol/general/2025-Classification-and-Pay-Plan.pdf",
        "source_type": "city_pay_plan_schedule",
        "effective_date": "2025-01-01", "union": "PBPA Unit 156B",
        "notes": "Schedule E Grade 4 Lieutenant (title 9173). Step 9 max rate $153,240. Longevity Step 10 (25yr) $157,926; Step 11 red-circle $161,910."
    },
    ("Chicago", "police_captain"): {
        "entry_base": None, "top_base": 167628, "years_to_top": 20,
        "max_with_longevity": 174264, "max_years": 30,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.chicago.gov/content/dam/city/depts/dol/general/2025-Classification-and-Pay-Plan.pdf",
        "cba_url": "https://www.chicago.gov/content/dam/city/depts/dol/general/2025-Classification-and-Pay-Plan.pdf",
        "source_type": "city_pay_plan_schedule",
        "effective_date": "2025-01-01", "union": "PBPA Unit 156",
        "notes": "Schedule E Grade 5 Captain (title 9175). Step 9 max rate $167,628. Longevity Step 10 (25yr) $171,780; Step 11 red-circle $174,264."
    },
    # NYC — detective and sergeant verified; lieutenant/captain are scanned PDFs
    ("New York", "police_detective"): {
        "entry_base": None, "top_base": 154751, "years_to_top": None,
        "max_with_longevity": 158093, "max_years": None,
        "comparison_basis": "post_progression_base",
        "source_url": "https://nycdetectives.org/current-salary-charts/",
        "cba_url": "https://www.nyc.gov/site/olr/labor/labor-uniformed-contracts.page",
        "source_type": "union_wage_chart",
        "effective_date": "2025-06-01", "union": "DEA",
        "notes": "Detective 1st Grade top base under DEA CBA 6/1/2022-5/31/2027 after 6/1/2025 3.50% raise. Det 2nd Grade $134,819; Det 3rd Grade $119,980. 2.25% service differential ($2,721+) at 5 yrs in rank. NB: 'Detective Specialist' titles under PBA contract are different and lower."
    },
    ("New York", "police_sergeant"): {
        "entry_base": 109651, "top_base": 134819, "years_to_top": 6,
        "max_with_longevity": 140212, "max_years": 6,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.nyc.gov/assets/olr/downloads/pdf/collectivebargaining/2021-2026/sba-unit-agreement-2021-2026.pdf",
        "cba_url": "https://www.nyc.gov/assets/olr/downloads/pdf/collectivebargaining/2021-2026/sba-unit-agreement-2021-2026.pdf",
        "source_type": "cba",
        "effective_date": "2024-12-10", "union": "SBA",
        "notes": "Per April 14, 2025 SBA Unit Agreement: incumbents below top step on 12/10/2024 moved to top step ($134,819). New sergeants follow 6-step schedule (Step 1 $109,651 → Step 6 $134,819). Top step rises to $140,212 effective 12/10/2025."
    },
    ("New York", "police_lieutenant"): {
        "entry_base": None, "top_base": None, "years_to_top": None,
        "comparison_basis": "needs_research",
        "source_url": "https://www.nyc.gov/assets/olr/downloads/pdf/collectivebargaining/2021-2026/lba-10-5-2023-unit-bargaining-agreement.pdf",
        "source_type": "needs_research",
        "union": "LBA",
        "notes": "LBA Unit Bargaining Agreement 2022-2027 PDF on OLR is image-only; could not extract base figures. 2017 base was $124,373 top step. Practitioner sources suggest current top base ~$155-175K but not from official source."
    },
    ("New York", "police_captain"): {
        "entry_base": None, "top_base": None, "years_to_top": None,
        "comparison_basis": "needs_research",
        "source_url": "https://www.nyc.gov/site/olr/labor/labor-uniformed-contracts.page",
        "source_type": "needs_research",
        "union": "CEA",
        "notes": "Most recent posted CEA executed contract on OLR is 2003-2012; current CEA agreement details not located in extractable official PDF. Practitioner sources suggest current top base ~$180-200K (unverified)."
    },
    # DC — all 4 ranks (Lt/Capt are FY23 figures since FY26 not posted)
    ("Washington, D.C.", "police_detective"): {
        "entry_base": None, "top_base": 138252, "years_to_top": None,
        "max_with_longevity": 166829, "max_years": 30,
        "comparison_basis": "post_progression_base",
        "source_url": "https://dchr.dc.gov/sites/default/files/dc/sites/DCHR/page_content/attachments/FY26%20MPD%20Union.pdf",
        "cba_url": "https://dchr.dc.gov/sites/default/files/dc/sites/DCHR/page_content/attachments/FY26%20MPD%20Union.pdf",
        "source_type": "official_salary_schedule",
        "effective_date": "2025-10-05", "union": "FOP/MPD Labor Committee",
        "notes": "Class 03 Detective FY26 schedule (4.25% raise 10/5/2025). Pay #3 Step 7 (top + 5-yr retention) = $138,252. Pay #1 base Step 7 = $126,361. Longevity 30 YOS Pay #8 Step 7 = $166,829."
    },
    ("Washington, D.C.", "police_sergeant"): {
        "entry_base": None, "top_base": 143054, "years_to_top": None,
        "max_with_longevity": 173745, "max_years": 30,
        "comparison_basis": "post_progression_base",
        "source_url": "https://dchr.dc.gov/sites/default/files/dc/sites/DCHR/page_content/attachments/FY26%20MPD%20Union.pdf",
        "cba_url": "https://dchr.dc.gov/sites/default/files/dc/sites/DCHR/page_content/attachments/FY26%20MPD%20Union.pdf",
        "source_type": "official_salary_schedule",
        "effective_date": "2025-10-05", "union": "FOP/MPD Labor Committee",
        "notes": "Class 04 Sergeant. Pay #1 Step 6 = $130,750 base. Pay #3 Step 6 (5-yr retention top) = $143,054. Longevity 30 YOS Step 6 = $173,745."
    },
    ("Washington, D.C.", "police_lieutenant"): {
        "entry_base": None, "top_base": 135535, "years_to_top": None,
        "max_with_longevity": 157416, "max_years": 30,
        "comparison_basis": "approximate",
        "pre_raise": True,
        "source_url": "https://dchr.dc.gov/sites/default/files/dc/sites/dchr/page_content/attachments/non_union_police_fy23.pdf",
        "source_type": "official_salary_schedule",
        "effective_date": "2022-10-09", "union": "Non-union (MPD Lt is non-bargaining)",
        "notes": "FY23 schedule (only one located). Class 05 Lieutenant Pay #4 Step 5 (5-yr retention top) = $135,535. Pay #1 base Step 5 = $123,878. FY26 figures should be ~10-12% higher reflecting subsequent COLAs."
    },
    ("Washington, D.C.", "police_captain"): {
        "entry_base": None, "top_base": 150904, "years_to_top": None,
        "max_with_longevity": 177345, "max_years": 30,
        "comparison_basis": "approximate",
        "pre_raise": True,
        "source_url": "https://dchr.dc.gov/sites/default/files/dc/sites/dchr/page_content/attachments/non_union_police_fy23.pdf",
        "source_type": "official_salary_schedule",
        "effective_date": "2022-10-09", "union": "Non-union",
        "notes": "FY23 schedule. Class 07 Captain Pay #4 Step 4 (5-yr retention top) = $150,904. Pay #1 base Step 4 = $137,925. FY26 figures should be ~10-12% higher."
    },
    # Boston — captain only (single Globe-cited number); others scanned PDFs
    ("Boston", "police_captain"): {
        "entry_base": None, "top_base": 194000, "years_to_top": None,
        "comparison_basis": "approximate",
        "source_url": "https://www.boston.gov/sites/default/files/file/2025/08/BPSOF%20Executive%20Order%20and%20Salary%20Scale%202020-2024.pdf",
        "cba_url": "https://www.boston.gov/sites/default/files/file/2024/06/BPSOF%20MOA%202020-2025_Final_Signed.pdf",
        "source_type": "agency_announcement",
        "effective_date": None, "union": "BPSOF",
        "notes": "$194,000 figure cited by Boston Globe (3/3/2026) for BPD captain base salary; not independently verified from extractable BPSOF salary scale (PDF is scanned image)."
    },
    ("Boston", "police_detective"): {
        "comparison_basis": "needs_research",
        "source_url": "https://www.boston.gov/sites/default/files/file/2025/08/BPDBS%2C%20Executive%20Order%20and%20Salary%20Scale%202020-2024.pdf",
        "cba_url": "https://www.boston.gov/sites/default/files/file/2024/05/BPDBS%20MOA%202020-2025_Final_Signed.pdf",
        "source_type": "needs_research",
        "union": "BPDBS",
        "notes": "BPDBS salary scale PDF is scanned image; not text-extractable. Needs OCR pass."
    },
    ("Boston", "police_sergeant"): {
        "comparison_basis": "needs_research",
        "source_url": "https://www.boston.gov/sites/default/files/file/2025/08/BPSOF%20Executive%20Order%20and%20Salary%20Scale%202020-2024.pdf",
        "source_type": "needs_research",
        "union": "BPSOF",
        "notes": "Salary scale shows top sergeant 3rd-year base around $109-117k depending on tour but rank labels are image-embedded; could not deterministically map figures to rank without OCR."
    },
    ("Boston", "police_lieutenant"): {
        "comparison_basis": "needs_research",
        "source_url": "https://www.boston.gov/sites/default/files/file/2025/08/BPSOF%20Executive%20Order%20and%20Salary%20Scale%202020-2024.pdf",
        "source_type": "needs_research",
        "union": "BPSOF",
        "notes": "Per Boston Globe 2025 reporting, top-paid Boston cops include lieutenants with base ~$160-180k (unverified)."
    },
    # Philadelphia — all 4 ranks scanned PDFs
    ("Philadelphia", "police_detective"): {
        "comparison_basis": "needs_research",
        "source_url": "https://fop5.org/wp-content/uploads/2025/09/OFFICIAL-FY-2026-PAYSCALES-FROM-RECRUIT-TO-C.-INSPt.pdf",
        "cba_url": "https://fop5.org/wp-content/uploads/2025/08/FOP-5-Act-111-Award-2025-2027.pdf",
        "source_type": "needs_research",
        "effective_date": "2025-07-01", "union": "FOP Lodge 5",
        "notes": "Official FY2026 FOP Lodge 5 payscale PDF (recruit to chief inspector) is scanned image; not text-extractable. 2025-2027 Act 111 Award gives 3.0%+1.5%+3.0%+1.5%."
    },
    ("Philadelphia", "police_sergeant"): {
        "comparison_basis": "needs_research",
        "source_url": "https://fop5.org/wp-content/uploads/2025/09/OFFICIAL-FY-2026-PAYSCALES-FROM-RECRUIT-TO-C.-INSPt.pdf",
        "source_type": "needs_research",
        "union": "FOP Lodge 5",
        "notes": "PPD career page indicates ~14% pay raise on promotion from corporal/detective to sergeant. Needs OCR."
    },
    ("Philadelphia", "police_lieutenant"): {
        "comparison_basis": "needs_research",
        "source_url": "https://fop5.org/wp-content/uploads/2025/09/OFFICIAL-FY-2026-PAYSCALES-FROM-RECRUIT-TO-C.-INSPt.pdf",
        "source_type": "needs_research",
        "union": "FOP Lodge 5",
        "notes": "Scanned image PDF. Needs OCR."
    },
    ("Philadelphia", "police_captain"): {
        "comparison_basis": "needs_research",
        "source_url": "https://fop5.org/wp-content/uploads/2025/09/OFFICIAL-FY-2026-PAYSCALES-FROM-RECRUIT-TO-C.-INSPt.pdf",
        "source_type": "needs_research",
        "union": "FOP Lodge 5",
        "notes": "Scanned image PDF. Needs OCR."
    },
}


def main():
    data = json.loads(DATA.read_text())

    # Add role definitions registry
    data["role_definitions"] = ROLE_DEFINITIONS

    # Update _metadata to reflect expanded scope
    data["_metadata"]["scope"] = (
        "Side-by-side comparison of contract base salary across 13 large U.S. cities "
        "for police (5 ranks), firefighter, sanitation, transit, K-12 teacher and "
        f"{sum(1 for r in ROLE_DEFINITIONS.values() if r['category'] == 'Other public sector')} "
        "other public-sector occupations. All figures sourced from city CBAs, official "
        "salary schedules and department careers pages — every cell links to its source."
    )

    # Ingest East Coast police data
    ingested = 0
    for (city_name, role_key), payload in EAST_COAST_POLICE.items():
        for c in data["cities"]:
            if c["city"] == city_name:
                c["roles"][role_key] = payload
                ingested += 1
                break
    print(f"Ingested {ingested} East Coast police-rank cells")
    print(f"Role definitions: {len(ROLE_DEFINITIONS)}")

    DATA.write_text(json.dumps(data, indent=2))
    print(f"Wrote {DATA}")


if __name__ == "__main__":
    main()
