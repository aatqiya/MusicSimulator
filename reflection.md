# Reflection

## Profile Comparisons

**High-Energy Pop vs. Chill Lofi**

These two profiles produced almost completely non-overlapping results, which makes sense. The pop user got high-energy tracks with happy moods; the lofi user got slow, acoustic, low-energy tracks. The only feature that could theoretically bridge them — mood (both can be "happy" or "relaxed") — was never close enough to overcome the genre and energy gap. This confirms that when genre and energy both diverge, the system correctly sends users in opposite directions.

**Chill Lofi vs. Deep Intense Rock**

Both of these profiles favor a specific genre, but the lofi profile had a richer result set because there were more lofi songs in the catalog. The rock profile's top result was obvious (Storm Runner), but positions 2–5 were filled by songs from completely different genres. Comparing these two outputs highlighted how catalog size per genre directly determines recommendation quality — lofi users got meaningful variety, rock users got one real match and four energy-based fallbacks.

**High-Energy Pop vs. Deep Intense Rock**

Both profiles target high energy (0.85 and 0.92 respectively), so they shared some songs in their lower-ranked results — Storm Runner appeared in the pop list and Sunrise City appeared in the rock list, each earning energy-similarity points despite genre mismatches. This showed that when genre points are maxed out for the top result, energy becomes the main differentiator for the rest of the list. A pop user and a rock user targeting similar energy levels will overlap more than expected, which is a real limitation of the current weighting scheme.

---

## What I Learned

The biggest takeaway was how much the choice of weights shapes the character of a recommender without the user knowing it. Giving genre a 2.0 weight vs. 1.5 does not sound like a big deal, but it changes which songs appear in positions 3–5 of nearly every profile's output. Real recommendation systems make thousands of decisions like this, and the users never see them — they just experience the output and form opinions about whether the app "gets" their taste.

I also learned that transparency is genuinely hard to scale. Showing "genre match (+2.0); mood match (+1.0)" is useful for a toy system, but at Spotify's scale, the model has hundreds of features and those explanations would mean nothing to most users. There is a real tension between building systems that are explainable and building systems that are accurate.

The part that changed how I think about music apps most was the filter bubble experiment. Once I saw that a pop user never got shown a jazz or classical recommendation even when the energy and mood were perfect, I started thinking differently about every playlist Spotify has ever made for me. The algorithm is not surfacing what is best — it is surfacing what is closest to what I have already told it I like, and those are not the same thing.
