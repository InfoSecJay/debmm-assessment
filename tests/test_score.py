"""Unit tests for the core scoring helpers in scorer/score.py.

Focus: the three pure functions that encode the DEBMM methodology —
question-level scoring, criterion-level aggregation, and tier
determination with the progressive-cap rule. These are the parts that
must not regress between releases.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Make scorer/ importable when running pytest from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scorer"))

from score import (  # noqa: E402
    compute_criterion_score,
    determine_tier,
    score_question,
)


# ── score_question ─────────────────────────────────────────────────────────


SCALE_Q = {"id": "T0-Q1", "type": "scale"}
CHECKLIST_Q_DEFINED = {
    "id": "T0-Q2",
    "type": "checklist",
    "scoring": {"yes_value": 3},
}
CHECKLIST_Q_MANAGED = {
    "id": "T0-Q3",
    "type": "checklist",
    "scoring": {"yes_value": 4},
}


def test_scale_valid_answer_scores_directly():
    result = score_question(SCALE_Q, 3)
    assert result["score"] == 3
    assert result["status"] == "scored"


def test_scale_out_of_range_is_invalid():
    result = score_question(SCALE_Q, 6)
    assert result["score"] is None
    assert result["status"] == "invalid"


def test_checklist_yes_uses_per_question_yes_value():
    # The Yes-value mapping is intentionally per-question — the same
    # Yes signals different maturity depending on what's being asked.
    assert score_question(CHECKLIST_Q_DEFINED, True)["score"] == 3
    assert score_question(CHECKLIST_Q_MANAGED, True)["score"] == 4


def test_checklist_no_always_maps_to_one():
    assert score_question(CHECKLIST_Q_DEFINED, False)["score"] == 1
    assert score_question(CHECKLIST_Q_MANAGED, False)["score"] == 1


def test_unanswered_returns_none_score():
    result = score_question(SCALE_Q, None)
    assert result["score"] is None
    assert result["status"] == "unanswered"


# ── compute_criterion_score ───────────────────────────────────────────────


def _scored(value):
    return {"score": value, "status": "scored"}


def test_criterion_average_rounds_to_two_decimals():
    result = compute_criterion_score([_scored(4), _scored(5), _scored(3)])
    assert result["score"] == 4.0
    assert result["level"] == 4
    assert result["level_name"] == "Managed"


def test_criterion_with_no_scored_questions_returns_none():
    result = compute_criterion_score([{"score": None, "status": "unanswered"}])
    assert result["score"] is None
    assert result["scored_count"] == 0


# ── determine_tier — the progressive-cap rule ─────────────────────────────


def _tier_with_scores(*scores):
    """Build the tier_scores fragment determine_tier expects, given the
    criterion scores for that tier."""
    return {
        "criteria": {
            f"crit_{i}": {"score": s} for i, s in enumerate(scores)
        }
    }


def test_all_tiers_passing_yields_tier_4():
    tier_scores = {
        "tier_0": _tier_with_scores(4.0, 4.5),
        "tier_1": _tier_with_scores(3.5, 4.0),
        "tier_2": _tier_with_scores(3.0, 3.0),
        "tier_3": _tier_with_scores(3.0, 3.5),
        "tier_4": _tier_with_scores(3.0, 4.0),
    }
    result = determine_tier(tier_scores)
    assert result["tier_number"] == 4
    assert result["tier_name"] == "Tier 4: Expert"


def test_one_intermediate_failure_caps_tier_at_basic():
    # All Foundation and Basic criteria pass, but one Intermediate
    # criterion is below 3.0 — the progressive-cap rule means the tier
    # stops at Tier 1 even if Advanced and Expert criteria look fine.
    tier_scores = {
        "tier_0": _tier_with_scores(4.0, 4.0),
        "tier_1": _tier_with_scores(4.0, 3.5),
        "tier_2": _tier_with_scores(2.5, 3.0),  # one fails
        "tier_3": _tier_with_scores(4.0, 4.0),
        "tier_4": _tier_with_scores(4.0, 4.0),
    }
    result = determine_tier(tier_scores)
    assert result["tier_number"] == 1
    assert result["tier_name"] == "Tier 1: Basic"


def test_foundation_failure_yields_below_foundation():
    tier_scores = {
        "tier_0": _tier_with_scores(4.0, 2.5),  # one fails
        "tier_1": _tier_with_scores(4.0, 4.0),
        "tier_2": _tier_with_scores(4.0, 4.0),
        "tier_3": _tier_with_scores(4.0, 4.0),
        "tier_4": _tier_with_scores(4.0, 4.0),
    }
    result = determine_tier(tier_scores)
    assert result["tier_number"] == -1
    assert result["tier_name"] == "Below Foundation"


def test_score_exactly_3_is_passing():
    # Boundary check: 3.0 is the Defined threshold, inclusive.
    tier_scores = {
        "tier_0": _tier_with_scores(3.0, 3.0),
        "tier_1": _tier_with_scores(2.99, 3.0),  # 2.99 fails
    }
    result = determine_tier(tier_scores)
    assert result["tier_number"] == 0  # T0 passes, T1 caps
