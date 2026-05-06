#!/usr/bin/env python3
"""Ingest K-12 teacher schedule from Stage 3 agent.
Maps to existing role schema:
  entry_base       = BA Step 1 entry
  top_base         = BA-lane top step (where defined)
  max_with_longevity = MA-lane top step (or doctorate top where district has it)
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data.json"

T = {
    "New York": {
        "entry_base": 64789, "top_base": 120408, "years_to_top": 22,
        "max_with_longevity": 122583,
        "comparison_basis": "post_progression_base",
        "source_url": "https://files.uft.org/contract2023/DOE-salary-schedules.pdf",
        "source_type": "cba",
        "effective_date": "2024-25", "union": "UFT",
        "notes": "NYC DOE. Lanes BA C1, BA+30 C1+PD, MA C2, MA+30 C6, etc. Step 8B reached ~year 7-8; longevity differentials L5/L10/L13/L15/L18/L20/L22 push to true top at ~22 years. Top base shown is BA C1 8B+L22; max_with_longevity is MA C2 8B+L22."
    },
    "Los Angeles": {
        "entry_base": 66639, "top_base": None, "years_to_top": None,
        "max_with_longevity": 116383,
        "comparison_basis": "approximate",
        "source_url": "https://www.lausd.org/cms/lib/CA01000043/Centricity/domain/280/salary%20tables/T_Table_JulDec2024.pdf",
        "source_type": "cba",
        "effective_date": "2024-25", "union": "UTLA",
        "notes": "LAUSD T-table. Pay Scale Group 1 Level 1 = $66,639. No clean 'BA only top step' — advancement requires units beyond BA. MA top w/ DR differential + 4 Career Increments on C-basis = $116,383."
    },
    "Chicago": {
        "entry_base": 64469, "top_base": 105635, "years_to_top": 26,
        "max_with_longevity": 112266,
        "comparison_basis": "approximate",
        "source_url": "https://contract.ctulocal1.org/cps/a-1a",
        "source_type": "cba",
        "effective_date": "2024-25", "union": "CTU",
        "notes": "CPS, 208-day. Lanes I (BA) through VI (PhD/2 Masters). Lane I Step 1 = $64,470. 26 steps; Step 26 is COLA-only. BA top approx $105,635; MA Lane III approx $112,266 (per pre-correction 2024-25 figures)."
    },
    "Houston": {
        "entry_base": 64000, "top_base": 89500, "years_to_top": 40,
        "max_with_longevity": None,
        "comparison_basis": "post_progression_base",
        "source_url": "https://teacherquality.nctq.org/dmsView/houston_2425",
        "source_type": "cba",
        "effective_date": "2024-25", "union": "Non-CB (TX); HFT/HEA prof. associations",
        "notes": "HISD Non-NES 10-month: Step 0 $64,000 → Step 40 $89,500. No BA/MA lane differentiation (TX standard). NES (New Education System) campuses use a separate subject-specific table $65k-$101k+ depending on grade/subject."
    },
    "Phoenix": {
        "entry_base": 52000, "top_base": None, "years_to_top": None,
        "max_with_longevity": 58127,
        "comparison_basis": "approximate",
        "source_url": "https://www.pxu.org/documents/departments/talent-division%2Fjobs/employment/salary-schedules-2024-2025/640658",
        "source_type": "department_careers_page",
        "effective_date": "2024-25", "union": "PUCSO/CSEA",
        "notes": "Phoenix Union HSD. Live PDF page is JS-loaded, can't auto-fetch. District publicly states minimum starting $52,000 / $58,127 with master's; avg salary 'over $70,000' per district announcement. Phoenix is split among many K-8 districts; PUHSD is the largest secondary district."
    },
    "Philadelphia": {
        "entry_base": 54146, "top_base": 80821, "years_to_top": 11,
        "max_with_longevity": 91273,
        "comparison_basis": "post_progression_base",
        "source_url": "https://pft.org/sites/default/files/media/documents/2024/2024-2025%20PFT%20Salary%20Schedule%20(2)_0.pdf",
        "source_type": "cba",
        "effective_date": "2024-25", "union": "PFT",
        "notes": "10-month Teacher schedule, Steps 1-11. BA Step 11 $80,821; MA Step 11 $91,273; MA+30 $99,534; Doctorate $103,512. Senior Career Teacher (post-Step 11) $107,495. Includes 5% raise per Sept 2024 contract extension."
    },
    "San Antonio": {
        "entry_base": 58400, "top_base": 74178, "years_to_top": 30,
        "max_with_longevity": 76178,
        "comparison_basis": "approximate",
        "source_url": "https://www.saisd.net/page/compensation-resource-manual",
        "source_type": "department_careers_page",
        "effective_date": "2024-25", "union": "SA Alliance of Teachers (no CB)",
        "notes": "SAISD. 2024-25 starting $58,400 (raised to $60,000 BA / $62,000 MA for 2025-26). Top Step 30 figures from 2025-26 schedule (~$74k BA / $76k MA). 2024-25 figures slightly lower."
    },
    "San Diego": {
        "entry_base": 58902, "top_base": 93087, "years_to_top": 17,
        "max_with_longevity": 121652,
        "comparison_basis": "post_progression_base",
        "source_url": "https://sandiegounified.community.diligentoneplatform.com/document/4c0d8d70-aedc-46f7-af93-e1cac75af5e3/",
        "source_type": "cba",
        "effective_date": "2024-25", "union": "SDEA",
        "notes": "Salary Plan 0160, 184-day. Grades 010 (BA) → 014 (BA+90 w/MA). 17 steps; longevity stipend at step 76. Top base shown is Grade 010 (BA) Step 17 $93,087; max_with_longevity is highest Grade 014 Step 17 $121,652."
    },
    "Dallas": {
        "entry_base": 62000, "top_base": 66500, "years_to_top": 10,
        "max_with_longevity": 104000,
        "comparison_basis": "approximate",
        "source_url": "https://teacherquality.nctq.org/dmsView/DallasISD2024-2025CompensationHandbook100424",
        "source_type": "department_careers_page",
        "effective_date": "2024-25", "union": "Alliance-AFT (no CB)",
        "notes": "Dallas ISD Teachers Introductory Compensation Schedule (new hires only): Novice $62,000 → Step 10+ $66,500. After year 1, returning teachers move to Teacher Excellence Initiative (TEI) effectiveness-based pay (Progressing/Proficient/Exemplary/Master/Distinguished, $65k-$104k+). max_with_longevity shown = TEI Distinguished ceiling. Average teacher base = $70,217."
    },
    "San Francisco": {
        "entry_base": 73689, "top_base": 109618, "years_to_top": 21,
        "max_with_longevity": None,
        "comparison_basis": "post_progression_base",
        "source_url": "https://uesf.org/members/contracts-salary-schedules/",
        "source_type": "cba",
        "effective_date": "2024-25", "union": "UESF",
        "notes": "SFUSD. PSGs by credential and units beyond BA: B6 (BA <30), B7 (BA+30-59), B8 (BA+60+/MA). B6 Step 1 (BA only) $73,689 total; B6 step 21 $109,618 (last step). B8 (BA+60+/MA) substantially higher. Plus QTEA + FWEA add-ons."
    },
    "Boston": {
        "entry_base": 66043, "top_base": 110057, "years_to_top": 9,
        "max_with_longevity": 116082,
        "comparison_basis": "post_progression_base",
        "source_url": "https://btu.org/contracts/",
        "source_type": "cba",
        "effective_date": "2024-25", "union": "BTU",
        "notes": "BPS, 9-step traditional schedule. Lanes Bachelors, B+15, Masters, M+15..M+75, Doctorate. Figures are BTU 9/1/2023 schedule + 2.5% per 2024-27 contract retro to 9/1/2024. BA Step 1 $66,043; BA Step 9 $110,057; MA Step 9 $116,082."
    },
    "Seattle": {
        "entry_base": 61578, "top_base": 84947, "years_to_top": 12,
        "max_with_longevity": 118665,
        "comparison_basis": "post_progression_base",
        "source_url": "https://mysps.seattleschools.org/wp-content/uploads/sites/106/2024/07/FINAL-Certificated-Non-Supervisory-3.7-2024-25.pdf",
        "source_type": "cba",
        "effective_date": "2024-25", "union": "SEA",
        "notes": "SPS Lanes 100 (BA) → 906 (PhD). Lane 100 Step 1 base $61,578 (180-day); Lane 100 caps at Step 12 base $84,947 (TOTAL with contractual/tech/responsibility days $102,025). Lane 906 (PhD) Step 15 base $118,665. Advancement requires both years AND credit hours."
    },
    "Washington, D.C.": {
        "entry_base": 64640, "top_base": 102498, "years_to_top": 16,
        "max_with_longevity": 126474,
        "comparison_basis": "post_progression_base",
        "source_url": "https://dcps.dc.gov/sites/default/files/dc/sites/dcps/page_content/attachments/ET%2015%20FY%202024-2028%20Pay%20Schedule.pdf",
        "source_type": "cba",
        "effective_date": "2024-25", "union": "WTU",
        "notes": "DCPS ET-15 10-month schedule. Lanes Bachelors, BA+15, BA+30/Masters, MA+30, MA+60/PhD. Steps 1-11, 12-15 band, then 16. BA top Step 12-15 $102,498 (BA does not get Step 16). MA top Step 16 $126,474. MA+60/PhD top Step 16 $133,623."
    },
}


def main():
    data = json.loads(DATA.read_text())
    cities_by_name = {c["city"]: c for c in data["cities"]}
    n = 0
    for city, payload in T.items():
        cities_by_name[city]["roles"]["teacher"] = payload
        n += 1
    DATA.write_text(json.dumps(data, indent=2))
    print(f"Ingested {n} teacher cells")


if __name__ == "__main__":
    main()
