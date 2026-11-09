import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Algorithm Recipe: points awarded for each kind of match.
DEFAULT_WEIGHTS = {
    "genre": 2.0,     # exact genre match
    "mood": 1.0,      # exact mood match
    "energy": 1.0,    # max points when energy equals the target; shrinks with distance
    "acoustic": 0.5,  # bonus/penalty for acousticness vs. the user's acoustic taste
}


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def score_song(user_prefs: Dict, song: Dict, weights: Optional[Dict] = None) -> Tuple[float, List[str]]:
    """Score one song against user preferences; return (score, list of reasons)."""
    w = weights or DEFAULT_WEIGHTS
    score = 0.0
    reasons: List[str] = []

    if song["genre"] == user_prefs.get("genre"):
        score += w["genre"]
        reasons.append(f"genre match (+{w['genre']:.1f})")

    if song["mood"] == user_prefs.get("mood"):
        score += w["mood"]
        reasons.append(f"mood match (+{w['mood']:.1f})")

    if "energy" in user_prefs:
        closeness = 1.0 - abs(song["energy"] - user_prefs["energy"])
        points = w["energy"] * closeness
        score += points
        reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} (+{points:.2f})")

    if "likes_acoustic" in user_prefs:
        # Reward acoustic songs for acoustic fans, electronic songs for everyone else.
        fit = song["acousticness"] if user_prefs["likes_acoustic"] else 1.0 - song["acousticness"]
        points = w["acoustic"] * fit
        score += points
        reasons.append(f"acoustic fit (+{points:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5,
                    weights: Optional[Dict] = None) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k as (song, score, explanation), best first."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights)
        scored.append((song, score, "; ".join(reasons)))
    # sorted() returns a new list and leaves `songs` untouched; list.sort() would mutate in place.
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs from a CSV file into dicts, converting numeric fields to int/float."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            for key in ("energy", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)
    return songs


def _profile_to_prefs(user: UserProfile) -> Dict:
    """Convert a UserProfile into the dict format used by score_song."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }


class Recommender:
    """OOP wrapper around the scoring logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for the user, best first."""
        prefs = _profile_to_prefs(user)
        ranked = sorted(self.songs, key=lambda s: score_song(prefs, s.__dict__)[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain in words why a song scored the way it did."""
        score, reasons = score_song(_profile_to_prefs(user), song.__dict__)
        return f"Score {score:.2f}: " + "; ".join(reasons)
