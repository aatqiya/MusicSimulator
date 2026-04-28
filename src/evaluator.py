"""
Evaluation utilities: confidence scoring and recommendation quality checks.
"""

from typing import Dict, List, Tuple

MAX_POSSIBLE_SCORE = 4.5  # genre(2.0) + mood(1.0) + energy(1.0) + acoustic(0.5)


def confidence_score(score: float) -> float:
    """Return a 0.0–1.0 confidence value for a recommendation score."""
    return round(min(score / MAX_POSSIBLE_SCORE, 1.0), 2)


def confidence_label(confidence: float) -> str:
    """Return a human-readable label for a confidence value."""
    if confidence >= 0.75:
        return "High"
    if confidence >= 0.45:
        return "Medium"
    return "Low"


def evaluate_run(
    results: List[Tuple[Dict, float, str]],
    expected_top: str | None = None,
    expected_top_any: List[str] | None = None,
) -> Dict:
    """
    Evaluate a single recommender run against expected outcomes.

    Returns a dict with: passed (bool), confidence scores, avg_confidence.
    """
    if not results:
        return {"passed": False, "reason": "No results returned", "avg_confidence": 0.0}

    top_title = results[0][0]["title"]
    confidences = [confidence_score(score) for _, score, _ in results]
    avg_confidence = round(sum(confidences) / len(confidences), 2)

    passed = True
    reason = "OK"

    if expected_top and top_title != expected_top:
        passed = False
        reason = f"Expected '{expected_top}' at #1, got '{top_title}'"
    elif expected_top_any and top_title not in expected_top_any:
        passed = False
        reason = f"Expected one of {expected_top_any} at #1, got '{top_title}'"

    return {
        "passed": passed,
        "reason": reason,
        "top_title": top_title,
        "confidences": confidences,
        "avg_confidence": avg_confidence,
    }
