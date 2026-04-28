# Music Recommender Simulation

## Project Summary

This project simulates a content-based music recommendation system. Given a user's taste profile (preferred genre, mood, and energy level), the system scores every song in a catalog and returns the top matches. It mirrors how real platforms like Spotify surface music using song attributes rather than crowd behavior, making the logic transparent and easy to inspect.

---

## Original Project

This project extends the **Module 2 Music Recommender** mini-project, which introduced `Song` and `UserProfile` dataclasses and a basic three-attribute scoring function over a 10-song hardcoded catalog. The original returned ranked results but had no evaluation tooling, no confidence scoring, no explainability layer, and no reliability testing. This version expands the catalog to 18 songs, adds an `evaluator` module with confidence scoring and pass/fail evaluation, integrates structured logging throughout, and produces a testing summary on every run.

---

## Demo Walkthrough

> **[▶ Watch the Loom walkthrough](YOUR_LOOM_LINK_HERE)** — 5–7 minute video showing all three profiles running end-to-end, confidence labels on each result, and evaluation pass/fail output.

---

## How The System Works

Real-world platforms like Spotify combine two main approaches: **collaborative filtering** (recommending songs that similar users enjoyed) and **content-based filtering** (recommending songs whose attributes match what you already like). This simulation focuses on content-based filtering because it only requires song metadata — no user history needed.

**Features each `Song` uses:**
- `genre` — categorical label (pop, lofi, rock, etc.)
- `mood` — emotional tone (happy, chill, intense, etc.)
- `energy` — float 0.0–1.0, how loud/active the track feels
- `tempo_bpm` — beats per minute
- `valence` — float 0.0–1.0, musical positivity
- `danceability` — float 0.0–1.0, how suitable for dancing
- `acousticness` — float 0.0–1.0, how acoustic vs. electronic

**What the `UserProfile` stores:**
- `favorite_genre` — the genre to match first
- `favorite_mood` — preferred emotional tone
- `target_energy` — ideal energy level (0.0–1.0)
- `likes_acoustic` — boolean preference for acoustic tracks

**Algorithm Recipe (scoring one song):**

| Rule | Points |
|------|--------|
| Genre matches user preference | +2.0 |
| Mood matches user preference | +1.0 |
| Energy proximity: `1.0 - abs(song_energy - target_energy)` | 0.0–1.0 |
| Acoustic bonus (if `likes_acoustic` and `acousticness >= 0.6`) | +0.5 |

**Ranking rule:** All songs are scored, then sorted from highest to lowest. The top K are returned with a confidence label (High / Medium / Low) based on score relative to the theoretical maximum of 4.5.

**Data flow:**

```mermaid
flowchart TD
    A[User Preference Profile\ngenre · mood · energy · likes_acoustic] --> B[Load songs.csv]
    B --> C{For each song in catalog}
    C --> D[score_song\ngenre match +2.0\nmood match +1.0\nenergy proximity 0–1.0\nacoustic bonus +0.5]
    D --> E[Attach score + confidence + reasons to song]
    E --> C
    C --> F[Sort all scored songs\nhighest → lowest]
    F --> G[Return top K results\nwith explanations]
    G --> H[evaluate_run\npass/fail · avg confidence]
    H --> I[Print evaluation summary]
```

> The system architecture diagram is also exported as a PNG in [assets/architecture.png](assets/architecture.png).

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the recommender:

   ```bash
   python -m src.main
   ```

### Running Tests

```bash
pytest
```

---

## Sample Interactions

**Profile: High-Energy Pop** (`genre: pop | mood: happy | energy: 0.85`)

```
==================================================
Profile: High-Energy Pop
  Genre: pop  |  Mood: happy  |  Energy: 0.85
==================================================
  1. Sunrise City by Neon Echo
     Score : 3.97  |  Confidence: High
     Why   : genre match (+2.0); mood match (+1.0); energy similarity (+0.97)

  2. Gym Hero by Max Pulse
     Score : 2.92  |  Confidence: Medium
     Why   : genre match (+2.0); energy similarity (+0.92)

  3. Rooftop Lights by Indigo Parade
     Score : 1.91  |  Confidence: Low
     Why   : mood match (+1.0); energy similarity (+0.91)

  Evaluation: PASS | Avg Confidence: 0.51 | OK
```

**Profile: Chill Lofi** (`genre: lofi | mood: chill | energy: 0.38 | likes_acoustic: true`)

```
==================================================
Profile: Chill Lofi
  Genre: lofi  |  Mood: chill  |  Energy: 0.38
==================================================
  1. Library Rain by Paper Lanterns
     Score : 4.47  |  Confidence: High
     Why   : genre match (+2.0); mood match (+1.0); energy similarity (+0.97); acoustic preference (+0.5)

  2. Midnight Coding by LoRoom
     Score : 4.46  |  Confidence: High
     Why   : genre match (+2.0); mood match (+1.0); energy similarity (+0.96); acoustic preference (+0.5)

  3. Focus Flow by LoRoom
     Score : 3.48  |  Confidence: High
     Why   : genre match (+2.0); energy similarity (+0.98); acoustic preference (+0.5)

  Evaluation: PASS | Avg Confidence: 0.72 | OK
```

**Profile: Deep Intense Rock** (`genre: rock | mood: intense | energy: 0.92`)

```
==================================================
Profile: Deep Intense Rock
  Genre: rock  |  Mood: intense  |  Energy: 0.92
==================================================
  1. Storm Runner by Voltline
     Score : 3.99  |  Confidence: High
     Why   : genre match (+2.0); mood match (+1.0); energy similarity (+0.99)

  2. Gym Hero by Max Pulse
     Score : 1.99  |  Confidence: Low
     Why   : mood match (+1.0); energy similarity (+0.99)

  3. Thunder Core by Ironwall
     Score : 1.95  |  Confidence: Low
     Why   : mood match (+1.0); energy similarity (+0.95)

  Evaluation: PASS | Avg Confidence: 0.44 | OK
```

**Evaluation Summary (all runs):**
```
==================================================
  Evaluation Summary: 3/3 profiles PASSED
  Overall avg confidence: 0.56
==================================================
```

<img width="1119" height="660" alt="Screenshot 2026-04-14 at 9 15 26 PM" src="https://github.com/user-attachments/assets/c35acb98-c466-4bc6-a6be-16b802e2bdf5" />
<img width="1111" height="660" alt="Screenshot 2026-04-14 at 9 15 46 PM" src="https://github.com/user-attachments/assets/1f65e33e-e9d0-440f-a72d-020a02960483" />


---

## Design Decisions

**Why content-based filtering?** It requires only song metadata — no user history or other users' behavior. This makes the logic fully auditable and reproducible from a small CSV file.

**Why genre weight 2.0, mood weight 1.0?** Experiment 1 showed that a weight of 3.0 for genre caused every result to be genre-locked, even when energy and mood were wrong. 2.0 lets mood and energy contribute meaningfully without being swamped.

**Why a separate `evaluator` module?** Separating scoring logic from evaluation logic means the recommender itself has no knowledge of what "correct" means — the evaluator is the testing layer. This mirrors how production ML systems separate inference from monitoring.

**Trade-offs:** Fixed weights are interpretable but brittle. A learned weighting system would perform better on edge cases but lose the ability to explain exactly why a song ranked where it did.

---

## Experiments

**Experiment 1 — Genre weight too dominant.**
Starting with a genre weight of 3.0 caused nearly every result for a pop user to be a pop song, even when the energy and mood were completely wrong. Dropping it to 2.0 let mood and energy contribute meaningfully.

**Experiment 2 — Removing the mood check.**
Commenting out the mood bonus caused the "Chill Lofi" profile to surface "Focus Flow" above "Midnight Coding" because their energies were closer. This showed that mood is a real differentiator between lofi subgenres.

**Experiment 3 — Doubling energy weight.**
Replacing `1.0 - energy_gap` with `2.0 - 2*energy_gap` made the Deep Rock profile recommend "Gym Hero" (pop) at position 2 over "Thunder Core" (metal) — energy alone was overriding genre. Kept the original single-unit scale.

**Experiment 4 — Adversarial profile (conflicting prefs).**
Testing `genre: lofi, mood: intense, energy: 0.9` produced strange results: lofi songs scored genre points but lost energy points; intense non-lofi songs won on energy but not genre. The system couldn't serve this user well, exposing a real gap.

---

## Testing Summary

3 out of 3 profiles **PASSED** the evaluation check. The top-ranked song matched the expected result for each profile.

| Profile | Top Result | Avg Confidence | Result |
|---|---|---|---|
| High-Energy Pop | Sunrise City | 0.51 | PASS |
| Chill Lofi | Library Rain | 0.72 | PASS |
| Deep Intense Rock | Storm Runner | 0.44 | PASS |

**Overall avg confidence: 0.56.** The Chill Lofi profile scored highest because multiple catalog songs matched all four attributes simultaneously. The Deep Intense Rock profile scored lowest (0.44 avg) because only one rock song exists in the catalog — positions 2–5 were filled by high-energy songs from other genres, which earn partial points but no genre bonus. The adversarial test (lofi + intense + high energy) cannot pass: no catalog song scores well on both genre and energy for that combination, which is an expected and documented failure mode.

---

## Limitations and Risks

- The catalog only has 18 songs — real systems have millions, so genre diversity is artificially constrained here.
- Genre is a fixed string label; "indie pop" and "pop" are treated as completely different even though they overlap.
- The system has no memory of what a user has already heard, so it will keep recommending the same top song forever.
- Acoustic preference only applies as a binary bonus; there is no penalty for non-acoustic songs when the user wants acoustic.
- Users with niche genres (like bossa nova or classical) get almost no genre-match points because the catalog has only one song in each.

---

## Reflection

See [model_card.md](model_card.md) for a full breakdown of how the model works, its known biases, AI collaboration notes, and ideas for improvement.

Building this recommender made one thing immediately clear: simple rules create predictable but rigid behavior. A real Spotify recommendation feels fluid because it blends hundreds of features and learns from billions of interactions. This simulation uses four features and fixed weights, which makes it transparent but also brittle — one song can dominate a niche genre. The bias toward genre (2.0 points) over mood (1.0 point) reflects a deliberate design choice, but it means a user who mainly cares about mood will get genre-heavy results anyway. Real AI systems face the same tradeoff at enormous scale, and the fact that even a toy system produces "filter bubbles" after just a few tests shows how quickly these patterns emerge.

---

## Portfolio Note

This project demonstrates that I can build an end-to-end AI system with transparent decision-making, structured evaluation, and documented trade-offs — not just a script that produces output. The evaluation layer, confidence scoring, and adversarial testing show that I think about reliability as a first-class concern, not an afterthought.
