#!/usr/bin/env python3
"""
DEBMM LLM-Assisted Scorer

Extends the automated scorer by using an LLM to:
1. Score text/written answers on the 1-5 maturity scale
2. Identify inconsistencies between answers
3. Generate improvement recommendations

Supports OpenAI and Anthropic APIs.

Usage:
    python llm_scorer.py <response.yaml> --provider anthropic --model claude-sonnet-4-6
    python llm_scorer.py <response.yaml> --provider openai --model gpt-4o
    python llm_scorer.py <response.yaml> --dry-run  # Show prompt without calling API

Environment variables:
    OPENAI_API_KEY    - Required for --provider openai
    ANTHROPIC_API_KEY - Required for --provider anthropic
"""

import argparse
import json
import os
import sys
from pathlib import Path

import yaml

from score import run_scoring, DEFAULT_RUBRIC, DEFAULT_QUESTIONNAIRE
from report import generate_report

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent


def load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_rubric_context(rubric_path: Path) -> str:
    """Build a concise rubric summary for the LLM prompt."""
    rubric = load_yaml(rubric_path)
    lines = ["# DEBMM Rubric Summary", ""]
    lines.append("Maturity Levels: 1=Initial, 2=Repeatable, 3=Defined, 4=Managed, 5=Optimized")
    lines.append("")

    for tier in rubric["tiers"]:
        lines.append(f"## {tier['name']}")
        for crit in tier["criteria"]:
            lines.append(f"### {crit['name']} (id: {crit['id']})")
            for level_num, level_data in crit["levels"].items():
                lines.append(f"  Level {level_num}: {level_data['qualitative'].strip()}")
        lines.append("")

    return "\n".join(lines)


def build_analysis_prompt(
    results: dict,
    rubric_context: str,
    questionnaire: dict,
) -> str:
    """Build the prompt for LLM analysis."""
    q_index = {q["id"]: q for q in questionnaire["questions"]}

    # Collect text answers and their context
    text_items = []
    for item in results["needs_review"]:
        q_def = q_index.get(item["id"], {})
        text_items.append({
            "id": item["id"],
            "criterion": item["criterion"],
            "question": q_def.get("question", "Unknown question"),
            "answer": item["answer"],
        })

    # Collect all scored items for inconsistency checking
    scored_summary = {}
    for tid, tdata in results["tier_scores"].items():
        for cid, cdata in tdata["criteria"].items():
            scored_summary[cid] = {
                "name": cdata["name"],
                "score": cdata["score"],
                "level": cdata.get("level_name", "N/A"),
            }

    prompt = f"""You are an expert detection engineering assessor evaluating an organization's maturity using the DEBMM (Detection Engineering Behavior Maturity Model).

{rubric_context}

## Current Automated Scores

The following scores were calculated from checklist and scale answers:

"""
    for cid, cdata in scored_summary.items():
        if cdata["score"] is not None:
            prompt += f"- {cdata['name']}: {cdata['score']}/5.0 ({cdata['level']})\n"

    prompt += f"""
## Text Answers to Score

The following text answers need to be scored on the 1-5 maturity scale. For each answer, assess the maturity level described and provide a brief justification.

"""
    for item in text_items:
        prompt += f"""### {item['id']} - {item['criterion']}
**Question**: {item['question']}
**Answer**: {item['answer']}

"""

    prompt += """## Your Task

Respond with a JSON object containing exactly these fields:

1. "text_scores": Array of objects, one per text answer above, each with:
   - "id": The question ID (e.g., "T0-Q10")
   - "criterion": The criterion ID
   - "score": Integer 1-5 based on the rubric levels
   - "justification": 1-2 sentence explanation of why this score

2. "inconsistencies": Array of strings describing any inconsistencies between the checklist/scale answers and the text answers. For example, if someone rates themselves as "Defined" on a scale question but their text answer describes Initial-level practices. Empty array if none found.

3. "improvement_plan": A markdown-formatted improvement plan with specific, actionable recommendations organized by priority. Focus on the lowest-scoring areas first, especially in foundational tiers. Include concrete next steps the team can take.

Respond ONLY with the JSON object, no other text."""

    return prompt


def call_openai(prompt: str, model: str) -> dict:
    """Call OpenAI API."""
    try:
        from openai import OpenAI
    except ImportError:
        print("Error: openai package not installed. Run: pip install openai", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    return json.loads(response.choices[0].message.content)


def call_anthropic(prompt: str, model: str) -> dict:
    """Call Anthropic API."""
    try:
        from anthropic import Anthropic
    except ImportError:
        print("Error: anthropic package not installed. Run: pip install anthropic", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )

    # Extract JSON from response
    text = response.content[0].text
    # Handle case where model wraps JSON in markdown code block
    if text.strip().startswith("```"):
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]

    return json.loads(text.strip())


def merge_llm_scores(results: dict, llm_analysis: dict, questionnaire: dict) -> dict:
    """Merge LLM text scores back into the main results."""
    q_index = {q["id"]: q for q in questionnaire["questions"]}

    if "text_scores" not in llm_analysis:
        return results

    # Build a map of LLM scores by criterion
    llm_by_criterion = {}
    for ts in llm_analysis["text_scores"]:
        crit = ts.get("criterion") or q_index.get(ts["id"], {}).get("criterion")
        if crit:
            llm_by_criterion.setdefault(crit, []).append(ts["score"])

    # Recalculate criterion scores including LLM text scores
    for tid, tdata in results["tier_scores"].items():
        for cid, cdata in tdata["criteria"].items():
            if cid in llm_by_criterion:
                # Get existing scored values
                existing_scores = []
                for q in cdata.get("questions", []):
                    if q.get("score") is not None:
                        existing_scores.append(q["score"])

                # Add LLM scores
                all_scores = existing_scores + llm_by_criterion[cid]
                new_avg = round(sum(all_scores) / len(all_scores), 2)
                new_level = round(new_avg)
                level_names = {
                    1: "Initial", 2: "Repeatable", 3: "Defined",
                    4: "Managed", 5: "Optimized",
                }

                cdata["score"] = new_avg
                cdata["level"] = new_level
                cdata["level_name"] = level_names.get(new_level, "Unknown")
                cdata["includes_llm_scores"] = True

        # Recalculate tier average
        tier_scores = [
            c["score"] * c.get("weight", 1.0)
            for c in tdata["criteria"].values()
            if c["score"] is not None
        ]
        tier_weights = sum(
            c.get("weight", 1.0)
            for c in tdata["criteria"].values()
            if c["score"] is not None
        )
        tdata["score"] = round(sum(tier_scores) / tier_weights, 2) if tier_weights > 0 else None

    # Recalculate overall
    all_weighted = []
    total_weight = 0
    for tid, tdata in results["tier_scores"].items():
        for cid, cdata in tdata["criteria"].items():
            if cdata["score"] is not None:
                w = cdata.get("weight", 1.0)
                all_weighted.append(cdata["score"] * w)
                total_weight += w

    results["overall_score"] = round(sum(all_weighted) / total_weight, 2) if total_weight > 0 else None
    results["llm_enhanced"] = True

    return results


def main():
    parser = argparse.ArgumentParser(
        description="LLM-assisted DEBMM assessment scoring.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("response", type=Path, help="Path to completed response YAML")
    parser.add_argument("--rubric", type=Path, default=DEFAULT_RUBRIC)
    parser.add_argument("--questionnaire", type=Path, default=DEFAULT_QUESTIONNAIRE)
    parser.add_argument(
        "--provider", choices=["openai", "anthropic"], default="anthropic",
        help="LLM provider (default: anthropic)",
    )
    parser.add_argument(
        "--model", default=None,
        help="Model name (default: claude-sonnet-4-6 for anthropic, gpt-4o for openai)",
    )
    parser.add_argument("--report", type=Path, help="Output markdown report path")
    parser.add_argument("--json-out", type=Path, help="Save full JSON results")
    parser.add_argument("--llm-json-out", type=Path, help="Save raw LLM analysis JSON")
    parser.add_argument("--dry-run", action="store_true", help="Print prompt without calling API")

    args = parser.parse_args()

    if args.model is None:
        args.model = "claude-sonnet-4-6" if args.provider == "anthropic" else "gpt-4o"

    # Run automated scoring first
    print("Running automated scoring...")
    results = run_scoring(args.rubric, args.questionnaire, args.response)

    if not results["needs_review"]:
        print("No text answers to review. Running report generation only.")
        if args.report:
            report_md = generate_report(results)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"Report saved to: {args.report}")
        return

    # Build LLM prompt
    print("Building LLM analysis prompt...")
    rubric_context = build_rubric_context(args.rubric)
    questionnaire = load_yaml(args.questionnaire)
    prompt = build_analysis_prompt(results, rubric_context, questionnaire)

    if args.dry_run:
        print("\n" + "=" * 60)
        print("DRY RUN - Prompt that would be sent to LLM:")
        print("=" * 60)
        print(prompt)
        print("=" * 60)
        print(f"\nProvider: {args.provider}")
        print(f"Model: {args.model}")
        print(f"Text answers to score: {len(results['needs_review'])}")
        return

    # Call LLM
    print(f"Calling {args.provider} ({args.model})...")
    if args.provider == "openai":
        llm_analysis = call_openai(prompt, args.model)
    else:
        llm_analysis = call_anthropic(prompt, args.model)

    print("LLM analysis complete.")

    # Save raw LLM output if requested
    if args.llm_json_out:
        with open(args.llm_json_out, "w", encoding="utf-8") as f:
            json.dump(llm_analysis, f, indent=2)
        print(f"LLM analysis saved to: {args.llm_json_out}")

    # Merge LLM scores into results
    merged_results = merge_llm_scores(results, llm_analysis, questionnaire)

    # Save full results if requested
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(merged_results, f, indent=2, default=str)
        print(f"Full results saved to: {args.json_out}")

    # Generate report
    report_md = generate_report(merged_results, llm_analysis)

    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(report_md)
        print(f"Report saved to: {args.report}")
    else:
        print(report_md)


if __name__ == "__main__":
    main()
