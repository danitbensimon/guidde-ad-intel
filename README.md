# Competitor Facebook Ad Intelligence to Guidde Creative Brief

One pipeline, two halves. It scrapes competitors' Facebook ads, scores them to find the single best ad on a defended definition of "best," then rebuilds that winner as a Guidde creative brief and a shot-by-shot storyboard with generated images.

**Real run output (not a hypothetical):**
- **Winning ad:** Scribe, "The part nobody puts on the job description" — a car-POV UGC video with documentation-pain copy ([exact ad, by Meta Library ID](https://www.facebook.com/ads/library/?id=1737809570795386))
- **Winner teardown:** [`output/01_winner_analysis.md`](output/01_winner_analysis.md)
- **Creative brief:** [`output/02_creative_brief.md`](output/02_creative_brief.md)
- **Storyboard + produced ad:** [storyboard with frames (rendered)](https://htmlpreview.github.io/?https://github.com/danitbensimon/guidde-ad-intel/blob/main/output/04_storyboard.html) and the [produced ad, with full ad copy (rendered)](https://htmlpreview.github.io/?https://github.com/danitbensimon/guidde-ad-intel/blob/main/output/demo_video.html)
- **Run report (auto-generated, full score math):** [`output/run_report.md`](output/run_report.md)

---

## 1. Data source: why Apify, not Meta's official API

Meta hides spend and performance, and its **official Ad Library API only returns political and social-issue ads**, so it cannot see commercial SaaS ads from Scribe, Loom, Camtasia, or WalkMe. Confirmed on Meta's own docs and independent scrapers (minimaxir's README states it plainly). So the official API is a dead end for this task.

The public Ad Library website does carry these commercial ads. We read it through the Apify actor `curious_coder/facebook-ads-library-scraper` (no login), collecting **by resolved Page ID** per brand. Cost is roughly **$1 per full run**.

One trap worth naming: connecting a Facebook account (via Composio or an OAuth "meta ads" tool) is the wrong move. That authenticates your own ad account; competitor intelligence lives in the public Ad Library, which needs no account at all.

## 2. Defining "best": three gates, then a two-stage score

Meta gives no spend or performance, so "best" is inferred. An ad must first clear three gates, then it is scored in two stages.

**Gates (pass/fail):**
- **Active today.** A paused ad tells us nothing about current performance.
- **Not retargeting.** UTM-confirmed retargeting ads are excluded (only Loom tags its links; those are warm-audience feature reminders, the wrong benchmark for a prospecting ad).
- **Is a Guidde alternative.** The copy must sell one of Guidde's own use cases (checked against guidde.com): creating guides, docs, SOPs, walkthroughs, onboarding, training, customer support, software rollout, product demos, AI adoption, or in-app guidance. This excludes adjacent products and, deliberately, async-messaging / meeting-replacement, which Guidde explicitly is not.

Ads are also split into two funnel lanes first, product / how-it-works (MOFU) and awareness / lead-gen (TOFU), so a "download the report" ad never competes head-to-head with a product ad. Each lane crowns its own winner; the one to rebuild is the product winner.

**Stage 1, each brand's champion (within-brand only):**
`champion = 0.6 persistence + 0.4 longevity`
Persistence = how many distinct *months* the brand re-launched this message, read from its active + inactive history, so a brand that keeps coming back to a message scores high while a one-off blast of many simultaneous copies does not. Longevity = days since the message's earliest version. Both are normalized inside the brand, so each brand is judged against its own ads, never against a rival that started earlier or spawns more variants.

**Stage 2, the champions compete (cross-brand):**
`final = 0.5 repetition + 0.5 relevance`
Repetition = how many of the four competitors also run the champion's angles (the brief's own criterion; a message rivals echo is validated). Relevance = how close the message sits to Guidde's own job, capturing a workflow into step-by-step video documentation, graded in tiers. Two signals, not one, because **repetition alone tied the three finalists** (identical angle coverage); relevance is what separated them on merit.

Why two stages: within-brand facts (a brand re-running its own ad) pick a brand's best ad; cross-brand facts (an angle rivals share, closeness to Guidde) pick which brand's best ad wins. Keeping them separate stops one brand's ad volume from dominating the result.

**The winner: Scribe, "The part nobody puts on the job description"** — a car-POV UGC video with documentation-pain copy (Meta Library ID 1737809570795386). It is Scribe's most-proven ad (champion 1.0: re-issued across 2 distinct months, 5 versions, running 62 days), it is market-validated (its problem-hook angle runs across 3 of the 4 competitors), and it sits dead-center on Guidde's core (relevance tier 3). Stage-2 final 0.71. Scribe is the competitor closest to Guidde, both turn a screen capture into step-by-step documentation, so the winning formula transfers almost one to one.

## 3. Scoping decisions (the judgment calls)

- **All four competitors, no up-front cut.** Any brand that fell out fell out because the data removed it (WalkMe runs almost no guide-creation ads; Loom advertises async communication, not guides), reported with counts.
- **DCO (dynamic) ads are eligible.** Guidde can run a dynamic ad too, and the real hook lives in the ad's cards, so excluding them would silently narrow the field.
- **All formats scored, then narrowed by relevance, not by guess.** The Guidde-alternative gate was widened from a narrow "guides only" definition to Guidde's full use-case set after checking guidde.com, so the field is scoped by what Guidde actually does rather than by an arbitrary boundary.
- **What I cut, and why I can defend it.** BOFU was folded into MOFU (a "Sign up" CTA doesn't make a product ad bottom-funnel); UTM-confirmed retargeting ads were gated out (wrong benchmark for a prospecting ad); and "tedious-calls" language from Scribe's own copy was left out of Guidde's ad once I checked guidde.com and saw Guidde doesn't position that way. Each cut is a boundary you can see in `config.py` and move.

## 4. The powerful idea: measure persistence across active AND inactive ads

The hardest problem in this data is **DCO version churn**. A dynamic creative is re-issued constantly as fresh versions, each with a new Library ID and a reset start date, so a single active-only snapshot sees one version's age, never the message's real staying power.

The fix is to **compare active ads against inactive ads of the same message.** Scrape `active_status=all` (not just active), group each ad with its re-issued versions by content similarity (TF-IDF, in `matching.py`), and measure:
- **true longevity** = days from the message's earliest version to now, and
- **persistence** = how many distinct calendar months the brand re-launched the message.

By that measure the winning Scribe ad reads as **5 versions across 2 distinct months, 62 days of true longevity**, rather than one short run, revealed preference for a message the brand keeps re-committing to. This turns DCO churn from a bug (misleading dates) into the persistence signal itself. It is the correct implementation of "new versions of the same ad."

To see it yourself: on any brand's Ad Library page, switch the "Active status" filter from **Active** to **All**. The inactive ads carry full start-to-end date ranges that reveal the message's real history.

## 5. Where it breaks (failure handling)

- **DCO longevity is fuzzy.** Per-version dates reset, so a single snapshot's "days running" understates a churning message (see section 4). Load-bearing check: the winner won on message, not longevity, so this does not change the result.
- **Per-ad deep links are inconsistent.** Meta only exposes some ads as a standalone `?id=<Library ID>` link. The winner does resolve exactly that way (verified), so the report links to it directly; for ads that don't, it falls back to the advertiser's page narrowed by the ad's copy. Links also need `&country=US`, or the Ad Library hides US-targeted ads from a non-US viewer.
- **Data freshness.** The scrape is a point-in-time snapshot. Fast-cycling advertisers like Scribe can churn a specific version out within days, so a re-run before acting is wise.
- **The Guidde-alternative and funnel classifiers are keyword heuristics.** They mislabel at the margins (a genuine guide ad occasionally reads as neutral). They are transparent and tunable, but they are not perfect; the error mode is missing a relevant ad, not inventing one.

## 6. External providers, credentials & cost

| Provider | Used for | Credential needed | Cost of a run |
|---|---|---|---|
| **Apify** (`curious_coder/facebook-ads-library-scraper`) | Part 1: scraping the public Meta Ad Library | `APIFY_TOKEN` in `.env` | ~$1 (4 brands, <1,000 ads) |
| **Higgsfield** (Soul 2.0 image, FLUX 3 video) | Part 2: generating the storyboard frames + the produced ad, driven from Claude | Higgsfield account (image ~0.12 credits each; video ~27.5 credits / 5s) | ~100 credits per ad (≈6 frames + one ~18-second clip) |
| **guidde.com** | Part 2: reading Guidde's real features for the brief | none (public site) | free |

The **scoring pipeline itself has no LLM/API cost** — it is deterministic Python. Only the scrape (Apify) and the optional creative generation (Higgsfield) cost money, and they are separable: Part 1 runs with just `APIFY_TOKEN`.

To reproduce from a clean machine you need: Python 3.9+, `pip install apify-client` (plus `pypdf` only if re-reading the brief PDF), and an `APIFY_TOKEN`. Part 2's creative generation additionally needs a Higgsfield account; the analysis (Parts 1) does not.

## 7. What breaks at 10x volume

At ~10x the ads (more brands, deeper history), two things bind first:

1. **The Apify scrape** becomes the wall-clock and cost bottleneck. Fix: move collection to a queue, run brands in parallel, and cache by `ad_archive_id` so re-runs only fetch deltas instead of re-scraping the full history.
2. **The clustering is O(n²)** — `matching.py` does pairwise TF-IDF cosine within each brand. At thousands of ads per brand that quadratic blows up. Fix: replace it with embedding + approximate nearest-neighbour (vector) search, which also upgrades the tagging from keywords to meaning.

Everything else (gates, scoring, reporting) is linear and streams fine. The scoring is stateless per ad, so it shards trivially. The real limit is upstream rate limits and the clustering, not the scorer.

## 8. What I would build next

With more time, in priority order:

1. **Track across repeated runs.** Save every run and notice when a message comes back, so we can measure true staying power over time and spot when a competitor changes its messaging.
2. **Match on meaning, not keywords.** Replace the keyword tagging (both the Guidde-alternative filter and the angle tags) with embedding-based matching, so borderline ads stop getting mislabeled — this is also the 10x clustering fix.
3. **Wire the winner straight into Part 2** so a single run goes scrape → score → brief → storyboard end to end on a schedule.
4. **Drop in a real Guidde metric** where the brief currently uses a placeholder proof number ("hours saved").

_Already done since the first draft:_ persistence now measures distinct re-issue months across active **and** inactive history (not copies-today); the winner links by its exact Meta Library ID; and the storyboard is produced as a real UGC video, not just frames.

## 9. Run it

```bash
cp .env.example .env          # add your APIFY_TOKEN
python3 src/collect.py        # scrape the four brands by page id -> data/raw/
python3 src/rank.py           # gates + two-stage scoring -> data/ranked.* , winner.json
python3 src/report.py         # human-readable run report -> output/run_report.md
```

Every scoring decision, gate, and weight lives in `src/config.py`, in one auditable place.

## 10. What I deliberately skipped

Per the brief: no auth, UI, tests, CI/CD, or productionizing. The pipeline is a scored analysis plus a real creative output, not a deployable service.

## 11. Repo map

```
src/config.py    every scoping decision, gate, and weight, documented
src/collect.py   builds the Ad Library URL per brand, runs the Apify actor
src/angles.py    angle tagging + Guidde-alternative gate + graded Guidde-relevance
src/matching.py  TF-IDF cosine clustering of a message across active+inactive versions
src/rank.py      three gates, two-stage scoring, funnel segmentation, winner selection
src/report.py    generates output/run_report.md
src/gallery.py   generates output/champions_report.html (winners board)
src/storyboard_html.py  generates output/04_storyboard.html (Part 2 storyboard)
output/          01 winner analysis · 02 brief · 03/04 storyboard + frames · run report ·
                 champions_report.html · ARCHITECTURE.md · DEMO_SCRIPT.md · storyboard_ai/ (video + frames)
data/            raw scrapes · ranked.csv/json · winner.json · run_meta.json · champion_shots/
```

See `output/ARCHITECTURE.md` for the flow diagram and `output/DEMO_SCRIPT.md` for the demo walkthrough.
