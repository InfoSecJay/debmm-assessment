#!/usr/bin/env python3
"""
DEBMM Assessment Spreadsheet Generator

Generates an all-in-one Excel spreadsheet with:
  - Tab 1: Instructions
  - Tab 2: Assessment (fillable with dropdowns and auto-scoring)
  - Tab 3: Results Dashboard (auto-calculated scores, heatmap, chart)
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

# ── Color palette ─────────────────────────────────────────────────────────────

NAVY = "1B2A4A"
SLATE = "334155"
MED_BLUE = "4472C4"
WHITE = "FFFFFF"
LIGHT_GRAY = "F8FAFC"
HAIRLINE = "E2E8F0"
DARK_TEXT = "1E293B"
MED_TEXT = "475569"
ANSWER_BG = "FFFDE7"
ANSWER_BORDER_COLOR = "F9A825"
SECTION_BG = "EFF6FF"
ACCENT_BORDER = "93C5FD"

GREEN = "70AD47"
LIGHT_GREEN = "D1FAE5"
LIGHT_YELLOW = "FEF9C3"
LIGHT_ORANGE = "FED7AA"
LIGHT_RED = "FEE2E2"

# Level tint fills for rubric tab
LEVEL_TINT_LOW = "FFF1F2"     # Warm rose for levels 1-2
LEVEL_TINT_MID = "FEFCE8"     # Neutral warm for level 3
LEVEL_TINT_HIGH = "F0FDF4"    # Green tint for levels 4-5

# ── Font constants ────────────────────────────────────────────────────────────

FONT_TITLE = Font(name="Calibri", size=18, bold=True, color=WHITE)
FONT_HEADER = Font(name="Calibri", size=11, bold=True, color=WHITE)
FONT_TIER_BANNER = Font(name="Calibri", size=12, bold=True, color=WHITE)
FONT_SECTION = Font(name="Calibri", size=13, bold=True, color=NAVY)
FONT_BODY = Font(name="Calibri", size=11, color=DARK_TEXT)
FONT_BODY_BOLD = Font(name="Calibri", size=11, bold=True, color=DARK_TEXT)
FONT_SMALL = Font(name="Calibri", size=10, color=MED_TEXT)
FONT_OPTION = Font(name="Calibri", size=10, color=MED_TEXT)
FONT_ANSWER = Font(name="Calibri", size=12, bold=True, color=DARK_TEXT)
FONT_SCORE = Font(name="Calibri", size=24, bold=True, color=NAVY)
FONT_SCORE_MED = Font(name="Calibri", size=14, bold=True, color=NAVY)
FONT_SCORE_LABEL = Font(name="Calibri", size=11, bold=True, color=SLATE)
FONT_LEVEL_BOLD = Font(name="Calibri", size=10, bold=True, color=DARK_TEXT)

# ── Fill constants ────────────────────────────────────────────────────────────

FILL_NAVY = PatternFill("solid", fgColor=NAVY)
FILL_SLATE = PatternFill("solid", fgColor=SLATE)
FILL_WHITE = PatternFill("solid", fgColor=WHITE)
FILL_LIGHT_GRAY = PatternFill("solid", fgColor=LIGHT_GRAY)
FILL_SECTION = PatternFill("solid", fgColor=SECTION_BG)
FILL_ANSWER = PatternFill("solid", fgColor=ANSWER_BG)
FILL_GREEN = PatternFill("solid", fgColor=LIGHT_GREEN)
FILL_YELLOW = PatternFill("solid", fgColor=LIGHT_YELLOW)
FILL_ORANGE = PatternFill("solid", fgColor=LIGHT_ORANGE)
FILL_RED = PatternFill("solid", fgColor=LIGHT_RED)
FILL_LEVEL_LOW = PatternFill("solid", fgColor=LEVEL_TINT_LOW)
FILL_LEVEL_MID = PatternFill("solid", fgColor=LEVEL_TINT_MID)
FILL_LEVEL_HIGH = PatternFill("solid", fgColor=LEVEL_TINT_HIGH)

# ── Alignment constants ──────────────────────────────────────────────────────

ALIGN_WRAP = Alignment(horizontal="left", vertical="top", wrap_text=True)
ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
ALIGN_LEFT_TOP = Alignment(horizontal="left", vertical="top", wrap_text=True)

# ── Border constants ──────────────────────────────────────────────────────────

HAIRLINE_BOTTOM = Border(
    bottom=Side(style="thin", color=HAIRLINE),
)
THIN_BORDER = Border(
    left=Side(style="thin", color=HAIRLINE),
    right=Side(style="thin", color=HAIRLINE),
    top=Side(style="thin", color=HAIRLINE),
    bottom=Side(style="thin", color=HAIRLINE),
)
ANSWER_BORDER = Border(
    left=Side(style="thin", color=ANSWER_BORDER_COLOR),
    right=Side(style="thin", color=ANSWER_BORDER_COLOR),
    top=Side(style="thin", color=ANSWER_BORDER_COLOR),
    bottom=Side(style="thin", color=ANSWER_BORDER_COLOR),
)
SECTION_BORDER = Border(
    left=Side(style="medium", color=ACCENT_BORDER),
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


def style_row(ws, row, cols, font=None, fill=None, alignment=None, border=None):
    """Apply styles to a range of columns in a row."""
    for c in range(1, cols + 1):
        style_cell(ws.cell(row=row, column=c), font, fill, alignment, border)


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


# ── Tab 1: Instructions ──────────────────────────────────────────────────────


def build_instructions_tab(wb: Workbook):
    ws = wb.active
    ws.title = "Instructions"
    ws.sheet_properties.tabColor = NAVY

    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 90
    ws.column_dimensions["C"].width = 3

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
            "It covers 21 criteria across 7 categories, with 41 dropdown questions total.",
            "All questions are answered via dropdowns (Yes/No or Scale 1-5). No free-text required.",
        ]),
        ("How to Use", [
            "1.  Fill in your organization details at the top of the Assessment tab",
            "2.  Answer each question using the dropdown menus",
            "3.  For Yes/No questions \u2014 select from the dropdown",
            "4.  For Scale questions (1-5) \u2014 select your maturity rating",
            "5.  Switch to the Results Dashboard tab to see scores calculated automatically",
        ]),
        ("Maturity Levels", [
            "Each criterion is scored on a 1\u20135 scale:",
            "",
            "  1 \u2014 Initial          Minimal or no structured activity",
            "  2 \u2014 Repeatable    Sporadic, inconsistent efforts",
            "  3 \u2014 Defined         Regular, documented processes followed consistently",
            "  4 \u2014 Managed       Comprehensive, well-integrated with measurable outcomes",
            "  5 \u2014 Optimized     Fully automated, continuously improving",
        ]),
        ("DEBMM Tiers", [
            "Tier 0 \u2014 Foundation        Rule development, maintenance, roadmaps, threat modeling",
            "Tier 1 \u2014 Basic                 Baseline rules, version control, telemetry, testing",
            "Tier 2 \u2014 Intermediate     FP reduction, gap analysis, internal validation",
            "Tier 3 \u2014 Advanced           FN triage, external validation, advanced TTP coverage",
            "Tier 4 \u2014 Expert               Threat hunting, automation, AI/LLM integration",
            "",
            "Enrichment \u2014 People & Org       Team structure, training, leadership",
            "Enrichment \u2014 Process & Gov     Lifecycle, metrics, collaboration",
        ]),
        ("Tier Determination", [
            "Your achieved tier is the highest tier where ALL criteria in that tier (and all lower "
            "tiers) score \u2265 3.0 (Defined level). This enforces the progressive nature of the "
            "model \u2014 you need solid foundations before claiming advanced maturity.",
        ]),
        ("Scoring Paths", [
            "1.  This Spreadsheet \u2014 Fill it out and scores calculate automatically in the Dashboard",
            "2.  Python CLI \u2014 Export answers to YAML and run scorer/score.py for a detailed report",
            "3.  LLM-Assisted \u2014 Run scorer/llm_scorer.py for AI-generated improvement recommendations",
        ]),
        ("References", [
            "Elastic DEBMM: https://www.elastic.co/security-labs/elastic-releases-debmm",
            "Detection Engineering Maturity Matrix: https://detectionengineering.io/",
            "MITRE ATT&CK: https://attack.mitre.org/",
        ]),
    ]

    for section_title, lines in instructions:
        # Section title with left accent border
        cell = ws.cell(row=row, column=2, value=section_title)
        style_cell(cell, FONT_SECTION, FILL_SECTION, ALIGN_LEFT, SECTION_BORDER)
        ws.row_dimensions[row].height = 28
        row += 1

        for line in lines:
            cell = ws.cell(row=row, column=2, value=line)
            style_cell(cell, FONT_BODY, alignment=ALIGN_WRAP)
            row += 1

        row += 1  # Spacing between sections

    return ws


# ── Tab 2: Assessment ─────────────────────────────────────────────────────────


def build_assessment_tab(wb: Workbook, questionnaire: dict, rubric: dict, mode: str):
    ws = wb.create_sheet("Assessment")
    ws.sheet_properties.tabColor = MED_BLUE

    # Column widths — leaner layout without Tier and Type columns
    if mode == "audit":
        col_widths = {"A": 8, "B": 28, "C": 80, "D": 14, "E": 10, "F": 45}
        last_col = "F"
        last_col_num = 6
    else:
        col_widths = {"A": 8, "B": 28, "C": 80, "D": 14, "E": 10}
        last_col = "E"
        last_col_num = 5
    for col, width in col_widths.items():
        ws.column_dimensions[col].width = width

    # ── Title banner ────────────────────────────────────────────────────
    ws.merge_cells(f"A1:{last_col}1")
    ws.row_dimensions[1].height = 44
    c = ws["A1"]
    c.value = "  DEBMM Assessment"
    style_cell(c, FONT_TITLE, FILL_NAVY, Alignment(horizontal="left", vertical="center"))
    for i in range(1, last_col_num + 1):
        ws.cell(row=1, column=i).fill = FILL_NAVY

    # ── Metadata section ────────────────────────────────────────────────
    labels = ["Organization:", "Assessor Name:", "Assessor Role:", "Date:", "Assessment Type:"]
    for i, label in enumerate(labels):
        r = 3 + i
        ws.cell(row=r, column=1, value=label)
        style_cell(ws.cell(row=r, column=1), FONT_BODY_BOLD, alignment=ALIGN_LEFT)
        ws.merge_cells(f"B{r}:C{r}")
        style_cell(ws.cell(row=r, column=2), FONT_BODY, FILL_ANSWER, ALIGN_LEFT, ANSWER_BORDER)

    # Pre-fill assessment type
    ws.cell(row=7, column=2, value="Self-Assessment" if mode == "self" else "Audit")

    # Type dropdown
    dv_type = DataValidation(type="list", formula1='"Self-Assessment,Audit"', allow_blank=False)
    dv_type.error = "Please select Self-Assessment or Audit"
    dv_type.errorTitle = "Invalid Entry"
    ws.add_data_validation(dv_type)
    dv_type.add(ws.cell(row=7, column=2))

    # ── Data validations ────────────────────────────────────────────────
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

    # ── Spacer row ──────────────────────────────────────────────────────
    header_row = 9

    # ── Column headers ──────────────────────────────────────────────────
    if mode == "audit":
        headers = ["ID", "Criterion", "Question", "Answer", "Score", "Evidence / Notes"]
    else:
        headers = ["ID", "Criterion", "Question", "Answer", "Score"]
    for col_idx, header in enumerate(headers, 1):
        c = ws.cell(row=header_row, column=col_idx, value=header)
        style_cell(c, FONT_HEADER, FILL_SLATE, ALIGN_CENTER, THIN_BORDER)
    ws.row_dimensions[header_row].height = 28

    # ── Tier / criterion lookups ────────────────────────────────────────
    tier_names = {}
    tier_labels = {}  # For banner display
    for tier in rubric["tiers"]:
        tid = tier["id"]
        tier_names[tid] = tier["name"]
        if tid.startswith("tier_"):
            num = tid.replace("tier_", "")
            tier_names[int(num)] = tier["name"]
            tier_labels[int(num)] = f"TIER {num}: {tier['name'].upper()}"
            tier_labels[tid] = tier_labels[int(num)]
        else:
            # Enrichment tiers
            tier_labels[tid] = tier["name"].upper()

    crit_names = {}
    for tier in rubric["tiers"]:
        for crit in tier["criteria"]:
            crit_names[crit["id"]] = crit["name"]

    # ── Question rows ───────────────────────────────────────────────────
    row = header_row + 1
    current_tier = None
    question_rows = []

    q_key = "question" if mode == "self" else "question_audit"

    for q in questionnaire["questions"]:
        q_tier = q["tier"]

        # Tier separator — navy banner
        if q_tier != current_tier:
            current_tier = q_tier
            banner_text = tier_labels.get(q_tier, str(q_tier).upper())
            ws.merge_cells(f"A{row}:{last_col}{row}")
            c = ws.cell(row=row, column=1, value=f"  {banner_text}")
            style_cell(c, FONT_TIER_BANNER, FILL_NAVY,
                        Alignment(horizontal="left", vertical="center"))
            for col in range(1, last_col_num + 1):
                ws.cell(row=row, column=col).fill = FILL_NAVY
            ws.row_dimensions[row].height = 36
            row += 1

        # Question data
        qid = q["id"]
        qtype = q["type"]
        criterion = crit_names.get(q["criterion"], q["criterion"])
        question_text = q.get(q_key, q["question"])
        yes_value = q.get("scoring", {}).get("yes_value", 3) if qtype == "checklist" else None

        # Column A — ID
        ws.cell(row=row, column=1, value=qid)
        style_cell(ws.cell(row=row, column=1), FONT_SMALL, FILL_WHITE, ALIGN_CENTER, HAIRLINE_BOTTOM)

        # Column B — Criterion
        ws.cell(row=row, column=2, value=criterion)
        style_cell(ws.cell(row=row, column=2), FONT_SMALL, FILL_WHITE, ALIGN_LEFT_TOP, HAIRLINE_BOTTOM)

        # Column C — Question (with scale options formatted cleanly)
        if qtype == "scale" and "options" in q:
            option_lines = "\n".join(f"{k} \u2014 {v}" for k, v in q["options"].items())
            full_question = f"{question_text}\n\n{option_lines}"
        else:
            full_question = question_text
        ws.cell(row=row, column=3, value=full_question)
        style_cell(ws.cell(row=row, column=3), FONT_BODY, FILL_WHITE, ALIGN_LEFT_TOP, HAIRLINE_BOTTOM)

        # Column D — Answer (warm cream fill, the interactive column)
        answer_cell = ws.cell(row=row, column=4)
        style_cell(answer_cell, FONT_ANSWER, FILL_ANSWER, ALIGN_CENTER, ANSWER_BORDER)
        if qtype == "checklist":
            dv_yesno.add(answer_cell)
        elif qtype == "scale":
            dv_scale.add(answer_cell)

        # Column E — Score (auto-calculated)
        score_cell = ws.cell(row=row, column=5)
        answer_ref = f"D{row}"
        if qtype == "checklist":
            score_cell.value = f'=IF({answer_ref}="Yes",{yes_value},IF({answer_ref}="No",1,""))'
        elif qtype == "scale":
            score_cell.value = f'=IF({answer_ref}="","",{answer_ref})'
        style_cell(score_cell, FONT_BODY_BOLD, FILL_WHITE, ALIGN_CENTER, HAIRLINE_BOTTOM)
        score_cell.number_format = "0.0"

        # Column F — Evidence (audit only)
        if mode == "audit":
            evidence_cell = ws.cell(row=row, column=6)
            style_cell(evidence_cell, FONT_BODY, FILL_ANSWER, ALIGN_LEFT_TOP, ANSWER_BORDER)

        # Row height
        if qtype == "scale":
            ws.row_dimensions[row].height = 115
        else:
            ws.row_dimensions[row].height = 35

        question_rows.append({
            "row": row,
            "id": qid,
            "type": qtype,
            "criterion": q["criterion"],
            "tier": q_tier,
            "yes_value": yes_value,
        })
        row += 1

    # Conditional formatting on score column
    apply_conditional_formatting(ws, f"E{header_row + 1}:E{row - 1}")

    # Freeze panes below headers
    ws.freeze_panes = f"A{header_row + 1}"

    return ws, question_rows, header_row


# ── Tab 3: Results Dashboard ──────────────────────────────────────────────────


def build_dashboard_tab(wb: Workbook, rubric: dict, questionnaire: dict, question_rows: list, header_row: int):
    ws = wb.create_sheet("Results Dashboard")
    ws.sheet_properties.tabColor = GREEN

    col_widths = {"A": 3, "B": 40, "C": 15, "D": 15, "E": 15, "F": 3}
    for col, width in col_widths.items():
        ws.column_dimensions[col].width = width
    # Hidden chart data columns
    ws.column_dimensions["M"].width = 18
    ws.column_dimensions["N"].width = 10

    # ── Title ──────────────────────────────────────────────────────────
    ws.merge_cells("A1:F1")
    ws.row_dimensions[1].height = 50
    c = ws["A1"]
    c.value = "  DEBMM Assessment Results"
    style_cell(c, FONT_TITLE, FILL_NAVY, Alignment(horizontal="left", vertical="center"))
    for col in "ABCDEF":
        ws[f"{col}1"].fill = FILL_NAVY

    # ── Organization info ──────────────────────────────────────────────
    info_labels = ["Organization:", "Assessor:", "Date:", "Type:"]
    info_refs = ["Assessment!B3", "Assessment!B4", "Assessment!B6", "Assessment!B7"]
    for i, (label, ref) in enumerate(zip(info_labels, info_refs)):
        r = 3 + i
        ws.cell(row=r, column=2, value=label)
        style_cell(ws.cell(row=r, column=2), FONT_BODY_BOLD, alignment=ALIGN_LEFT)
        ws.cell(row=r, column=3, value=f"={ref}")
        style_cell(ws.cell(row=r, column=3), FONT_BODY, alignment=ALIGN_LEFT)

    # ── Completion indicator ───────────────────────────────────────────
    total_q = len(question_rows)
    # Count non-empty answers
    answer_cells = [f"Assessment!D{qr['row']}" for qr in question_rows]
    count_formula = "+".join(f'IF({ac}<>"",1,0)' for ac in answer_cells)
    ws.cell(row=7, column=2, value="Questions Answered:")
    style_cell(ws.cell(row=7, column=2), FONT_BODY_BOLD, alignment=ALIGN_LEFT)
    ws.cell(row=7, column=3, value=f"={{{count_formula}}}")
    # Use a simpler COUNTA approach
    ws.cell(row=7, column=3, value=f'=COUNTA(Assessment!D{question_rows[0]["row"]}:D{question_rows[-1]["row"]})&" / {total_q}"')
    style_cell(ws.cell(row=7, column=3), FONT_BODY, alignment=ALIGN_LEFT)

    # ── Build mappings ─────────────────────────────────────────────────
    crit_to_rows = {}
    for qr in question_rows:
        crit_to_rows.setdefault(qr["criterion"], []).append(qr)

    tier_criteria = []
    for tier in rubric["tiers"]:
        for crit in tier["criteria"]:
            tier_criteria.append({
                "tier_id": tier["id"],
                "tier_name": tier["name"],
                "crit_id": crit["id"],
                "crit_name": crit["name"],
            })

    # ── Score cards ────────────────────────────────────────────────────
    row = 9

    # Overall score label
    ws.merge_cells(f"B{row}:C{row}")
    ws.cell(row=row, column=2, value="Overall Maturity Score")
    style_cell(ws.cell(row=row, column=2), FONT_SCORE_LABEL, FILL_SECTION, ALIGN_CENTER, THIN_BORDER)
    ws.cell(row=row, column=3).fill = FILL_SECTION
    ws.cell(row=row, column=3).border = THIN_BORDER

    # Achieved tier label
    ws.merge_cells(f"D{row}:E{row}")
    ws.cell(row=row, column=4, value="Achieved Tier")
    style_cell(ws.cell(row=row, column=4), FONT_SCORE_LABEL, FILL_SECTION, ALIGN_CENTER, THIN_BORDER)
    ws.cell(row=row, column=5).fill = FILL_SECTION
    ws.cell(row=row, column=5).border = THIN_BORDER

    row += 1
    ws.row_dimensions[row].height = 55

    # Overall score value cell
    ws.merge_cells(f"B{row}:C{row}")
    style_cell(ws.cell(row=row, column=2), FONT_SCORE, FILL_WHITE, ALIGN_CENTER, THIN_BORDER)
    ws.cell(row=row, column=3).border = THIN_BORDER

    # Achieved tier value cell
    ws.merge_cells(f"D{row}:E{row}")
    style_cell(ws.cell(row=row, column=4), FONT_SCORE_MED, FILL_WHITE, ALIGN_CENTER, THIN_BORDER)
    ws.cell(row=row, column=5).border = THIN_BORDER

    overall_row = row
    row += 2

    # ── Breakdown table ────────────────────────────────────────────────
    for col_idx, header in enumerate(["Category / Criterion", "Score", "Level", "Status"], 2):
        c = ws.cell(row=row, column=col_idx, value=header)
        style_cell(c, FONT_HEADER, FILL_SLATE, ALIGN_CENTER, THIN_BORDER)
    table_header_row = row
    row += 1

    criterion_score_cells = []
    tier_score_cells = {}
    current_tier_id = None
    tier_crit_score_cells = []

    for tc in tier_criteria:
        if tc["tier_id"] != current_tier_id:
            # Finalize previous tier's average
            if current_tier_id is not None and tier_crit_score_cells:
                _finalize_tier_row(ws, tier_score_cells[current_tier_id]["row"], tier_crit_score_cells)

            current_tier_id = tc["tier_id"]
            tier_crit_score_cells = []

            # Tier header row
            ws.cell(row=row, column=2, value=tc["tier_name"])
            style_cell(ws.cell(row=row, column=2), FONT_BODY_BOLD, FILL_SECTION, ALIGN_LEFT, THIN_BORDER)
            for col in range(3, 6):
                style_cell(ws.cell(row=row, column=col), FONT_BODY_BOLD, FILL_SECTION, ALIGN_CENTER, THIN_BORDER)
            tier_score_cells[current_tier_id] = {"row": row, "name": tc["tier_name"]}
            row += 1

        # Criterion row
        crit_id = tc["crit_id"]
        rows_for_crit = crit_to_rows.get(crit_id, [])

        ws.cell(row=row, column=2, value=f"    {tc['crit_name']}")
        style_cell(ws.cell(row=row, column=2), FONT_BODY, FILL_WHITE, ALIGN_LEFT, HAIRLINE_BOTTOM)

        if rows_for_crit:
            score_refs = [f"Assessment!E{qr['row']}" for qr in rows_for_crit]
            if score_refs:
                refs_str = ",".join(score_refs)
                ws.cell(row=row, column=3, value=f'=IF(COUNT({refs_str})=0,"",AVERAGE({refs_str}))')
        ws.cell(row=row, column=3).number_format = "0.00"
        style_cell(ws.cell(row=row, column=3), FONT_BODY_BOLD, FILL_WHITE, ALIGN_CENTER, HAIRLINE_BOTTOM)

        # Level name
        score_ref = f"C{row}"
        level_formula = (
            f'=IF({score_ref}="","",IF({score_ref}>=4.5,"Optimized",'
            f'IF({score_ref}>=3.5,"Managed",IF({score_ref}>=2.5,"Defined",'
            f'IF({score_ref}>=1.5,"Repeatable","Initial")))))'
        )
        ws.cell(row=row, column=4, value=level_formula)
        style_cell(ws.cell(row=row, column=4), FONT_BODY, FILL_WHITE, ALIGN_CENTER, HAIRLINE_BOTTOM)

        # Status with conditional formatting
        status_formula = f'=IF({score_ref}="","",IF({score_ref}>=3,"\u2713 Pass","\u2717 Below Target"))'
        ws.cell(row=row, column=5, value=status_formula)
        style_cell(ws.cell(row=row, column=5), FONT_BODY, FILL_WHITE, ALIGN_CENTER, HAIRLINE_BOTTOM)

        criterion_score_cells.append(f"C{row}")
        tier_crit_score_cells.append(f"C{row}")
        row += 1

    # Finalize last tier
    if current_tier_id is not None and tier_crit_score_cells:
        _finalize_tier_row(ws, tier_score_cells[current_tier_id]["row"], tier_crit_score_cells)

    # Conditional formatting on score column and status column
    apply_conditional_formatting(ws, f"C{table_header_row + 1}:C{row - 1}")
    # Green for Pass, Red for Below Target
    ws.conditional_formatting.add(
        f"E{table_header_row + 1}:E{row - 1}",
        CellIsRule(operator="equal", formula=['"✓ Pass"'], fill=FILL_GREEN),
    )
    ws.conditional_formatting.add(
        f"E{table_header_row + 1}:E{row - 1}",
        CellIsRule(operator="equal", formula=['"✗ Below Target"'], fill=FILL_RED),
    )

    # ── Overall score formula ──────────────────────────────────────────
    if criterion_score_cells:
        all_refs = ",".join(criterion_score_cells)
        ws.cell(row=overall_row, column=2, value=f'=IF(COUNT({all_refs})=0,"",ROUND(AVERAGE({all_refs}),2)&" / 5.0")')
        ws.cell(row=overall_row, column=2).number_format = "@"

    # ── Achieved tier formula ──────────────────────────────────────────
    core_tiers = ["tier_0", "tier_1", "tier_2", "tier_3", "tier_4"]
    tier_display_labels = {
        "tier_0": "Tier 0: Foundation",
        "tier_1": "Tier 1: Basic",
        "tier_2": "Tier 2: Intermediate",
        "tier_3": "Tier 3: Advanced",
        "tier_4": "Tier 4: Expert",
    }

    tier_check_parts = {tid: [] for tid in core_tiers}
    crit_cell_idx = 0
    current_tier_scan = None
    for tc_item in tier_criteria:
        if tc_item["tier_id"] != current_tier_scan:
            current_tier_scan = tc_item["tier_id"]
        if current_tier_scan in core_tiers and crit_cell_idx < len(criterion_score_cells):
            tier_check_parts[current_tier_scan].append(criterion_score_cells[crit_cell_idx])
        crit_cell_idx += 1

    def tier_check_formula(tier_id):
        cells = tier_check_parts.get(tier_id, [])
        if not cells:
            return "TRUE"
        return f"AND({','.join(f'{c}>=3' for c in cells)})"

    cumulative_checks = {}
    for i, tid in enumerate(core_tiers):
        checks = [tier_check_formula(core_tiers[j]) for j in range(i + 1)]
        cumulative_checks[tid] = f"AND({','.join(checks)})"

    tier_formula = f'=IF({cumulative_checks["tier_4"]},"{tier_display_labels["tier_4"]}",'
    tier_formula += f'IF({cumulative_checks["tier_3"]},"{tier_display_labels["tier_3"]}",'
    tier_formula += f'IF({cumulative_checks["tier_2"]},"{tier_display_labels["tier_2"]}",'
    tier_formula += f'IF({cumulative_checks["tier_1"]},"{tier_display_labels["tier_1"]}",'
    tier_formula += f'IF({cumulative_checks["tier_0"]},"{tier_display_labels["tier_0"]}",'
    tier_formula += '"Below Foundation")))))'
    ws.cell(row=overall_row, column=4, value=tier_formula)

    # Conditional formatting on overall score area
    apply_conditional_formatting(ws, f"B{overall_row}:C{overall_row}")

    # ── Bar Chart (data in hidden columns M-N) ─────────────────────────
    chart_data_row = 2
    tier_row_list = [(ts["name"], ts["row"]) for ts in tier_score_cells.values()]
    if tier_row_list:
        ws.cell(row=chart_data_row, column=13, value="Category")
        ws.cell(row=chart_data_row, column=14, value="Score")
        chart_data_row += 1
        for name, trow in tier_row_list:
            ws.cell(row=chart_data_row, column=13, value=name)
            ws.cell(row=chart_data_row, column=14, value=f"=C{trow}")
            ws.cell(row=chart_data_row, column=14).number_format = "0.00"
            chart_data_row += 1

        chart = BarChart()
        chart.type = "col"
        chart.style = 10
        chart.title = "Maturity by Category"
        chart.y_axis.title = "Score (1\u20145)"
        chart.y_axis.scaling.min = 0
        chart.y_axis.scaling.max = 5
        chart.x_axis.title = None
        chart.legend = None
        data = Reference(ws, min_col=14, min_row=2, max_row=chart_data_row - 1)
        cats = Reference(ws, min_col=13, min_row=3, max_row=chart_data_row - 1)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)
        chart.width = 22
        chart.height = 14
        ws.add_chart(chart, f"B{overall_row + 3}")

    ws.freeze_panes = "A2"
    return ws


def _finalize_tier_row(ws, tier_row, crit_score_cells):
    """Insert average formula and level formula into a tier header row."""
    avg_refs = ",".join(crit_score_cells)
    ws.cell(row=tier_row, column=3, value=f'=IF(COUNT({avg_refs})=0,"",AVERAGE({avg_refs}))')
    ws.cell(row=tier_row, column=3).number_format = "0.00"
    score_ref = f"C{tier_row}"
    level_formula = (
        f'=IF({score_ref}="","",IF({score_ref}>=4.5,"Optimized",'
        f'IF({score_ref}>=3.5,"Managed",IF({score_ref}>=2.5,"Defined",'
        f'IF({score_ref}>=1.5,"Repeatable","Initial")))))'
    )
    ws.cell(row=tier_row, column=4, value=level_formula)


# ── Tab 4: Rubric Reference ──────────────────────────────────────────────────


def build_rubric_tab(wb: Workbook, rubric: dict):
    ws = wb.create_sheet("Rubric Reference")
    ws.sheet_properties.tabColor = "ED7D31"

    col_widths = {"A": 14, "B": 65, "C": 45}
    for col, width in col_widths.items():
        ws.column_dimensions[col].width = width

    # Title
    ws.merge_cells("A1:C1")
    ws.row_dimensions[1].height = 44
    c = ws["A1"]
    c.value = "  DEBMM Rubric Reference"
    style_cell(c, FONT_TITLE, FILL_NAVY, Alignment(horizontal="left", vertical="center"))
    for col in "ABC":
        ws[f"{col}1"].fill = FILL_NAVY

    row = 3
    level_names = {1: "Initial", 2: "Repeatable", 3: "Defined", 4: "Managed", 5: "Optimized"}

    for tier in rubric["tiers"]:
        # Tier header
        ws.merge_cells(f"A{row}:C{row}")
        ws.cell(row=row, column=1, value=tier["name"])
        style_cell(ws.cell(row=row, column=1), FONT_TIER_BANNER, FILL_NAVY,
                    Alignment(horizontal="left", vertical="center"))
        for col in range(2, 4):
            ws.cell(row=row, column=col).fill = FILL_NAVY
        ws.row_dimensions[row].height = 32

        if tier.get("description"):
            row += 1
            ws.merge_cells(f"A{row}:C{row}")
            ws.cell(row=row, column=1, value=tier["description"].strip())
            style_cell(ws.cell(row=row, column=1), FONT_SMALL, alignment=ALIGN_WRAP)
            ws.row_dimensions[row].height = 28
        row += 1

        for crit in tier["criteria"]:
            # Criterion name header
            ws.merge_cells(f"A{row}:C{row}")
            ws.cell(row=row, column=1, value=crit["name"])
            style_cell(ws.cell(row=row, column=1), FONT_BODY_BOLD, FILL_SECTION, ALIGN_LEFT, SECTION_BORDER)
            for col in range(2, 4):
                ws.cell(row=row, column=col).fill = FILL_SECTION
            ws.row_dimensions[row].height = 26
            row += 1

            # Column sub-headers
            for col_idx, header in enumerate(["Level", "Description", "Quantitative Measure"], 1):
                ws.cell(row=row, column=col_idx, value=header)
                style_cell(ws.cell(row=row, column=col_idx), FONT_HEADER, FILL_SLATE, ALIGN_CENTER, THIN_BORDER)
            ws.row_dimensions[row].height = 22
            row += 1

            for level_num in sorted(crit["levels"].keys()):
                level_data = crit["levels"][level_num]

                # Color-code by level
                if level_num <= 2:
                    row_fill = FILL_LEVEL_LOW
                elif level_num == 3:
                    row_fill = FILL_LEVEL_MID
                else:
                    row_fill = FILL_LEVEL_HIGH

                ws.cell(row=row, column=1, value=f"{level_num} \u2014 {level_names[level_num]}")
                style_cell(ws.cell(row=row, column=1), FONT_LEVEL_BOLD, row_fill, ALIGN_CENTER, THIN_BORDER)

                ws.cell(row=row, column=2, value=level_data["qualitative"].strip())
                style_cell(ws.cell(row=row, column=2), FONT_BODY, row_fill, ALIGN_WRAP, THIN_BORDER)

                ws.cell(row=row, column=3, value=level_data.get("quantitative", "").strip())
                style_cell(ws.cell(row=row, column=3), FONT_BODY, row_fill, ALIGN_WRAP, THIN_BORDER)

                ws.row_dimensions[row].height = 42
                row += 1

            row += 1  # Space between criteria

    ws.freeze_panes = "A2"
    return ws


# ── Main ──────────────────────────────────────────────────────────────────────


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
        "--output", "-o", type=Path,
        default=PROJECT_ROOT / "templates" / "debmm-assessment.xlsx",
        help="Output Excel file path (default: templates/debmm-assessment.xlsx)",
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
