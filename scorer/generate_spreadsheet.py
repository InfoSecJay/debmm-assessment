#!/usr/bin/env python3
"""
DEBMM Assessment Spreadsheet Generator

Generates an all-in-one Excel spreadsheet with:
  - Tab 1: Instructions
  - Tab 2: Assessment (fillable with dropdowns and auto-scoring)
  - Tab 3: Results Dashboard (auto-calculated scores, heatmap, recommendations)
  - Tab 4: Rubric Reference

Usage:
    python generate_spreadsheet.py [--output debmm-assessment.xlsx]
    python generate_spreadsheet.py --mode audit --output audit-assessment.xlsx
"""

import argparse
from pathlib import Path

import yaml
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_RUBRIC = PROJECT_ROOT / "rubric" / "rubric.yaml"
DEFAULT_QUESTIONNAIRE = PROJECT_ROOT / "questionnaire" / "questionnaire.yaml"

# ── Style constants ──────────────────────────────────────────────────────────

NAVY = "1B2A4A"
DARK_BLUE = "2C3E6B"
MED_BLUE = "4472C4"
LIGHT_BLUE = "D6E4F0"
LIGHTER_BLUE = "E9EFF7"
WHITE = "FFFFFF"
LIGHT_GRAY = "F2F2F2"
MED_GRAY = "D9D9D9"
DARK_GRAY = "404040"
GREEN = "70AD47"
YELLOW = "FFC000"
ORANGE = "ED7D31"
RED = "C00000"
LIGHT_GREEN = "E2EFDA"
LIGHT_YELLOW = "FFF2CC"
LIGHT_ORANGE = "FCE4D6"
LIGHT_RED = "F4CCCC"

FONT_TITLE = Font(name="Calibri", size=18, bold=True, color=WHITE)
FONT_HEADER = Font(name="Calibri", size=11, bold=True, color=WHITE)
FONT_SUBHEADER = Font(name="Calibri", size=11, bold=True, color=DARK_GRAY)
FONT_BODY = Font(name="Calibri", size=11, color=DARK_GRAY)
FONT_BODY_BOLD = Font(name="Calibri", size=11, bold=True, color=DARK_GRAY)
FONT_SMALL = Font(name="Calibri", size=10, color=DARK_GRAY)
FONT_LINK = Font(name="Calibri", size=11, color=MED_BLUE, underline="single")
FONT_TIER = Font(name="Calibri", size=14, bold=True, color=NAVY)
FONT_SCORE = Font(name="Calibri", size=24, bold=True, color=NAVY)
FONT_SCORE_MED = Font(name="Calibri", size=14, bold=True, color=NAVY)

FILL_NAVY = PatternFill("solid", fgColor=NAVY)
FILL_DARK_BLUE = PatternFill("solid", fgColor=DARK_BLUE)
FILL_MED_BLUE = PatternFill("solid", fgColor=MED_BLUE)
FILL_LIGHT_BLUE = PatternFill("solid", fgColor=LIGHT_BLUE)
FILL_LIGHTER_BLUE = PatternFill("solid", fgColor=LIGHTER_BLUE)
FILL_WHITE = PatternFill("solid", fgColor=WHITE)
FILL_LIGHT_GRAY = PatternFill("solid", fgColor=LIGHT_GRAY)
FILL_GREEN = PatternFill("solid", fgColor=LIGHT_GREEN)
FILL_YELLOW = PatternFill("solid", fgColor=LIGHT_YELLOW)
FILL_ORANGE = PatternFill("solid", fgColor=LIGHT_ORANGE)
FILL_RED = PatternFill("solid", fgColor=LIGHT_RED)

ALIGN_WRAP = Alignment(horizontal="left", vertical="top", wrap_text=True)
ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_CENTER_TOP = Alignment(horizontal="center", vertical="top", wrap_text=True)
ALIGN_LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)

THIN_BORDER = Border(
    left=Side(style="thin", color=MED_GRAY),
    right=Side(style="thin", color=MED_GRAY),
    top=Side(style="thin", color=MED_GRAY),
    bottom=Side(style="thin", color=MED_GRAY),
)


def load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def style_cell(cell, font=None, fill=None, alignment=None, border=None):
    if font:
        cell.font = font
    if fill:
        cell.fill = fill
    if alignment:
        cell.alignment = alignment
    if border:
        cell.border = border


def apply_conditional_formatting(ws, cell_range):
    """Apply red/orange/yellow/green conditional formatting to a score range."""
    ws.conditional_formatting.add(
        cell_range,
        CellIsRule(operator="between", formula=["1", "1.49"], fill=FILL_RED),
    )
    ws.conditional_formatting.add(
        cell_range,
        CellIsRule(operator="between", formula=["1.5", "2.49"], fill=FILL_ORANGE),
    )
    ws.conditional_formatting.add(
        cell_range,
        CellIsRule(operator="between", formula=["2.5", "3.49"], fill=FILL_YELLOW),
    )
    ws.conditional_formatting.add(
        cell_range,
        CellIsRule(operator="between", formula=["3.5", "5"], fill=FILL_GREEN),
    )


# ── Tab 1: Instructions ─────────────────────────────────────────────────────


def build_instructions_tab(wb: Workbook):
    ws = wb.active
    ws.title = "Instructions"
    ws.sheet_properties.tabColor = NAVY

    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 85
    ws.column_dimensions["C"].width = 3

    row = 1

    # Title banner
    ws.merge_cells("A1:C1")
    ws.row_dimensions[1].height = 50
    c = ws["A1"]
    c.value = "  DEBMM Assessment Tool"
    style_cell(c, FONT_TITLE, FILL_NAVY, Alignment(horizontal="left", vertical="center"))
    for col in ["A", "B", "C"]:
        ws[f"{col}1"].fill = FILL_NAVY

    row = 3

    instructions = [
        ("About This Assessment", [
            "This spreadsheet assesses your detection engineering team's maturity using Elastic's "
            "Detection Engineering Behavior Maturity Model (DEBMM), enriched with organizational "
            "dimensions from detectionengineering.io.",
            "",
            "It covers 21 criteria across 7 categories, with 56 questions total.",
        ]),
        ("How to Use", [
            "1. Fill in your organization details at the top of the Assessment tab",
            "2. Answer each question using the dropdown menus or text fields",
            "3. For Yes/No questions: select from the dropdown",
            "4. For Scale questions (1-5): select from the dropdown",
            "5. For Text questions: type your response in the 'Your Answer' column",
            "6. Use the 'Evidence / Notes' column for supporting details (optional but recommended)",
            "7. Switch to the Results Dashboard tab to see your scores automatically calculated",
        ]),
        ("Maturity Levels", [
            "Each criterion is scored on a 1-5 scale:",
            "",
            "  1 - Initial:      Minimal or no structured activity",
            "  2 - Repeatable:  Sporadic, inconsistent efforts",
            "  3 - Defined:       Regular, documented processes followed consistently",
            "  4 - Managed:     Comprehensive, well-integrated with measurable outcomes",
            "  5 - Optimized:   Fully automated, continuously improving",
        ]),
        ("DEBMM Tiers", [
            "Tier 0 - Foundation:     Basic groundwork (rule development, maintenance, roadmaps, threat modeling)",
            "Tier 1 - Basic:              Baseline rules, version control, telemetry, testing",
            "Tier 2 - Intermediate:  FP reduction, gap analysis, internal validation",
            "Tier 3 - Advanced:       FN triage, external validation, advanced TTP coverage",
            "Tier 4 - Expert:            Threat hunting, automation, AI/LLM integration",
            "",
            "Enrichment - People & Organization:  Team structure, training, leadership",
            "Enrichment - Process & Governance:   Lifecycle, metrics, collaboration",
        ]),
        ("Tier Determination", [
            "Your achieved tier is the highest tier where ALL criteria in that tier (and all lower "
            "tiers) score >= 3.0 (Defined level). This enforces the progressive nature of the "
            "model - you need solid foundations before claiming advanced maturity.",
        ]),
        ("Three Scoring Paths", [
            "1. This Spreadsheet: Fill it out and scores calculate automatically in the Dashboard tab",
            "2. Python CLI: Export answers to YAML and run scorer/score.py for a detailed report",
            "3. LLM-Assisted: Run scorer/llm_scorer.py to have AI score your text answers and "
            "generate improvement recommendations",
        ]),
        ("References", [
            "Elastic DEBMM: https://www.elastic.co/security-labs/elastic-releases-debmm",
            "Detection Engineering Maturity Matrix: https://detectionengineering.io/",
            "MITRE ATT&CK: https://attack.mitre.org/",
        ]),
    ]

    for section_title, lines in instructions:
        ws.cell(row=row, column=2, value=section_title)
        style_cell(ws.cell(row=row, column=2), FONT_TIER, alignment=ALIGN_LEFT)
        row += 1

        for line in lines:
            ws.cell(row=row, column=2, value=line)
            style_cell(ws.cell(row=row, column=2), FONT_BODY, alignment=ALIGN_WRAP)
            row += 1

        row += 1

    return ws


# ── Tab 2: Assessment ────────────────────────────────────────────────────────


def build_assessment_tab(wb: Workbook, questionnaire: dict, rubric: dict, mode: str):
    ws = wb.create_sheet("Assessment")
    ws.sheet_properties.tabColor = MED_BLUE

    # Column widths
    col_widths = {
        "A": 10,   # ID
        "B": 12,   # Tier
        "C": 30,   # Criterion
        "D": 10,   # Type
        "E": 65,   # Question
        "F": 18,   # Your Answer
        "G": 12,   # Auto Score
        "H": 50,   # Evidence / Notes
    }
    for col, width in col_widths.items():
        ws.column_dimensions[col].width = width

    # ── Metadata section ─────────────────────────────────────────────────
    ws.merge_cells("A1:H1")
    ws.row_dimensions[1].height = 40
    c = ws["A1"]
    c.value = "  DEBMM Assessment"
    style_cell(c, FONT_TITLE, FILL_NAVY, Alignment(horizontal="left", vertical="center"))
    for col in "ABCDEFGH":
        ws[f"{col}1"].fill = FILL_NAVY

    labels = ["Organization:", "Assessor Name:", "Assessor Role:", "Date:", "Assessment Type:"]
    for i, label in enumerate(labels):
        r = 3 + i
        ws.cell(row=r, column=2, value=label)
        style_cell(ws.cell(row=r, column=2), FONT_BODY_BOLD, alignment=ALIGN_LEFT)
        ws.merge_cells(f"C{r}:E{r}")
        style_cell(ws.cell(row=r, column=3), FONT_BODY, FILL_LIGHTER_BLUE, ALIGN_LEFT, THIN_BORDER)

    # Pre-fill assessment type
    ws.cell(row=7, column=3, value="Self-Assessment" if mode == "self" else "Audit")

    # Type dropdown for assessment type
    dv_type = DataValidation(type="list", formula1='"Self-Assessment,Audit"', allow_blank=False)
    dv_type.error = "Please select Self-Assessment or Audit"
    dv_type.errorTitle = "Invalid Entry"
    ws.add_data_validation(dv_type)
    dv_type.add(ws.cell(row=7, column=3))

    # ── Data validations ─────────────────────────────────────────────────
    dv_yesno = DataValidation(type="list", formula1='"Yes,No"', allow_blank=True)
    dv_yesno.error = "Please select Yes or No"
    dv_yesno.errorTitle = "Invalid Entry"
    dv_yesno.prompt = "Select Yes or No"
    dv_yesno.promptTitle = "Answer"
    ws.add_data_validation(dv_yesno)

    dv_scale = DataValidation(type="list", formula1='"1,2,3,4,5"', allow_blank=True)
    dv_scale.error = "Please select a value from 1 to 5"
    dv_scale.errorTitle = "Invalid Entry"
    dv_scale.prompt = "Select 1 (Initial) through 5 (Optimized)"
    dv_scale.promptTitle = "Maturity Rating"
    ws.add_data_validation(dv_scale)

    # ── Column headers ───────────────────────────────────────────────────
    header_row = 9
    headers = ["ID", "Tier", "Criterion", "Type", "Question", "Your Answer", "Score", "Evidence / Notes"]
    for col_idx, header in enumerate(headers, 1):
        c = ws.cell(row=header_row, column=col_idx, value=header)
        style_cell(c, FONT_HEADER, FILL_DARK_BLUE, ALIGN_CENTER, THIN_BORDER)

    ws.row_dimensions[header_row].height = 30

    # ── Question rows ────────────────────────────────────────────────────
    # Build tier name lookup
    tier_names = {}
    for tier in rubric["tiers"]:
        tier_names[tier["id"]] = tier["name"]
        # Also map numeric tiers
        if tier["id"].startswith("tier_"):
            tier_num = tier["id"].replace("tier_", "")
            tier_names[int(tier_num)] = tier["name"]
        else:
            tier_names[tier["id"]] = tier["name"]

    # Build criterion name lookup
    crit_names = {}
    for tier in rubric["tiers"]:
        for crit in tier["criteria"]:
            crit_names[crit["id"]] = crit["name"]

    row = header_row + 1
    current_tier = None
    question_rows = []  # Track (row, type, yes_value) for score formulas

    q_key = "question" if mode == "self" else "question_audit"

    for q in questionnaire["questions"]:
        # Tier separator row
        q_tier = q["tier"]
        tier_display = tier_names.get(q_tier, str(q_tier))
        if q_tier != current_tier:
            current_tier = q_tier
            ws.merge_cells(f"A{row}:H{row}")
            c = ws.cell(row=row, column=1, value=f"  {tier_display}")
            style_cell(c, FONT_TIER, FILL_LIGHT_BLUE, Alignment(horizontal="left", vertical="center"))
            for col in range(1, 9):
                ws.cell(row=row, column=col).fill = FILL_LIGHT_BLUE
            ws.row_dimensions[row].height = 30
            row += 1

        # Question row
        qid = q["id"]
        qtype = q["type"]
        criterion = crit_names.get(q["criterion"], q["criterion"])
        question_text = q.get(q_key, q["question"])
        yes_value = q.get("scoring", {}).get("yes_value", 3) if qtype == "checklist" else None

        # Alternate row shading
        row_fill = FILL_WHITE if (row % 2 == 0) else FILL_LIGHT_GRAY

        ws.cell(row=row, column=1, value=qid)
        style_cell(ws.cell(row=row, column=1), FONT_SMALL, row_fill, ALIGN_CENTER, THIN_BORDER)

        ws.cell(row=row, column=2, value=tier_display)
        style_cell(ws.cell(row=row, column=2), FONT_SMALL, row_fill, ALIGN_CENTER, THIN_BORDER)

        ws.cell(row=row, column=3, value=criterion)
        style_cell(ws.cell(row=row, column=3), FONT_SMALL, row_fill, ALIGN_WRAP, THIN_BORDER)

        type_display = {"checklist": "Yes/No", "scale": "Scale 1-5", "text": "Text"}.get(qtype, qtype)
        ws.cell(row=row, column=4, value=type_display)
        style_cell(ws.cell(row=row, column=4), FONT_SMALL, row_fill, ALIGN_CENTER, THIN_BORDER)

        # Question with scale descriptions if applicable
        if qtype == "scale" and "options" in q:
            option_lines = "\n".join(f"  {k} = {v}" for k, v in q["options"].items())
            full_question = f"{question_text}\n{option_lines}"
        else:
            full_question = question_text
        ws.cell(row=row, column=5, value=full_question)
        style_cell(ws.cell(row=row, column=5), FONT_BODY, row_fill, ALIGN_WRAP, THIN_BORDER)

        # Answer column - apply validation
        answer_cell = ws.cell(row=row, column=6)
        style_cell(answer_cell, FONT_BODY, FILL_LIGHTER_BLUE, ALIGN_CENTER, THIN_BORDER)
        if qtype == "checklist":
            dv_yesno.add(answer_cell)
        elif qtype == "scale":
            dv_scale.add(answer_cell)
        else:
            # Text - make answer column wider for this row
            style_cell(answer_cell, FONT_BODY, FILL_LIGHTER_BLUE, ALIGN_WRAP, THIN_BORDER)

        # Score column - auto-calculated formula
        score_cell = ws.cell(row=row, column=7)
        answer_ref = f"F{row}"
        if qtype == "checklist":
            formula = f'=IF({answer_ref}="Yes",{yes_value},IF({answer_ref}="No",1,""))'
            score_cell.value = formula
        elif qtype == "scale":
            formula = f'=IF({answer_ref}="","",{answer_ref})'
            score_cell.value = formula
        else:
            score_cell.value = ""
        style_cell(score_cell, FONT_BODY_BOLD, row_fill, ALIGN_CENTER, THIN_BORDER)
        score_cell.number_format = "0.0"

        # Evidence column
        evidence_cell = ws.cell(row=row, column=8)
        style_cell(evidence_cell, FONT_BODY, FILL_LIGHTER_BLUE, ALIGN_WRAP, THIN_BORDER)

        # Set row height for readability
        if qtype == "scale":
            ws.row_dimensions[row].height = 100
        elif qtype == "text":
            ws.row_dimensions[row].height = 60
        else:
            ws.row_dimensions[row].height = 30

        question_rows.append({
            "row": row,
            "id": qid,
            "type": qtype,
            "criterion": q["criterion"],
            "tier": q_tier,
            "yes_value": yes_value,
        })

        row += 1

    # Apply conditional formatting to score column
    score_range = f"G{header_row + 1}:G{row - 1}"
    apply_conditional_formatting(ws, score_range)

    # Freeze panes
    ws.freeze_panes = f"A{header_row + 1}"

    return ws, question_rows, header_row


# ── Tab 3: Results Dashboard ─────────────────────────────────────────────────


def build_dashboard_tab(wb: Workbook, rubric: dict, questionnaire: dict, question_rows: list, header_row: int):
    ws = wb.create_sheet("Results Dashboard")
    ws.sheet_properties.tabColor = GREEN

    col_widths = {"A": 3, "B": 40, "C": 15, "D": 15, "E": 15, "F": 3, "G": 50, "H": 3}
    for col, width in col_widths.items():
        ws.column_dimensions[col].width = width

    # ── Title ────────────────────────────────────────────────────────────
    ws.merge_cells("A1:H1")
    ws.row_dimensions[1].height = 50
    c = ws["A1"]
    c.value = "  DEBMM Assessment Results"
    style_cell(c, FONT_TITLE, FILL_NAVY, Alignment(horizontal="left", vertical="center"))
    for col in "ABCDEFGH":
        ws[f"{col}1"].fill = FILL_NAVY

    # ── Organization info (linked from Assessment tab) ───────────────────
    info_labels = ["Organization:", "Assessor:", "Date:", "Type:"]
    info_refs = ["Assessment!C3", "Assessment!C4", "Assessment!C6", "Assessment!C7"]
    for i, (label, ref) in enumerate(zip(info_labels, info_refs)):
        r = 3 + i
        ws.cell(row=r, column=2, value=label)
        style_cell(ws.cell(row=r, column=2), FONT_BODY_BOLD, alignment=ALIGN_LEFT)
        ws.cell(row=r, column=3, value=f"={ref}")
        style_cell(ws.cell(row=r, column=3), FONT_BODY, alignment=ALIGN_LEFT)

    # ── Build criterion → question row mapping ───────────────────────────
    crit_to_rows = {}
    for qr in question_rows:
        crit_to_rows.setdefault(qr["criterion"], []).append(qr)

    # Build tier → criterion mapping from rubric
    tier_criteria = []
    for tier in rubric["tiers"]:
        tier_id = tier["id"]
        tier_name = tier["name"]
        for crit in tier["criteria"]:
            tier_criteria.append({
                "tier_id": tier_id,
                "tier_name": tier_name,
                "crit_id": crit["id"],
                "crit_name": crit["name"],
            })

    # ── Overall Score Box ────────────────────────────────────────────────
    row = 8

    ws.merge_cells(f"B{row}:C{row}")
    ws.cell(row=row, column=2, value="Overall Maturity Score")
    style_cell(ws.cell(row=row, column=2), FONT_SUBHEADER, FILL_LIGHT_BLUE, ALIGN_CENTER)
    ws.cell(row=row, column=3).fill = FILL_LIGHT_BLUE

    ws.merge_cells(f"D{row}:E{row}")
    ws.cell(row=row, column=4, value="Achieved Tier")
    style_cell(ws.cell(row=row, column=4), FONT_SUBHEADER, FILL_LIGHT_BLUE, ALIGN_CENTER)
    ws.cell(row=row, column=5).fill = FILL_LIGHT_BLUE

    row += 1
    ws.row_dimensions[row].height = 50

    # Overall score = average of all criterion scores
    # We'll calculate this after placing criterion scores
    overall_score_cell = f"B{row}"
    ws.merge_cells(f"B{row}:C{row}")
    # Placeholder - will be set after we know criterion score cells
    style_cell(ws.cell(row=row, column=2), FONT_SCORE, FILL_WHITE, ALIGN_CENTER, THIN_BORDER)
    ws.cell(row=row, column=3).border = THIN_BORDER

    # Achieved tier cell
    tier_cell_ref = f"D{row}"
    ws.merge_cells(f"D{row}:E{row}")
    style_cell(ws.cell(row=row, column=4), FONT_SCORE_MED, FILL_WHITE, ALIGN_CENTER, THIN_BORDER)
    ws.cell(row=row, column=5).border = THIN_BORDER

    overall_row = row
    row += 2

    # ── Tier / Criterion Breakdown Table ─────────────────────────────────
    ws.cell(row=row, column=2, value="Category / Criterion")
    style_cell(ws.cell(row=row, column=2), FONT_HEADER, FILL_DARK_BLUE, ALIGN_CENTER, THIN_BORDER)
    ws.cell(row=row, column=3, value="Score")
    style_cell(ws.cell(row=row, column=3), FONT_HEADER, FILL_DARK_BLUE, ALIGN_CENTER, THIN_BORDER)
    ws.cell(row=row, column=4, value="Level")
    style_cell(ws.cell(row=row, column=4), FONT_HEADER, FILL_DARK_BLUE, ALIGN_CENTER, THIN_BORDER)
    ws.cell(row=row, column=5, value="Status")
    style_cell(ws.cell(row=row, column=5), FONT_HEADER, FILL_DARK_BLUE, ALIGN_CENTER, THIN_BORDER)

    table_header_row = row
    row += 1

    criterion_score_cells = []
    tier_score_cells = {}
    current_tier_id = None
    tier_crit_score_cells = []

    for tc in tier_criteria:
        # Tier header row
        if tc["tier_id"] != current_tier_id:
            # Close previous tier
            if current_tier_id is not None and tier_crit_score_cells:
                # Insert tier average row
                tier_row = tier_score_cells[current_tier_id]["row"]
                avg_refs = ",".join(tier_crit_score_cells)
                avg_formula = f"=IF(COUNT({avg_refs})=0,\"\",AVERAGE({avg_refs}))"
                ws.cell(row=tier_row, column=3, value=avg_formula)
                ws.cell(row=tier_row, column=3).number_format = "0.00"
                # Level formula
                score_ref = f"C{tier_row}"
                level_formula = (
                    f'=IF({score_ref}="","",IF({score_ref}>=4.5,"Optimized",'
                    f'IF({score_ref}>=3.5,"Managed",IF({score_ref}>=2.5,"Defined",'
                    f'IF({score_ref}>=1.5,"Repeatable","Initial")))))'
                )
                ws.cell(row=tier_row, column=4, value=level_formula)

            current_tier_id = tc["tier_id"]
            tier_crit_score_cells = []

            ws.cell(row=row, column=2, value=tc["tier_name"])
            style_cell(ws.cell(row=row, column=2), FONT_TIER, FILL_LIGHT_BLUE, ALIGN_LEFT, THIN_BORDER)
            style_cell(ws.cell(row=row, column=3), FONT_BODY_BOLD, FILL_LIGHT_BLUE, ALIGN_CENTER, THIN_BORDER)
            style_cell(ws.cell(row=row, column=4), FONT_BODY_BOLD, FILL_LIGHT_BLUE, ALIGN_CENTER, THIN_BORDER)
            style_cell(ws.cell(row=row, column=5), FONT_BODY_BOLD, FILL_LIGHT_BLUE, ALIGN_CENTER, THIN_BORDER)

            tier_score_cells[current_tier_id] = {"row": row, "name": tc["tier_name"]}
            row += 1

        # Criterion row
        crit_id = tc["crit_id"]
        rows_for_crit = crit_to_rows.get(crit_id, [])

        ws.cell(row=row, column=2, value=f"  {tc['crit_name']}")
        style_cell(ws.cell(row=row, column=2), FONT_BODY, FILL_WHITE, ALIGN_LEFT, THIN_BORDER)

        if rows_for_crit:
            # Score formula: average of scored questions for this criterion
            score_refs = [f"Assessment!G{qr['row']}" for qr in rows_for_crit if qr["type"] != "text"]
            if score_refs:
                refs_str = ",".join(score_refs)
                formula = f"=IF(COUNT({refs_str})=0,\"\",AVERAGE({refs_str}))"
                ws.cell(row=row, column=3, value=formula)
            else:
                ws.cell(row=row, column=3, value="")
        else:
            ws.cell(row=row, column=3, value="")

        ws.cell(row=row, column=3).number_format = "0.00"
        style_cell(ws.cell(row=row, column=3), FONT_BODY_BOLD, FILL_WHITE, ALIGN_CENTER, THIN_BORDER)

        # Level name formula
        score_ref = f"C{row}"
        level_formula = (
            f'=IF({score_ref}="","",IF({score_ref}>=4.5,"Optimized",'
            f'IF({score_ref}>=3.5,"Managed",IF({score_ref}>=2.5,"Defined",'
            f'IF({score_ref}>=1.5,"Repeatable","Initial")))))'
        )
        ws.cell(row=row, column=4, value=level_formula)
        style_cell(ws.cell(row=row, column=4), FONT_BODY, FILL_WHITE, ALIGN_CENTER, THIN_BORDER)

        # Status: check/cross based on >= 3.0
        status_formula = f'=IF({score_ref}="","",IF({score_ref}>=3,"Pass","Below Target"))'
        ws.cell(row=row, column=5, value=status_formula)
        style_cell(ws.cell(row=row, column=5), FONT_BODY, FILL_WHITE, ALIGN_CENTER, THIN_BORDER)

        criterion_score_cells.append(f"C{row}")
        tier_crit_score_cells.append(f"C{row}")
        row += 1

    # Close last tier
    if current_tier_id is not None and tier_crit_score_cells:
        tier_row = tier_score_cells[current_tier_id]["row"]
        avg_refs = ",".join(tier_crit_score_cells)
        avg_formula = f"=IF(COUNT({avg_refs})=0,\"\",AVERAGE({avg_refs}))"
        ws.cell(row=tier_row, column=3, value=avg_formula)
        ws.cell(row=tier_row, column=3).number_format = "0.00"
        score_ref = f"C{tier_row}"
        level_formula = (
            f'=IF({score_ref}="","",IF({score_ref}>=4.5,"Optimized",'
            f'IF({score_ref}>=3.5,"Managed",IF({score_ref}>=2.5,"Defined",'
            f'IF({score_ref}>=1.5,"Repeatable","Initial")))))'
        )
        ws.cell(row=tier_row, column=4, value=level_formula)

    # Apply conditional formatting to score column
    score_range = f"C{table_header_row + 1}:C{row - 1}"
    apply_conditional_formatting(ws, score_range)

    # ── Set overall score formula ────────────────────────────────────────
    if criterion_score_cells:
        all_refs = ",".join(criterion_score_cells)
        overall_formula = f"=IF(COUNT({all_refs})=0,\"\",ROUND(AVERAGE({all_refs}),2))"
        ws.cell(row=overall_row, column=2, value=overall_formula)
        ws.cell(row=overall_row, column=2).number_format = "0.00"

    # ── Achieved tier formula ────────────────────────────────────────────
    # Logic: highest tier where ALL criteria in that tier and below are >= 3.0
    # We need to check each core tier (not enrichment)
    core_tiers = ["tier_0", "tier_1", "tier_2", "tier_3", "tier_4"]
    tier_labels = {
        "tier_0": "Tier 0: Foundation",
        "tier_1": "Tier 1: Basic",
        "tier_2": "Tier 2: Intermediate",
        "tier_3": "Tier 3: Advanced",
        "tier_4": "Tier 4: Expert",
    }

    # Build per-tier "all >= 3" check
    tier_check_parts = {}
    for tc_item in tier_criteria:
        tid = tc_item["tier_id"]
        if tid in core_tiers:
            tier_check_parts.setdefault(tid, [])

    # Map criterion cells to tiers
    crit_cell_idx = 0
    current_tier_scan = None
    for tc_item in tier_criteria:
        if tc_item["tier_id"] != current_tier_scan:
            current_tier_scan = tc_item["tier_id"]
        if current_tier_scan in core_tiers:
            if crit_cell_idx < len(criterion_score_cells):
                tier_check_parts.setdefault(current_tier_scan, []).append(
                    criterion_score_cells[crit_cell_idx]
                )
        crit_cell_idx += 1

    # Build nested IF formula for tier determination
    # Check from highest to lowest
    def tier_check_formula(tier_id):
        cells = tier_check_parts.get(tier_id, [])
        if not cells:
            return "TRUE"
        conditions = [f"{c}>=3" for c in cells]
        return f"AND({','.join(conditions)})"

    # Build cumulative check: tier N requires all tiers 0..N to pass
    cumulative_checks = {}
    for i, tid in enumerate(core_tiers):
        checks = []
        for j in range(i + 1):
            checks.append(tier_check_formula(core_tiers[j]))
        cumulative_checks[tid] = f"AND({','.join(checks)})"

    # Nested IF: check from tier 4 down
    tier_formula = f'=IF({cumulative_checks["tier_4"]},"{tier_labels["tier_4"]}",'
    tier_formula += f'IF({cumulative_checks["tier_3"]},"{tier_labels["tier_3"]}",'
    tier_formula += f'IF({cumulative_checks["tier_2"]},"{tier_labels["tier_2"]}",'
    tier_formula += f'IF({cumulative_checks["tier_1"]},"{tier_labels["tier_1"]}",'
    tier_formula += f'IF({cumulative_checks["tier_0"]},"{tier_labels["tier_0"]}",'
    tier_formula += '"Below Foundation")))))'

    ws.cell(row=overall_row, column=4, value=tier_formula)

    # Apply conditional formatting to overall score
    apply_conditional_formatting(ws, f"B{overall_row}:C{overall_row}")

    row += 2

    # ── Bar Chart ────────────────────────────────────────────────────────
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Tier Scores"
    chart.y_axis.title = "Maturity Score (1-5)"
    chart.y_axis.scaling.min = 0
    chart.y_axis.scaling.max = 5
    chart.x_axis.title = "Category"

    # Collect tier score rows
    tier_row_list = [(ts["name"], ts["row"]) for ts in tier_score_cells.values()]
    if tier_row_list:
        # We need to create a reference from the tier score cells
        # Create a small data range for the chart
        chart_start_row = row
        ws.cell(row=row, column=7, value="Category")
        ws.cell(row=row, column=8, value="Score")
        style_cell(ws.cell(row=row, column=7), FONT_HEADER, FILL_DARK_BLUE, ALIGN_CENTER)
        style_cell(ws.cell(row=row, column=8), FONT_HEADER, FILL_DARK_BLUE, ALIGN_CENTER)
        row += 1

        for name, trow in tier_row_list:
            ws.cell(row=row, column=7, value=name)
            ws.cell(row=row, column=8, value=f"=C{trow}")
            ws.cell(row=row, column=8).number_format = "0.00"
            style_cell(ws.cell(row=row, column=7), FONT_BODY, alignment=ALIGN_LEFT)
            style_cell(ws.cell(row=row, column=8), FONT_BODY, alignment=ALIGN_CENTER)
            row += 1

        data = Reference(ws, min_col=8, min_row=chart_start_row, max_row=row - 1)
        cats = Reference(ws, min_col=7, min_row=chart_start_row + 1, max_row=row - 1)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)
        chart.shape = 4
        chart.width = 22
        chart.height = 14

        ws.add_chart(chart, f"B{overall_row + 3}")

    # Freeze panes
    ws.freeze_panes = "A2"

    return ws


# ── Tab 4: Rubric Reference ─────────────────────────────────────────────────


def build_rubric_tab(wb: Workbook, rubric: dict):
    ws = wb.create_sheet("Rubric Reference")
    ws.sheet_properties.tabColor = ORANGE

    col_widths = {"A": 30, "B": 12, "C": 60, "D": 40}
    for col, width in col_widths.items():
        ws.column_dimensions[col].width = width

    # Title
    ws.merge_cells("A1:D1")
    ws.row_dimensions[1].height = 40
    c = ws["A1"]
    c.value = "  DEBMM Rubric Reference"
    style_cell(c, FONT_TITLE, FILL_NAVY, Alignment(horizontal="left", vertical="center"))
    for col in "ABCD":
        ws[f"{col}1"].fill = FILL_NAVY

    row = 3

    for tier in rubric["tiers"]:
        # Tier header
        ws.merge_cells(f"A{row}:D{row}")
        ws.cell(row=row, column=1, value=tier["name"])
        style_cell(ws.cell(row=row, column=1), FONT_TIER, FILL_LIGHT_BLUE, ALIGN_LEFT)
        for col in range(2, 5):
            ws.cell(row=row, column=col).fill = FILL_LIGHT_BLUE
        ws.row_dimensions[row].height = 30

        if tier.get("description"):
            row += 1
            ws.merge_cells(f"A{row}:D{row}")
            ws.cell(row=row, column=1, value=tier["description"].strip())
            style_cell(ws.cell(row=row, column=1), FONT_SMALL, alignment=ALIGN_WRAP)

        row += 1

        for crit in tier["criteria"]:
            # Criterion header
            ws.merge_cells(f"A{row}:D{row}")
            ws.cell(row=row, column=1, value=crit["name"])
            style_cell(ws.cell(row=row, column=1), FONT_BODY_BOLD, FILL_LIGHTER_BLUE, ALIGN_LEFT)
            for col in range(2, 5):
                ws.cell(row=row, column=col).fill = FILL_LIGHTER_BLUE
            row += 1

            # Column headers for levels
            headers = ["Criterion", "Level", "Qualitative Description", "Quantitative Measure"]
            for col_idx, header in enumerate(headers, 1):
                ws.cell(row=row, column=col_idx, value=header)
                style_cell(
                    ws.cell(row=row, column=col_idx),
                    FONT_HEADER, FILL_DARK_BLUE, ALIGN_CENTER, THIN_BORDER,
                )
            row += 1

            level_names = {1: "Initial", 2: "Repeatable", 3: "Defined", 4: "Managed", 5: "Optimized"}
            for level_num in sorted(crit["levels"].keys()):
                level_data = crit["levels"][level_num]
                row_fill = FILL_WHITE if (level_num % 2 == 0) else FILL_LIGHT_GRAY

                ws.cell(row=row, column=1, value=crit["name"] if level_num == 1 else "")
                style_cell(ws.cell(row=row, column=1), FONT_BODY, row_fill, ALIGN_WRAP, THIN_BORDER)

                ws.cell(row=row, column=2, value=f"{level_num} - {level_names[level_num]}")
                style_cell(ws.cell(row=row, column=2), FONT_BODY_BOLD, row_fill, ALIGN_CENTER, THIN_BORDER)

                ws.cell(row=row, column=3, value=level_data["qualitative"].strip())
                style_cell(ws.cell(row=row, column=3), FONT_BODY, row_fill, ALIGN_WRAP, THIN_BORDER)

                ws.cell(row=row, column=4, value=level_data.get("quantitative", "").strip())
                style_cell(ws.cell(row=row, column=4), FONT_BODY, row_fill, ALIGN_WRAP, THIN_BORDER)

                ws.row_dimensions[row].height = 45
                row += 1

            row += 1  # Spacing between criteria

    # Freeze panes
    ws.freeze_panes = "A2"

    return ws


# ── Main ─────────────────────────────────────────────────────────────────────


def generate_spreadsheet(
    output_path: Path,
    rubric_path: Path = DEFAULT_RUBRIC,
    questionnaire_path: Path = DEFAULT_QUESTIONNAIRE,
    mode: str = "self",
):
    rubric = load_yaml(rubric_path)
    questionnaire = load_yaml(questionnaire_path)

    wb = Workbook()

    build_instructions_tab(wb)
    _, question_rows, header_row = build_assessment_tab(wb, questionnaire, rubric, mode)
    build_dashboard_tab(wb, rubric, questionnaire, question_rows, header_row)
    build_rubric_tab(wb, rubric)

    wb.save(output_path)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate DEBMM assessment spreadsheet.")
    parser.add_argument(
        "--output", "-o", type=Path, default=Path("debmm-assessment.xlsx"),
        help="Output Excel file path (default: debmm-assessment.xlsx)",
    )
    parser.add_argument(
        "--mode", choices=["self", "audit"], default="self",
        help="Assessment mode: self-assessment or audit (default: self)",
    )
    parser.add_argument("--rubric", type=Path, default=DEFAULT_RUBRIC)
    parser.add_argument("--questionnaire", type=Path, default=DEFAULT_QUESTIONNAIRE)

    args = parser.parse_args()

    output = generate_spreadsheet(args.output, args.rubric, args.questionnaire, args.mode)
    print(f"Spreadsheet generated: {output}")


if __name__ == "__main__":
    main()
