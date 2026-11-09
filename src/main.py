"""Command line runner for the Music Recommender Simulation."""

from pathlib import Path

from .recommender import load_songs, recommend_songs, DEFAULT_WEIGHTS

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "songs.csv"

PROFILES = {
    "Happy Pop (default)": {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92, "likes_acoustic": False},
    # Adversarial: conflicting preferences (high energy but sad mood, genre not in catalog)
    "Conflicted (energy 0.9 + sad)": {"genre": "blues", "mood": "sad", "energy": 0.9, "likes_acoustic": True},
    # Adversarial: calm genre but maximum energy
    "Classical but 1.0 energy": {"genre": "classical", "mood": "serene", "energy": 1.0, "likes_acoustic": True},
}


def show(title: str, prefs: dict, songs: list, k: int = 5, weights: dict = None) -> None:
    print(f"\n=== {title} ===")
    print(f"User profile: {prefs}")
    print("Recommendations:")
    for i, (song, score, why) in enumerate(recommend_songs(prefs, songs, k=k, weights=weights), 1):
        print(f"  {i}. {song['title']} by {song['artist']} - Score: {score:.2f}")
        print(f"     Because: {why}")


def main() -> None:
    songs = load_songs(str(DATA_PATH))
    print(f"Loaded songs: {len(songs)}")

    for title, prefs in PROFILES.items():
        show(title, prefs, songs)

    # Experiment: double energy weight, halve genre weight
    shifted = {**DEFAULT_WEIGHTS, "genre": 1.0, "energy": 2.0}
    show("EXPERIMENT (genre x0.5, energy x2): Happy Pop", PROFILES["Happy Pop (default)"], songs, weights=shifted)
    show("EXPERIMENT (genre x0.5, energy x2): Deep Intense Rock", PROFILES["Deep Intense Rock"], songs, weights=shifted)


if __name__ == "__main__":
    main()
