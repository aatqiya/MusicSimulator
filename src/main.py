"""
Command line runner for the Music Recommender Simulation.

Run with:
    python -m src.main
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs, recommend_songs


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


def print_recommendations(profile_name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print a formatted recommendation block for one user profile."""
    print(f"\n{'='*50}")
    print(f"Profile: {profile_name}")
    print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}  |  Energy: {user_prefs['energy']}")
    print(f"{'='*50}")
    recommendations = recommend_songs(user_prefs, songs, k=k)
    if not recommendations:
        print("  No recommendations found.")
        return
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  {rank}. {song['title']} by {song['artist']}")
        print(f"     Score : {score:.2f}")
        print(f"     Why   : {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs from catalog.\n")

    for profile_name, user_prefs in PROFILES.items():
        print_recommendations(profile_name, user_prefs, songs, k=5)


if __name__ == "__main__":
    main()
