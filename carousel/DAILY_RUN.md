# Daily carousel run (instructions for a Claude session)

Publish ONE pre-made carousel to @addzify62026, unless something was posted in the last 20 hours.

1. Skip check: list the last 5 posts (Composio INSTAGRAM_GET_IG_USER_MEDIA, account instagram_parto-amende). Any post in the last 20 h → skip.
2. Pick: first spec in `queue.json` whose slug is not in `posted.json` (also check its caption's first line isn't already live).
3. Slides: `posts/<slug>/slide_NN.jpg`, served from `https://raw.githubusercontent.com/tanishq286/addzify-resources/<commit-sha>/carousel/posts/<slug>/slide_NN.jpg`.
4. Check publishing quota → create one child container per slide (is_carousel_item) → carousel container with the spec's caption → publish → get permalink.
5. Append `{slug, media_id, permalink, posted_at}` to `posted.json`.
6. Mondays: weekly report (followers, 7-day reach/views/profile visits/interactions, best and worst post). Only API numbers, never estimates.

Never like, follow, comment or DM. On a failed step retry once, then stop and report — never publish a partial or duplicate carousel.
When `queue.json` is used up, write new specs following `STYLE.md`, render with `make_carousel.py`, and commit the slides before posting.
