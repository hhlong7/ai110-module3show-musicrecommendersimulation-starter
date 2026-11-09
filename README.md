# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version is a content-based music recommender (VibeFinder 1.0). It loads a 20-song catalog from `data/songs.csv`, scores every song against a user's taste profile (favorite genre, mood, target energy, and acoustic preference), and returns the top matches along with a plain-language explanation of each score.

---

## How The System Works

Real platforms like Spotify and YouTube combine two ideas. **Collaborative filtering** learns from other users' behavior (likes, skips, playlists, listening history): "people who liked what you like also liked this." **Content-based filtering** looks at the attributes of the songs themselves (genre, mood, tempo, energy). This project implements only the content-based side, because we have no other users' data, just a catalog and one taste profile.

**Song features:** `genre`, `mood`, `energy` (0-1), `tempo_bpm`, `valence`, `danceability`, `acousticness`. The score uses genre, mood, energy, and acousticness.

**UserProfile:** `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`.

**Algorithm Recipe (Scoring Rule, one song):**

- +2.0 if the song's genre equals the favorite genre
- +1.0 if the song's mood equals the favorite mood
- up to +1.0 for energy: `1 - |song_energy - target_energy|`, so closer is better (rewards closeness rather than just "higher" or "lower")
- up to +0.5 for acoustic fit: `acousticness` if the user likes acoustic, `1 - acousticness` otherwise
- every contribution is recorded as a "reason" so each recommendation is explainable

**Ranking Rule (list of songs):** the scoring rule judges a single song in isolation; the ranking rule applies it to every song in the catalog and sorts by score, highest first, keeping the top k. We need both because a score alone is meaningless until songs are compared against each other.

**Data flow:** Input (user prefs) -> Process (loop over every song in the CSV, call `score_song`) -> Output (sorted top-k with reasons).

**Expected biases:** genre is worth the most, so the system may over-prioritize genre and bury great songs that match the mood and energy but are in a different genre. Exact-string matching also means "pop" and "indie pop" are treated as completely different.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` (first three profiles shown; the full run also includes two adversarial profiles and a weight experiment):

```text
=== Happy Pop (default) ===
User profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}
Recommendations:
  1. Sunrise City by Neon Echo - Score: 4.39
     Because: genre match (+2.0); mood match (+1.0); energy 0.82 vs target 0.80 (+0.98); acoustic fit (+0.41)
  2. Gym Hero by Max Pulse - Score: 3.35
     Because: genre match (+2.0); energy 0.93 vs target 0.80 (+0.87); acoustic fit (+0.47)
  3. Rooftop Lights by Indigo Parade - Score: 2.29
     Because: mood match (+1.0); energy 0.76 vs target 0.80 (+0.96); acoustic fit (+0.33)
  4. Concrete Jungle by Lyric Smith - Score: 1.42
     Because: energy 0.78 vs target 0.80 (+0.98); acoustic fit (+0.44)
  5. Storm Runner by Voltline - Score: 1.34
     Because: energy 0.91 vs target 0.80 (+0.89); acoustic fit (+0.45)

=== Chill Lofi ===
User profile: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True}
Recommendations:
  1. Library Rain by Paper Lanterns - Score: 4.43
     Because: genre match (+2.0); mood match (+1.0); energy 0.35 vs target 0.35 (+1.00); acoustic fit (+0.43)
  2. Midnight Coding by LoRoom - Score: 4.29
     Because: genre match (+2.0); mood match (+1.0); energy 0.42 vs target 0.35 (+0.93); acoustic fit (+0.35)
  3. Focus Flow by LoRoom - Score: 3.34
     Because: genre match (+2.0); energy 0.40 vs target 0.35 (+0.95); acoustic fit (+0.39)
  4. Spacewalk Thoughts by Orbit Bloom - Score: 2.39
     Because: mood match (+1.0); energy 0.28 vs target 0.35 (+0.93); acoustic fit (+0.46)
  5. Porch Light Sessions by Wren & Willow - Score: 1.44
     Because: energy 0.38 vs target 0.35 (+0.97); acoustic fit (+0.47)

=== Deep Intense Rock ===
User profile: {'genre': 'rock', 'mood': 'intense', 'energy': 0.92, 'likes_acoustic': False}
Recommendations:
  1. Storm Runner by Voltline - Score: 4.44
     Because: genre match (+2.0); mood match (+1.0); energy 0.91 vs target 0.92 (+0.99); acoustic fit (+0.45)
  2. Gym Hero by Max Pulse - Score: 2.46
     Because: mood match (+1.0); energy 0.93 vs target 0.92 (+0.99); acoustic fit (+0.47)
  3. Basement Static by Hollow Teeth - Score: 1.46
     Because: energy 0.92 vs target 0.92 (+1.00); acoustic fit (+0.46)
  4. Neon Pulse by Circuit Kid - Score: 1.45
     Because: energy 0.96 vs target 0.92 (+0.96); acoustic fit (+0.48)
  5. Iron Cathedral by Black Meridian - Score: 1.42
     Because: energy 0.98 vs target 0.92 (+0.94); acoustic fit (+0.48)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

**Weight shift (genre 2.0 -> 1.0, energy 1.0 -> 2.0).** For the Happy Pop profile, *Rooftop Lights* (indie pop, happy, energy 0.76) jumped from #3 (2.29) to #2 (3.25) and passed *Gym Hero* (pop, intense, energy 0.93), and non-pop songs like *Concrete Jungle* and *Night Drive Loop* filled the rest of the list. The results became more varied across genres but arguably less "on genre." For Deep Intense Rock, the order of the top 5 stayed nearly identical, because high-energy songs were already the best matches.

**Adversarial profiles.**

- *Blues / sad / energy 0.9*: no blues or sad songs exist, so only the energy and acoustic terms contribute and the top five scores are nearly tied (0.99-1.04). The system confidently ranks songs that don't match the user's genre or mood at all.
- *Classical / serene / energy 1.0*: the lone classical song ranks #1 (3.69) purely from genre + mood, even though its energy (0.20) is the opposite of what the user asked for. The genre/mood bonus overwhelms a huge energy mismatch.

**Different users.** Lofi fans get quiet, acoustic songs; rock fans get loud, electronic-leaning songs; the acoustic term mainly acts as a tie-breaker.

---

## Limitations and Risks

- Tiny catalog (20 songs); most genres have only one song, so a user whose favorite genre is represented once gets one genre match and then filler.
- Exact-match genre and mood: "pop" vs. "indie pop" earn zero genre credit, and mood labels like "chill" vs. "relaxed" are treated as unrelated.
- Genre is weighted heavily, so it can outrank a much better energy fit (see the classical experiment).
- Ignores tempo, valence, danceability, lyrics, language, artist, and listening history.
- No diversity control: the top 5 can be near-duplicates, and the user never gets surprised.

See [model_card.md](model_card.md) for more.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this showed me how little machinery it takes to make recommendations feel intelligent: a handful of numeric and categorical features, a few hand-picked weights, and a sort. The "magic" is really the weights, and choosing them is a value judgment about what matters in taste. Turning data into predictions means turning a song and a person into numbers that can be compared, and the explanation list made it easy to see exactly why a song won.

Bias can show up in many places: a catalog dominated by a few genres, exact-match rules that treat near-identical genres as unrelated, weights that favor one feature, and profiles that assume one fixed taste per user. In a real system the same patterns would create filter bubbles, since users only get more of what they already listed, and would under-serve people whose tastes fall into categories the data barely covers.
