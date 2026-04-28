"""
Command line runner for the Music Recommender Simulation.

Run with:
    python -m src.main
"""

import sys
import os
import logging

sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs, recommend_songs
from evaluator import evaluate_run, confidence_score, confidence_label

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "likes_acoustic": False,
    },
}

EXPECTED = {
    "High-Energy Pop": {"expected_top": "Sunrise City"},
    "Chill Lofi": {"expected_top_any": ["Library Rain", "Midnight Coding"]},
    "Deep Intense Rock": {"expected_top": "Storm Runner"},
}


def print_recommendations(profile_name: str, user_prefs: dict, songs: list, k: int = 5) -> dict:
    """Print recommendations for one profile and return the evaluation result."""
    logger.info("Running profile: %s", profile_name)
    print(f"\n{'='*50}")
    print(f"Profile: {profile_name}")
    print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}  |  Energy: {user_prefs['energy']}")
    print(f"{'='*50}")

    recommendations = recommend_songs(user_prefs, songs, k=k)

    if not recommendations:
        logger.warning("No results returned for profile: %s", profile_name)
        print("  No recommendations found.")
        return {"passed": False, "reason": "No results", "avg_confidence": 0.0, "confidences": []}

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        conf = confidence_label(confidence_score(score))
        print(f"  {rank}. {song['title']} by {song['artist']}")
        print(f"     Score : {score:.2f}  |  Confidence: {conf}")
        print(f"     Why   : {explanation}")
        print()

    eval_kwargs = EXPECTED.get(profile_name, {})
    eval_result = evaluate_run(recommendations, **eval_kwargs)

    status = "PASS" if eval_result["passed"] else "FAIL"
    print(f"  Evaluation: {status} | Avg Confidence: {eval_result['avg_confidence']:.2f} | {eval_result['reason']}")
    logger.info(
        "Profile '%s': %s | avg_confidence=%.2f",
        profile_name, status, eval_result["avg_confidence"],
    )

    return eval_result


def main() -> None:
    logger.info("Music Recommender starting")

    try:
        songs = load_songs("data/songs.csv")
    except FileNotFoundError:
        logger.error("data/songs.csv not found — run from the project root directory")
        sys.exit(1)

    logger.info("Loaded %d songs from catalog", len(songs))
    print(f"Loaded {len(songs)} songs from catalog.\n")

    results = {}
    for profile_name, user_prefs in PROFILES.items():
        results[profile_name] = print_recommendations(profile_name, user_prefs, songs, k=5)

    passed = sum(1 for r in results.values() if r.get("passed"))
    total = len(results)
    all_confidences = [c for r in results.values() for c in r.get("confidences", [])]
    overall_avg = round(sum(all_confidences) / len(all_confidences), 2) if all_confidences else 0.0

    print(f"\n{'='*50}")
    print(f"  Evaluation Summary: {passed}/{total} profiles PASSED")
    print(f"  Overall avg confidence: {overall_avg:.2f}")
    print(f"{'='*50}\n")
    logger.info("Done. %d/%d passed. Overall avg confidence: %.2f", passed, total, overall_avg)


if __name__ == "__main__":
    main()
