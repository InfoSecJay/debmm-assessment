"""Extract DEBMM assessment data from a completed .xlsx into JSON for report generation.

Usage:
    python scorer/extract_data.py <assessment.xlsx> [-o output.json]

The spreadsheet MUST be opened and saved in Excel first so that formulas are evaluated.
Reads the Report Data tab (designed for machine consumption).
"""

import argparse
import json
import sys
from pathlib import Path

import openpyxl


def _to_float(value):
    """Safely convert a cell value to float."""
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _to_str(value, default=""):
    """Safely convert a cell value to string."""
    if value is None:
        return default
    return str(value).strip()


def extract_report_data(xlsx_path: Path) -> dict:
    """Read the Report Data tab and return structured dict matching generate_debmm.js schema."""
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)

    if "Report Data" not in wb.sheetnames:
        print(f"Error: No 'Report Data' tab found in {xlsx_path}", file=sys.stderr)
        print(f"Available sheets: {wb.sheetnames}", file=sys.stderr)
        sys.exit(1)

    ws = wb["Report Data"]

    # ── Table 1: Summary (rows 2-8, columns A-B) ──
    summary = {}
    for row in range(2, 9):
        label = _to_str(ws.cell(row=row, column=1).value)
        value = ws.cell(row=row, column=2).value
        summary[label] = value

    org = _to_str(summary.get("Organization"))
    assessor = _to_str(summary.get("Assessor"))
    date_val = summary.get("Date")
    if hasattr(date_val, "strftime"):
        date_str = date_val.strftime("%Y-%m-%d")
    else:
        date_str = _to_str(date_val, "N/A")
    assess_type = _to_str(summary.get("Assessment Type", "Self-Assessment"))

    overall_raw = summary.get("Overall Score")
    overall_score = _to_float(overall_raw)
    if overall_score is None and isinstance(overall_raw, str):
        # Handle "3.04 / 5.0" format from Dashboard
        try:
            overall_score = float(overall_raw.split("/")[0].strip())
        except (ValueError, IndexError):
            overall_score = 0.0

    achieved_tier = _to_str(summary.get("Achieved Tier", "N/A"))
    completion = _to_str(summary.get("Completion", "0 / 0"))

    # ── Table 2: Tier Progression (row 10 = header, rows 11-15 = data) ──
    tiers = []
    for row in range(11, 16):
        tier_id = _to_str(ws.cell(row=row, column=1).value)
        if not tier_id:
            break
        tier_name = _to_str(ws.cell(row=row, column=2).value)
        score = _to_float(ws.cell(row=row, column=3).value)
        level = _to_str(ws.cell(row=row, column=4).value, "N/A")
        status = _to_str(ws.cell(row=row, column=5).value, "N/A")
        progression = _to_str(ws.cell(row=row, column=6).value, "Not Started")

        tiers.append({
            "id": tier_id,
            "name": tier_name,
            "score": score if score is not None else 0.0,
            "level": level,
            "status": status,
            "progression": progression,
        })

    # ── Table 3: Criterion Breakdown (row 17 = header, rows 18+ = data) ──
    criteria = []
    row = 18
    while True:
        section = _to_str(ws.cell(row=row, column=1).value)
        if not section:
            break
        category = _to_str(ws.cell(row=row, column=2).value)
        criterion = _to_str(ws.cell(row=row, column=3).value)
        score = _to_float(ws.cell(row=row, column=4).value)
        level = _to_str(ws.cell(row=row, column=5).value, "N/A")
        status = _to_str(ws.cell(row=row, column=6).value, "N/A")

        criteria.append({
            "section": section,
            "category": category,
            "criterion": criterion,
            "score": score if score is not None else 0.0,
            "level": level,
            "status": status,
        })
        row += 1

    return {
        "org": org,
        "assessor": assessor,
        "date": date_str,
        "type": assess_type,
        "overallScore": overall_score if overall_score is not None else 0.0,
        "achievedTier": achieved_tier,
        "completion": completion,
        "tiers": tiers,
        "criteria": criteria,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Extract DEBMM assessment data from xlsx to JSON."
    )
    parser.add_argument("xlsx", type=Path, help="Path to completed assessment .xlsx")
    parser.add_argument(
        "-o", "--output", type=Path, default=None,
        help="Output JSON path (default: <input>_data.json)",
    )
    args = parser.parse_args()

    if not args.xlsx.exists():
        print(f"Error: File not found: {args.xlsx}", file=sys.stderr)
        sys.exit(1)

    data = extract_report_data(args.xlsx)

    output = args.output or args.xlsx.with_suffix("").with_name(
        args.xlsx.stem + "_data.json"
    )
    output.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Data extracted: {output}")
    print(f"  Organization: {data['org'] or 'N/A'}")
    print(f"  Overall Score: {data['overallScore']}")
    print(f"  Achieved Tier: {data['achievedTier']}")
    print(f"  Tiers: {len(data['tiers'])}, Criteria: {len(data['criteria'])}")


if __name__ == "__main__":
    main()
