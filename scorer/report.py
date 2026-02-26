#!/usr/bin/env python3
"""
DEBMM Assessment Report Generator

Generates a markdown report from scored assessment results.
Can be used standalone or imported by score.py and llm_scorer.py.

Usage:
    python report.py <results.json> [--output report.md]
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def generate_report(results: dict, llm_analysis: dict | None = None) -> str:
    """Generate a markdown assessment report from scoring results.

    Args:
        results: Output from score.run_scoring()
        llm_analysis: Optional LLM analysis results to merge in
    """
    meta = results["metadata"]
    org = meta.get("organization", "Unknown Organization")
    assessor = meta.get("assessor_name", "Unknown")
    date = meta.get("date", datetime.now().strftime("%Y-%m-%d"))
    atype = meta.get("assessment_type", "self").title()
    overall = results["overall_score"]
    tier = results["tier_determination"]

    lines = []

    # Header
    lines.append(f"# DEBMM Assessment Report")
    lines.append("")
    lines.append(f"| | |")
    lines.append(f"|---|---|")
    lines.append(f"| **Organization** | {org} |")
    lines.append(f"| **Assessor** | {assessor} |")
    lines.append(f"| **Date** | {date} |")
    lines.append(f"| **Assessment Type** | {atype} |")
    lines.append(f"| **Overall Score** | **{overall}/5.0** |")
    lines.append(f"| **Achieved Tier** | **{tier['tier_name']}** |")
    lines.append("")

    # Executive Summary
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(f"- **Overall Maturity Score**: {overall}/5.0")
    lines.append(f"- **Achieved Tier**: {tier['tier_name']}")
    lines.append(f"- {tier['description']}")
    lines.append(f"- **Questions Scored**: {results['scored_count']}/{results['question_count']}")
    lines.append(f"- **Text Answers Pending Review**: {results['needs_review_count']}")
    if results["issue_count"] > 0:
        lines.append(f"- **Issues (unanswered/invalid)**: {results['issue_count']}")
    lines.append("")

    # Score summary bar
    lines.append("### Maturity Overview")
    lines.append("")
    lines.append("| Category | Score | Level |")
    lines.append("|----------|-------|-------|")
    for tid, tdata in results["tier_scores"].items():
        score_str = f"{tdata['score']}/5.0" if tdata["score"] is not None else "N/A"
        level = _score_to_level(tdata["score"]) if tdata["score"] else "N/A"
        lines.append(f"| {tdata['name']} | {score_str} | {level} |")
    lines.append("")

    # Detailed tier breakdowns
    lines.append("---")
    lines.append("")
    lines.append("## Detailed Results")
    lines.append("")

    for tid, tdata in results["tier_scores"].items():
        score_str = f"{tdata['score']}/5.0" if tdata["score"] is not None else "N/A"
        lines.append(f"### {tdata['name']} - {score_str}")
        lines.append("")
        lines.append("| Criterion | Score | Level | Questions Scored | Pending Review |")
        lines.append("|-----------|-------|-------|-----------------|----------------|")

        for cid, cdata in tdata["criteria"].items():
            c_score = f"{cdata['score']}" if cdata["score"] is not None else "N/A"
            c_level = cdata.get("level_name", "N/A") if cdata["score"] is not None else "N/A"
            c_scored = f"{cdata['scored_count']}/{cdata['total_count']}"
            c_review = f"{cdata['needs_review_count']}" if cdata["needs_review_count"] > 0 else "-"
            lines.append(f"| {cdata['name']} | {c_score} | {c_level} | {c_scored} | {c_review} |")

        lines.append("")

    # Recommendations
    if results["recommendations"]:
        lines.append("---")
        lines.append("")
        lines.append("## Recommendations")
        lines.append("")
        lines.append("The following criteria scored below Defined (3.0) and should be prioritized for improvement:")
        lines.append("")

        high_priority = [r for r in results["recommendations"] if r["priority"] == "high"]
        med_priority = [r for r in results["recommendations"] if r["priority"] == "medium"]

        if high_priority:
            lines.append("### High Priority (Foundation & Basic Tiers)")
            lines.append("")
            for rec in high_priority:
                lines.append(f"- **{rec['criterion']}** ({rec['tier']}): "
                           f"Currently at {rec['current_level']} ({rec['current_score']}/5.0). "
                           f"{rec['recommendation']}")
            lines.append("")

        if med_priority:
            lines.append("### Medium Priority (Intermediate & Above)")
            lines.append("")
            for rec in med_priority:
                lines.append(f"- **{rec['criterion']}** ({rec['tier']}): "
                           f"Currently at {rec['current_level']} ({rec['current_score']}/5.0). "
                           f"{rec['recommendation']}")
            lines.append("")

    # LLM Analysis (if available)
    if llm_analysis:
        lines.append("---")
        lines.append("")
        lines.append("## AI-Assisted Analysis")
        lines.append("")

        if "text_scores" in llm_analysis:
            lines.append("### Text Answer Scores")
            lines.append("")
            lines.append("| Question | Score | Justification |")
            lines.append("|----------|-------|---------------|")
            for ts in llm_analysis["text_scores"]:
                lines.append(f"| {ts['id']} | {ts['score']}/5 | {ts['justification']} |")
            lines.append("")

        if "inconsistencies" in llm_analysis and llm_analysis["inconsistencies"]:
            lines.append("### Identified Inconsistencies")
            lines.append("")
            for inc in llm_analysis["inconsistencies"]:
                lines.append(f"- {inc}")
            lines.append("")

        if "improvement_plan" in llm_analysis:
            lines.append("### Improvement Recommendations")
            lines.append("")
            lines.append(llm_analysis["improvement_plan"])
            lines.append("")

    # Items needing review
    if results["needs_review"]:
        lines.append("---")
        lines.append("")
        lines.append("## Items Requiring Manual Review")
        lines.append("")
        lines.append("The following text answers could not be automatically scored and require human evaluation:")
        lines.append("")

        for item in results["needs_review"]:
            lines.append(f"### {item['id']} ({item['criterion']})")
            lines.append("")
            lines.append(f"> {item['answer']}")
            lines.append("")

    # Issues
    if results["issues"]:
        lines.append("---")
        lines.append("")
        lines.append("## Issues")
        lines.append("")
        for issue in results["issues"]:
            status = issue["status"].replace("_", " ").title()
            error = f" - {issue['error']}" if issue.get("error") else ""
            lines.append(f"- **{issue['id']}**: {status}{error}")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*Generated by [DEBMM Assessment Tool](https://github.com/your-org/debmm-assessment). "
                "Based on [Elastic's DEBMM](https://www.elastic.co/security-labs/elastic-releases-debmm) "
                "with enrichment from [detectionengineering.io](https://detectionengineering.io/).*")
    lines.append("")

    return "\n".join(lines)


def _score_to_level(score: float) -> str:
    """Convert numeric score to level name."""
    if score is None:
        return "N/A"
    level = round(score)
    names = {1: "Initial", 2: "Repeatable", 3: "Defined", 4: "Managed", 5: "Optimized"}
    return names.get(level, "Unknown")


def main():
    parser = argparse.ArgumentParser(description="Generate DEBMM assessment report.")
    parser.add_argument("results", type=Path, help="Path to JSON results from score.py")
    parser.add_argument("--output", "-o", type=Path, default=None, help="Output markdown file")
    parser.add_argument(
        "--llm-results", type=Path, default=None,
        help="Optional LLM analysis JSON to merge into report",
    )

    args = parser.parse_args()

    if not args.results.exists():
        print(f"Error: Results file not found: {args.results}", file=sys.stderr)
        sys.exit(1)

    with open(args.results, "r", encoding="utf-8") as f:
        results = json.load(f)

    llm_analysis = None
    if args.llm_results and args.llm_results.exists():
        with open(args.llm_results, "r", encoding="utf-8") as f:
            llm_analysis = json.load(f)

    report = generate_report(results, llm_analysis)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
