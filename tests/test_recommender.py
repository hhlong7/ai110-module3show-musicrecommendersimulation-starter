from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


from src.recommender import load_songs, score_song, recommend_songs, DEFAULT_WEIGHTS


def _song(**overrides):
    base = {"title": "T", "artist": "A", "genre": "pop", "mood": "happy",
            "energy": 0.8, "acousticness": 0.2}
    base.update(overrides)
    return base


def test_load_songs_converts_numbers():
    songs = load_songs("data/songs.csv")
    assert len(songs) == 20
    assert isinstance(songs[0]["energy"], float)
    assert isinstance(songs[0]["id"], int)


def test_score_song_genre_and_mood_bonus_with_reasons():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    score, reasons = score_song(prefs, _song())
    assert score == DEFAULT_WEIGHTS["genre"] + DEFAULT_WEIGHTS["mood"] + DEFAULT_WEIGHTS["energy"]
    assert any("genre match" in r for r in reasons)
    assert any("mood match" in r for r in reasons)


def test_score_song_closer_energy_scores_higher():
    prefs = {"energy": 0.5}
    near, _ = score_song(prefs, _song(energy=0.55))
    far, _ = score_song(prefs, _song(energy=0.95))
    assert near > far


def test_recommend_songs_sorted_and_limited_to_k():
    songs = load_songs("data/songs.csv")
    prefs = {"genre": "lofi", "mood": "chill", "energy": 0.35}
    results = recommend_songs(prefs, songs, k=3)
    assert len(results) == 3
    scores = [score for _, score, _ in results]
    assert scores == sorted(scores, reverse=True)
    assert results[0][0]["genre"] == "lofi"


def test_recommend_songs_does_not_mutate_input():
    songs = load_songs("data/songs.csv")
    original_order = [s["id"] for s in songs]
    recommend_songs({"genre": "rock", "energy": 0.9}, songs, k=5)
    assert [s["id"] for s in songs] == original_order


def test_custom_weights_change_ranking():
    songs = [_song(title="GenreMatch", genre="pop", energy=0.1),
             _song(title="EnergyMatch", genre="rock", energy=0.9)]
    prefs = {"genre": "pop", "energy": 0.9}
    default_top = recommend_songs(prefs, songs, k=1)[0][0]["title"]
    shifted = {**DEFAULT_WEIGHTS, "genre": 0.1, "energy": 3.0}
    shifted_top = recommend_songs(prefs, songs, k=1, weights=shifted)[0][0]["title"]
    assert default_top == "GenreMatch"
    assert shifted_top == "EnergyMatch"
