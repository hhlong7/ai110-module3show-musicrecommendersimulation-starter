# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder suggests the top 5 songs from a small catalog based on a user's favorite genre, favorite mood, target energy level, and whether they like acoustic music. It assumes each user has one fixed taste. It is built for classroom exploration, not for real listeners or production use.

---

## 3. How the Model Works

Every song gets a score for how well it fits the user, and the highest scores win.

- A song earns **2 points** if its genre is the user's favorite genre.
- It earns **1 point** if its mood matches the favorite mood.
- It earns **up to 1 point for energy**: the closer the song's energy is to the user's target, the more points. A song exactly on target gets the full point; a song at the opposite extreme gets almost none.
- It earns **up to half a point for acoustic fit**: acoustic songs for people who like acoustic music, electronic-sounding songs for everyone else.

The program then sorts all 20 songs by score and shows the top five, each with a short list of reasons ("genre match", "energy close to target"). Compared with the starter code, which returned nothing, I wrote the whole scoring and ranking logic, and the explanations.

---

## 4. Data

The catalog (`data/songs.csv`) has 20 songs: the 10 starter songs plus 10 I added. Genres: pop, indie pop, lofi, rock, ambient, jazz, synthwave, hip hop, r&b, country, edm, classical, metal, reggae, folk, punk, and latin. Moods include happy, chill, intense, relaxed, moody, focused, confident, romantic, nostalgic, euphoric, serene, aggressive, warm, and rebellious. Each song also has tempo, valence, danceability, and acousticness, though only energy and acousticness are used in scoring.

Missing: lyrics, language, artist similarity, era, and any real listening history. Most genres have exactly one song, and lofi has three, so lofi fans get more variety than anyone else.

---

## 5. Strengths

- Works well when the user's genre and mood exist in the catalog: the Chill Lofi and Deep Intense Rock profiles returned exactly what I would expect (Library Rain and Storm Runner on top).
- Energy closeness is a more sensible rule than "higher is better", so a calm user is not shown loud songs.
- Every recommendation comes with reasons, so it is easy to see why a song ranked where it did.

---

## 6. Limitations and Bias

The system over-prioritizes genre. In the "Classical but energy 1.0" test, the only classical song (energy 0.20) ranked first with 3.69 points because it earned genre and mood bonuses, even though it is the opposite of what the user asked for on energy. Genre is worth up to twice as much as the whole energy score.

Exact-string matching treats "pop" and "indie pop" as unrelated, and "chill" and "relaxed" as unrelated, so near-matches get no credit. Users whose favorite genre or mood is not in the catalog (the blues/sad profile) get nearly tied scores and effectively random-looking results. With only 20 songs and mostly one song per genre, users of rare genres get one real match and then filler. Lofi listeners are favored because lofi has three songs. The system also never shows anything surprising, which can create a filter bubble.

---

## 7. Evaluation

I tested five profiles: Happy Pop, Chill Lofi, Deep Intense Rock, and two adversarial ones (blues/sad with energy 0.9, and classical/serene with energy 1.0). For the first three, the top result matched my intuition each time.

**Profile comparisons.**
- *Happy Pop vs. Deep Intense Rock:* Both like high energy, but Pop's top 3 are bright songs (Sunrise City, Gym Hero, Rooftop Lights) while Rock's are harder (Storm Runner, Gym Hero, Basement Static). Gym Hero appears in both because it is pop *and* intense, which is why a gym song can show up for someone who just wants "Happy Pop": it matches on genre and energy even though its mood is wrong.
- *Chill Lofi vs. Happy Pop:* Lofi's list is all low-energy and acoustic; Pop's is high-energy and electronic. The energy and acoustic terms are clearly doing their job.
- *Blues/sad vs. Chill Lofi:* Lofi has clear winners (4.43 vs. 4.29 vs. 3.34); blues/sad has five songs within 0.05 points of each other, so the ranking is basically arbitrary. That shows the output is only meaningful when the profile matches the catalog.

**Experiment.** I halved the genre weight (2.0 to 1.0) and doubled the energy weight (1.0 to 2.0). Happy Pop's list became more varied across genres: Rooftop Lights moved above Gym Hero and non-pop songs like Concrete Jungle entered the top 5. The change made results different rather than clearly better, but it confirmed that genre was the dominant factor.

**Surprise:** how confident the system looks when it is wrong. The adversarial profiles still got scored lists without any warning that nothing fit.

I also ran the two starter unit tests, which pass.

---

## 8. Future Work

- Use partial credit for related genres and moods (pop vs. indie pop) instead of exact matches.
- Add tempo, valence, and danceability to the score, and let users set their own weights.
- Add a diversity step so the top 5 are not near-duplicates, and warn when no song is a good match.
- Grow the catalog so each genre has several songs.

---

## 9. Personal Reflection

My biggest learning moment was seeing that the "intelligence" is mostly the weights I chose: changing two numbers visibly changed the rankings. AI tools helped me draft the scoring function and the experiments quickly, but I had to double-check the output myself, for example confirming the energy math and noticing that the adversarial classical profile exposed a flaw the happy path hid. What surprised me is how a few simple rules and a sort can feel like a real recommendation, especially with the reasons printed next to each song. Next I would add collaborative signals like skips and likes, and a diversity rule so the system can surprise people.
