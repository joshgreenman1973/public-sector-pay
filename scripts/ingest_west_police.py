#!/usr/bin/env python3
"""Ingest West Coast police rank ladder from Stage 2 agent."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data.json"

PAYLOADS = {
    # LAPD — current MOU 24/25 effective 6/29/2025
    ("Los Angeles", "police_detective"): {
        "entry_base": None, "top_base": 181614, "years_to_top": None,
        "max_with_longevity": 191010, "max_years": 20,
        "comparison_basis": "post_progression_base",
        "source_url": "https://cao.lacity.gov/mous/MOU24-22.pdf",
        "cba_url": "https://cao.lacity.gov/mous/MOU24-22.pdf",
        "source_type": "cba",
        "effective_date": "2025-06-29", "union": "LAPPL",
        "notes": "Detective III, class 2223-3, schedule 8, top step (Step 7) = $181,614. Longevity: +$120/biwk at 10y, +$240 at 15y, +$360 at 20y ($9,396/yr). Max with 20-yr longevity = $191,010 base."
    },
    ("Los Angeles", "police_sergeant"): {
        "entry_base": None, "top_base": 172051, "years_to_top": None,
        "max_with_longevity": 181447, "max_years": 20,
        "comparison_basis": "post_progression_base",
        "source_url": "https://cao.lacity.gov/mous/MOU24-22.pdf",
        "source_type": "cba",
        "effective_date": "2025-06-29", "union": "LAPPL",
        "notes": "Sergeant II, class 2227-2, schedule 7, top step = $172,051. Plus $9,396 longevity at 20y = $181,447."
    },
    ("Los Angeles", "police_lieutenant"): {
        "entry_base": None, "top_base": 202244, "years_to_top": None,
        "max_with_longevity": 237719, "max_years": None,
        "comparison_basis": "post_progression_base",
        "source_url": "https://cao.lacity.gov/mous/MOU24-22.pdf",
        "source_type": "cba",
        "effective_date": "2025-06-29", "union": "LAPPL",
        "notes": "Lieutenant II, class 2232-2, top step at schedule 10 = $202,244. With time-in-grade Lt II progresses through schedules 11/12/13 to $237,719."
    },
    ("Los Angeles", "police_captain"): {
        "entry_base": None, "top_base": 261522, "years_to_top": 0,
        "comparison_basis": "post_progression_base",
        "source_url": "https://cao.lacity.gov/mous/MOU25-27.pdf",
        "cba_url": "https://cao.lacity.gov/mous/MOU25-27.pdf",
        "source_type": "cba",
        "effective_date": "2025-06-29", "union": "LAPCO (MOU 25)",
        "notes": "Captain I, class 2244-1, range 9046, Step 7 = $261,522. Captain II $275,887; Captain III $291,225. Per Article 5.2, promotion places employee directly on Step 7."
    },
    # SF — single-step Q050/Q060/Q080
    ("San Francisco", "police_detective"): {
        "entry_base": None, "top_base": 176462, "years_to_top": 0,
        "comparison_basis": "post_progression_base",
        "source_url": "https://careers.sf.gov/classifications/?classCode=Q050",
        "source_type": "city_classification_page",
        "effective_date": "2025-07-01", "union": "POA",
        "notes": "SFPD has no separate Detective civil-service class. Investigators are titled 'Inspector' but classified as Q050 Sergeant. So Detective and Sergeant base figures are identical = $176,462. Single-step classification."
    },
    ("San Francisco", "police_sergeant"): {
        "entry_base": None, "top_base": 176462, "years_to_top": 0,
        "comparison_basis": "post_progression_base",
        "source_url": "https://careers.sf.gov/classifications/?classCode=Q050",
        "source_type": "city_classification_page",
        "effective_date": "2025-07-01", "union": "POA",
        "notes": "Q050 Sergeant: $84.84/hr × 2080 = $176,462. Single-step. Eligibility requires min 2 years SFPD service as Q002."
    },
    ("San Francisco", "police_lieutenant"): {
        "entry_base": None, "top_base": 201474, "years_to_top": 0,
        "comparison_basis": "post_progression_base",
        "source_url": "https://careers.sf.gov/classifications/?classCode=Q060",
        "source_type": "city_classification_page",
        "effective_date": "2025-07-01", "union": "POA",
        "notes": "Q060 Lieutenant: $96.86/hr × 2080 = $201,474. Single-step."
    },
    ("San Francisco", "police_captain"): {
        "entry_base": None, "top_base": 254592, "years_to_top": 0,
        "comparison_basis": "post_progression_base",
        "source_url": "https://careers.sf.gov/classifications/?classCode=Q080",
        "source_type": "city_classification_page",
        "effective_date": "2025-07-01", "union": "POA / management",
        "notes": "Q080 Captain: $122.40/hr × 2080 = $254,592. Single-step, exempt from overtime."
    },
    # San Diego
    ("San Diego", "police_detective"): {
        "entry_base": None, "top_base": 125715, "years_to_top": 4,
        "max_with_longevity": 132001, "max_years": None,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.sandiego.gov/sites/default/files/saltable.pdf",
        "cba_url": "https://www.sandiego.gov/sites/default/files/sdpd_pay_scale.pdf",
        "source_type": "city_salary_schedule",
        "effective_date": "2026-01-01", "union": "SDPOA",
        "notes": "Police Detective (1684), Step E top: $60.44/hr × 2080 = $125,715. Plus 5% Detective specialty pay. Longevity 5% per POA MOU Art. 63."
    },
    ("San Diego", "police_sergeant"): {
        "entry_base": None, "top_base": 145371, "years_to_top": 1,
        "max_with_longevity": 152640, "max_years": None,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.sandiego.gov/sites/default/files/saltable.pdf",
        "source_type": "city_salary_schedule",
        "effective_date": "2026-01-01", "union": "SDPOA",
        "notes": "Police Sergeant (1696), Step E: $69.89/hr × 2080 = $145,371. With 5% longevity = $152,640."
    },
    ("San Diego", "police_lieutenant"): {
        "entry_base": None, "top_base": 184163, "years_to_top": 1,
        "max_with_longevity": 193371, "max_years": None,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.sandiego.gov/sites/default/files/saltable.pdf",
        "source_type": "city_salary_schedule",
        "effective_date": "2026-01-01", "union": "SDPOA",
        "notes": "Police Lieutenant (1683), Step E: $88.54/hr × 2080 = $184,163. With 5% longevity = $193,371."
    },
    ("San Diego", "police_captain"): {
        "entry_base": None, "top_base": 218816, "years_to_top": 1,
        "max_with_longevity": 229757, "max_years": None,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.sandiego.gov/sites/default/files/saltable.pdf",
        "source_type": "city_salary_schedule",
        "effective_date": "2026-01-01", "union": "SDPOA / unrep mgmt",
        "notes": "Police Captain (1680), Step E: $105.20/hr × 2080 = $218,816."
    },
    # Seattle
    ("Seattle", "police_detective"): {
        "entry_base": None, "top_base": 160418, "years_to_top": 4.5,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.seattle.gov/documents/departments/opa/legislation/2024-2027%20spog%20cba%20w%20moas%20links%20-%20signed.pdf",
        "cba_url": "https://www.seattle.gov/documents/departments/opa/legislation/2024-2027%20spog%20cba%20w%20moas%20links%20-%20signed.pdf",
        "source_type": "cba",
        "effective_date": "2025-12-31", "union": "SPOG",
        "notes": "Detective in Seattle is an ASSIGNMENT premium (4% of base) on top of Police Officer top step, NOT a separate rank. Top-step PO base $154,248 × 1.04 = $160,418. Detective-Homicide/CSI/FIT = 6% premium ($163,503)."
    },
    ("Seattle", "police_sergeant"): {
        "entry_base": None, "top_base": 177480, "years_to_top": 1.5,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.seattle.gov/documents/departments/opa/legislation/2024-2027%20spog%20cba%20w%20moas%20links%20-%20signed.pdf",
        "source_type": "cba",
        "effective_date": "2025-12-31", "union": "SPOG",
        "notes": "Police Sergeant top step (18 mos) = $14,790/mo × 12 = $177,480. Patrol premium 1.5% adds for patrol sergeants."
    },
    ("Seattle", "police_lieutenant"): {
        "entry_base": None, "top_base": 217668, "years_to_top": 2.5,
        "max_with_longevity": 245965, "max_years": 30,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.seattle.gov/documents/departments/opa/legislation/spma%202024%20to%202027%20cba%20final%202025-09-24%20for%20signature%20-%20signed.pdf",
        "cba_url": "https://www.seattle.gov/documents/departments/opa/legislation/spma%202024%20to%202027%20cba%20final%202025-09-24%20for%20signature%20-%20signed.pdf",
        "source_type": "cba",
        "effective_date": "2025-12-31", "union": "SPMA",
        "notes": "Lieutenant top step (30 mos) effective 12/31/2025 = $18,139/mo × 12 = $217,668. Longevity per Appendix A.6: 6% at 15y, 7% at 20y, 12% at 25y, 13% at 30y → max ~$245,965."
    },
    ("Seattle", "police_captain"): {
        "entry_base": None, "top_base": 258852, "years_to_top": 2.5,
        "comparison_basis": "post_progression_base",
        "source_url": "https://www.seattle.gov/documents/departments/opa/legislation/spma%202024%20to%202027%20cba%20final%202025-09-24%20for%20signature%20-%20signed.pdf",
        "source_type": "cba",
        "effective_date": "2025-12-31", "union": "SPMA",
        "notes": "Captain top step (30 mos) effective 12/31/2025 = $21,571/mo × 12 = $258,852. Precinct Captain assignment +6%; Violent Crimes/Night/Traffic +2-3%."
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
    print(f"Ingested {n} West Coast police-rank cells")


if __name__ == "__main__":
    main()
