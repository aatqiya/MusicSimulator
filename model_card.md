# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 is designed to suggest songs from a small catalog based on a user's preferred genre, mood, and energy level. It is built for classroom exploration — not production use. It assumes users can describe their taste numerically (e.g., "I like high-energy music") and that songs can be meaningfully compared using a handful of attributes. It should not be used as a real product or to influence actual music distribution.

---

## 3. How the Model Works

Each song in the catalog has attributes: genre, mood, energy (a number from 0 to 1), and acousticness. The user provides a taste profile with a preferred genre, preferred mood, a target energy level, and whether they like acoustic music.

To score a song, the system adds up points:
- If the song's genre matches the user's favorite, it earns 2 points — the biggest single reward.
- If the song's mood matches, it earns 1 more point.
- The closer the song's energy is to the user's target, the more energy points it earns — up to 1 point for a perfect match, scaling down to 0 for a completely opposite energy.
- If the user likes acoustic music and the song is highly acoustic, it gets a small bonus of 0.5 points.

Once every song has a score, they are sorted from highest to lowest and the top results are returned. The system also explains each recommendation in plain language so users understand exactly why a song appeared. A confidence label (High / Medium / Low) is attached to each result based on its score relative to the theoretical maximum of 4.5.

---

## 4. Data

The catalog contains 18 songs stored in `data/songs.csv`. Each song has: title, artist, genre, mood, energy, tempo in BPM, valence, danceability, and acousticness. The original 10 songs were provided as a starter dataset; 8 additional songs were added to improve diversity. The expanded catalog now covers: pop, lofi, rock, ambient, jazz, synthwave, indie pop, EDM, folk, country, R&B, metal, bossa nova, hip-hop, and classical.

Despite the expansion, the catalog is still very small. Most genres have only one or two songs, so users whose preferences fall outside of pop or lofi will get sparse recommendations. The dataset also has no information about lyrics, language, era, or cultural origin, which are significant factors in real musical taste.

---

## 5. Strengths

- The system works best for users with clearly defined tastes in the most-represented genres (pop and lofi), where there are multiple songs to choose from and meaningful differentiation in scores.
- The explanation feature makes recommendations transparent — users can see exactly why a song ranked where it did, which is rare in real systems.
- The scoring logic is simple enough to audit by hand, making it easy to spot and correct unexpected behavior.
- For the "Chill Lofi" profile, the results felt genuinely accurate — the top two songs were both lofi and chill, differentiated by energy proximity and acoustic bonus.

---

## 6. Limitations and Bias

The biggest limitation is genre over-representation. Pop songs have the best chance of appearing in recommendations because there are more of them and the genre weight is the largest single factor. A user who loves bossa nova or classical will almost never see their preferred genre score genre-match points because there is only one song in each of those categories.

The system also creates a filter bubble. Because genre is the dominant signal, users repeatedly see the same genre cluster at the top. There is no diversity mechanism to introduce variety, so a pop fan will never encounter a jazz song even if the mood and energy would be a perfect fit.

Another limitation is that the energy score is symmetric — a song at 0.3 energy and a song at 0.7 energy get identical energy penalties for a user targeting 0.5. This treats overenergy the same as underenergy, which does not match most users' actual experience.

Finally, the system has no notion of what the user has already heard, so it will recommend the same top song every time with no way to provide fresh suggestions.

**Misuse potential:** Because the scoring weights are fully exposed, a bad actor could reverse-engineer the catalog to make any song surface first by tuning its metadata. In a real production system, the scoring logic would not be public. The system should also never be used to make decisions about which artists receive promotion or distribution — it reflects catalog size bias, not musical quality.

---

## 7. Evaluation

Three distinct profiles were tested:

- **High-Energy Pop** (genre: pop, mood: happy, energy: 0.85): Results felt accurate. "Sunrise City" was a clear top pick with near-perfect matches on all three scored attributes. "Gym Hero" was correctly ranked second despite being "intense" rather than "happy" — it still earned genre and energy points. Avg confidence: 0.51.

- **Chill Lofi** (genre: lofi, mood: chill, energy: 0.38, likes acoustic: true): Results also felt right. "Library Rain" and "Midnight Coding" were nearly tied, which makes sense because both are lofi + chill + low energy + acoustic. The acoustic bonus was the tiebreaker. Avg confidence: 0.72 — the highest of all three profiles.

- **Deep Intense Rock** (genre: rock, mood: intense, energy: 0.92): Only one rock song exists in the catalog, so Storm Runner dominated at position 1. Positions 2–5 were filled by high-energy songs from other genres. This exposed the catalog's thinness for niche genres. Avg confidence: 0.44 — the lowest, reflecting how quickly results degrade when genre coverage is thin.

An adversarial test with contradictory preferences (lofi + intense + 0.9 energy) confirmed the system cannot serve users with internally conflicting tastes — it splits its points between genre and energy with no song winning on both.

**Overall: 3/3 profiles PASSED. Overall avg confidence: 0.56.**

---

## 8. Future Work

1. **Add a diversity penalty.** If the same genre or artist already appears in the top results, apply a small score reduction to the next song from that genre/artist. This would break up filter bubbles naturally.

2. **Use valence and danceability in scoring.** These attributes are already in the dataset but ignored. A user could specify a minimum valence ("I want upbeat music") and those features could add or subtract points accordingly.

3. **Expand the catalog significantly.** Eighteen songs is not enough to make meaningful recommendations for niche genres. A catalog of at least 100 songs across 15+ genres would make the scoring differences matter more.

4. **Replace fixed weights with learned weights.** Instead of hardcoding 2.0 for genre and 1.0 for mood, the system could ask users to rate a few recommendations and then adjust the weights based on their feedback — a simple form of learning.

---

## 9. Personal Reflection

The most surprising moment was realizing how quickly a simple scoring rule creates a filter bubble. After testing just three profiles, it was obvious that pop songs dominated results even for users who had no genre preference because pop happened to match mood and energy more often in this small catalog. Real recommender systems face the same problem at a vastly larger scale, and the industry solutions — diversity re-ranking, serendipity injection — all exist precisely because naive scoring always trends toward the familiar.

Using fixed weights also made me think differently about how Spotify's "Discover Weekly" actually works. Collaborative filtering sidesteps the weight problem entirely by saying "people like you listened to this" rather than "this song scores 3.47." That approach requires millions of data points but avoids the brittleness I ran into with hand-tuned weights. Building this toy version made the trade-offs between interpretability and accuracy feel very real — the simpler the model, the easier it is to explain, but the worse it handles edge cases.

---

## 10. AI Collaboration

AI (Claude) was used throughout this project as a coding partner and design reviewer.

**Helpful suggestion:** When building the evaluator, Claude suggested attaching human-readable confidence labels ("High / Medium / Low") on top of raw numeric confidence scores, rather than just printing the float. This made the terminal output immediately interpretable without forcing users to mentally map 0.72 onto a quality scale. That suggestion was adopted directly and improved the readability of every output block.

**Flawed suggestion:** Claude initially suggested doubling the energy weight — replacing `1.0 - energy_gap` with `2.0 - 2*energy_gap` — arguing it would give more nuanced differentiation between songs with similar genres. In practice (Experiment 3), this caused "Gym Hero" (pop, intense) to overtake "Storm Runner" (rock, intense) for the Deep Rock profile purely on energy proximity, overriding the genre signal entirely. The suggestion was rejected after testing confirmed it broke the genre-first priority the system is designed around.
