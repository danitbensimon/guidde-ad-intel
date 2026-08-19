# Competitor Ad Intelligence — Run Report
_Generated 2026-08-18 19:00 UTC_

## 1. What ran
Source: public **Meta Ad Library** via Apify (`curious_coder/facebook-ads-library-scraper`, no login), by Page ID per brand. Both **active** ads (scored) and **inactive** ads (message back-history) are pulled.

| Brand | Pulled | Active | Inactive (history) | Retgt excl | Non-alt excl |
|---|--:|--:|--:|--:|--:|
| Scribe | 535 | 35 | 482 | 0 | 18 |
| Camtasia | 320 | 7 | 34 | 0 | 279 |
| Loom | 790 | 10 | 13 | 10 | 66 |
| WalkMe | 761 | 255 | 380 | 0 | 126 |

**2406 pulled → 307 active scored → 36 distinct creatives**, split by funnel stage: MOFU 30 (product / how-it-works) · TOFU 6 (awareness / lead-gen).

## 2. How it was scored
Three gates, then two stages, run separately inside each funnel stage.

**Gates:** active today · not UTM-retargeting · sells a Guidde use case.

**Stage 1 — within-brand champion:** `0.6·persistence + 0.4·longevity`. Persistence = **distinct months the message was re-launched** (from active + inactive versions grouped by content similarity, threshold 0.55), so a blast of many simultaneous copies does not count as staying power. Longevity = days since the message's earliest version. Both within-brand.

**Stage 2 — cross-brand, two signals combined** `0.5·repetition + 0.5·relevance`:
- **Repetition** = how validated the message is across the 4 competitors (the brief's "creative repetition across competitors"): the more rivals share the champion's angles, the higher it scores. Built from the angle map in §4a.
- **Relevance** = how central the message is to **Guidde's own job** (create step-by-step video documentation to onboard / train / support), tier ÷ 3: 3 = core (the guide / doc / SOP itself), 2 = adjacent (onboarding, training, support, demos), 1 = peripheral (AI-adoption, async video).

_Both terms matter: repetition is the market's vote (the named criterion), relevance is closeness to Guidde and **breaks the tie repetition can't**, the finalists have identical angle-coverage profiles (one mid- + one high-coverage angle each), so any function of coverage ties them; only relevance separates them on merit. Remaining ties fall back to repetition, then the Stage-1 champion score._

## 3. Stage 1 — each brand's field (within-brand)
Every brand's active, Guidde-relevant ads compete **only against their own brand** here, so a brand that simply runs more ads can't crowd the board. The top ad per brand in each funnel stage becomes that brand's **champion (⭐)** and advances to Stage 2. Score = `0.6·persistence + 0.4·longevity`, both normalized within the brand (so every brand's best = 1.0).


**Scribe** — 18 distinct active creatives
|  | Ad | Stage | Re-issue mo | True days | Persist | Longev | Champion score | Link |
|--|---|--|--:|--:|--:|--:|--:|---|
| ⭐ | 'The part nobody puts on the job description:' | MOFU | 2 | 62 | 1.0 | 1.0 | **1.0** | [ad](https://www.facebook.com/ads/library/?id=1737809570795386) |
|  | 'Turn Any Process Into a Step-by-Step Guide' | MOFU | 2 | 24 | 1.0 | 0.376 | **0.7504** | [ad](https://www.facebook.com/ads/library/?id=1072538672370396) |
|  | 'Clear steps. Fewer questions.' | MOFU | 2 | 22 | 1.0 | 0.36 | **0.744** | [ad](https://www.facebook.com/ads/library/?id=1521004986492791) |
|  | 'The SOP that used to take hours. Now takes m' | MOFU | 1 | 16 | 0.5 | 0.248 | **0.3992** | [ad](https://www.facebook.com/ads/library/?id=28812767481658401) |
|  | '❌ 4 hours making an SOP ❌ A call to explain ' | MOFU | 1 | 8 | 0.5 | 0.136 | **0.3544** | [ad](https://www.facebook.com/ads/library/?id=1587377913081253) |
|  | 'Cut New Hire Ramp Time by 40%' | MOFU | 1 | 8 | 0.5 | 0.136 | **0.3544** | [ad](https://www.facebook.com/ads/library/?id=1834837897315178) |
| | _+12 more (all scored below the champion)_ | | | | | | | |

**Camtasia** — 6 distinct active creatives
|  | Ad | Stage | Re-issue mo | True days | Persist | Longev | Champion score | Link |
|--|---|--|--:|--:|--:|--:|--:|---|
| ⭐ | 'Trusted by Teams who Train' | MOFU | 2 | 70 | 1.0 | 0.986 | **0.9944** | [ad](https://www.facebook.com/ads/library/?id=1555644152851009) |
|  | 'AI Voice Generation For Training Videos' | MOFU | 1 | 72 | 0.5 | 1.0 | **0.7** | [ad](https://www.facebook.com/ads/library/?id=1353237916728386) |
|  | 'Training Mag Choice Awards Winner 2025\u200b' | MOFU | 1 | 72 | 0.5 | 1.0 | **0.7** | [ad](https://www.facebook.com/ads/library/?id=27137286055935763) |
|  | 'Translate Training Videos\u200b with Camtasia\u200b' | MOFU | 1 | 70 | 0.5 | 0.986 | **0.6944** | [ad](https://www.facebook.com/ads/library/?id=2576669752783892) |
|  | 'Say it with a video' | MOFU | 1 | 50 | 0.5 | 0.706 | **0.5824** | [ad](https://www.facebook.com/ads/library/?id=1373501117978409) |
|  | 'Easy training video creation' | MOFU | 1 | 12 | 0.5 | 0.175 | **0.37** | [ad](https://www.facebook.com/ads/library/?id=1675484953890583) |

**Loom** — 7 distinct active creatives
|  | Ad | Stage | Re-issue mo | True days | Persist | Longev | Champion score | Link |
|--|---|--|--:|--:|--:|--:|--:|---|
| ⭐ | 'Is your team stuck accomodating schedules an' | MOFU | 3 | 260 | 1.0 | 1.0 | **1.0** | [ad](https://www.facebook.com/ads/library/?id=1340695467952174) |
|  | 'Video that moves work forward' | MOFU | 1 | 128 | 0.333 | 0.491 | **0.3962** | [ad](https://www.facebook.com/ads/library/?id=2199486914156206) |
|  | 'Build and ship quicker with AI workflows' | MOFU | 1 | 128 | 0.333 | 0.491 | **0.3962** | [ad](https://www.facebook.com/ads/library/?id=1454359272564729) |
|  | 'Share presentations, feedback, updates, and ' | MOFU | 1 | 128 | 0.333 | 0.491 | **0.3962** | [ad](https://www.facebook.com/ads/library/?id=1472348837768432) |
|  | 'Add the power of Loom to your Atlassian work' | MOFU | 1 | 82 | 0.333 | 0.318 | **0.327** | [ad](https://www.facebook.com/ads/library/?id=1005832245724475) |
|  | 'Explain ideas, give feedback, and share upda' | MOFU | 1 | 82 | 0.333 | 0.318 | **0.327** | [ad](https://www.facebook.com/ads/library/?id=1025676566662228) |
| | _+1 more (all scored below the champion)_ | | | | | | | |

**WalkMe** — 5 distinct active creatives
|  | Ad | Stage | Re-issue mo | True days | Persist | Longev | Champion score | Link |
|--|---|--|--:|--:|--:|--:|--:|---|
| ⭐ | 'AI was supposed to reduce friction. Instead,' ⚑ | TOFU | 4 | 84 | 1.0 | 0.719 | **0.8876** | [ad](https://www.facebook.com/ads/library/?id=1093770439981628) |
|  | '37% of workers skip AI entirely — not becaus' | TOFU | 3 | 118 | 0.75 | 1.0 | **0.85** | [ad](https://www.facebook.com/ads/library/?id=1323439673253335) |
|  | 'Your employees spend 7.9 hours a week managi' | TOFU | 3 | 118 | 0.75 | 1.0 | **0.85** | [ad](https://www.facebook.com/ads/library/?id=1311404944499262) |
|  | 'Only 46% of workers get guidance while actua' | TOFU | 3 | 118 | 0.75 | 1.0 | **0.85** | [ad](https://www.facebook.com/ads/library/?id=1485315262781094) |
|  | 'Organizations getting execution right are pu' | TOFU | 1 | 70 | 0.25 | 0.591 | **0.3864** | [ad](https://www.facebook.com/ads/library/?id=1762440595135113) |

_⚑ = Meta flags the ad low-impression. Full field in `data/ranked.csv`._

## 4. Stage 2 — the champions compete, by funnel stage
The Stage-1 champions now compete across brands, in two funnel lanes so a lead-gen report (TOFU) never runs head-to-head with a product ad (MOFU). Score = `0.5·repetition + 0.5·relevance` (both defined in §2).

### 4a. The repetition signal — cross-competitor angle map
How many of the 4 competitors run each messaging angle. An ad's **repetition** score sums the competitor-coverage of the angles it uses, so a message the whole market echoes scores higher. This table is a **scoring input**, it feeds the repetition term.

| Angle | Competitors | Coverage |
|---|---|:--:|
| time_saved | Camtasia, Loom, Scribe, WalkMe | 4/4 |
| stat_proof | Camtasia, Scribe, WalkMe | 3/4 |
| problem_hook | Loom, Scribe, WalkMe | 3/4 |
| ai_powered | Camtasia, Loom, WalkMe | 3/4 |
| onboarding_training | Camtasia, Scribe | 2/4 |
| documentation_sop | Loom, Scribe | 2/4 |
| async_vs_meetings | Loom, Scribe | 2/4 |
| tool_overload | Loom, WalkMe | 2/4 |
| repetitive_questions | Scribe | 1/4 |

### 4b. The champions ranked
**The primary result Guidde should rebuild is the Product / how-it-works winner.** Repetition is equal across the MOFU finalists (identical coverage profiles), so relevance decides, exactly the tie-break repetition alone can't make.


#### MOFU — Product / how-it-works  ⭐ primary
| # | Brand | Champion ad | Repetition | Guidde-fit (tier · keyword) | **Stage 2 final** | Ad |
|--:|---|---|--:|--:|--:|---|
| 1 | Scribe | 'The part nobody puts on the job description:' | 0.417 | 1.0 · t3 · `guide` | **0.7085** | [ad](https://www.facebook.com/ads/library/?id=1737809570795386) |
| 2 | Camtasia | 'Trusted by Teams who Train' | 0.417 | 0.667 · t2 · `train` | **0.542** | [ad](https://www.facebook.com/ads/library/?id=1555644152851009) |
| 3 | Loom | 'Is your team stuck accomodating schedules an' | 0.417 | 0.333 · t1 · `record and share` | **0.375** | [ad](https://www.facebook.com/ads/library/?id=1340695467952174) |

_Why each MOFU champion scored what it did:_
- **Scribe** 'The part nobody puts on the job descript' → **Stage 1** `0.6×persist(1.0) + 0.4×longev(1.0) = 1.0` (2 distinct months, 62 days running). **Stage 2** `0.5×rep(0.417) + 0.5×rel(1.0) = 0.7085` — repetition from angle `problem_hook` (3/4 rivals share it); relevance tier 3 (core Guidde use case) set by the word `guide`.
- **Camtasia** 'Trusted by Teams who Train' → **Stage 1** `0.6×persist(1.0) + 0.4×longev(0.986) = 0.9944` (2 distinct months, 70 days running). **Stage 2** `0.5×rep(0.417) + 0.5×rel(0.667) = 0.542` — repetition from angle `stat_proof` (3/4 rivals share it); relevance tier 2 (onboard / train / support) set by the word `train`.
- **Loom** 'Is your team stuck accomodating schedule' → **Stage 1** `0.6×persist(1.0) + 0.4×longev(1.0) = 1.0` (3 distinct months, 260 days running). **Stage 2** `0.5×rep(0.417) + 0.5×rel(0.333) = 0.375` — repetition from angle `problem_hook` (3/4 rivals share it); relevance tier 1 (adoption / async (peripheral)) set by the word `record and share`.

#### TOFU — Awareness / lead-gen
| # | Brand | Champion ad | Repetition | Guidde-fit (tier · keyword) | **Stage 2 final** | Ad |
|--:|---|---|--:|--:|--:|---|
| 1 | WalkMe | 'AI was supposed to reduce friction. Instead,' ⚑low-impr | 0.5 | 0.333 · t1 · `digital adoption` | **0.4165** | [ad](https://www.facebook.com/ads/library/?id=1093770439981628) |
| 2 | Loom | 'Learn how Loom helps marketers eliminate app' | 0.5 | 0.0 · t0 · `` | **0.25** | [ad](https://www.facebook.com/ads/library/?id=1303392765004693) |

_Why each TOFU champion scored what it did:_
- **WalkMe** 'AI was supposed to reduce friction. Inst' → **Stage 1** `0.6×persist(1.0) + 0.4×longev(0.719) = 0.8876` (4 distinct months, 84 days running). **Stage 2** `0.5×rep(0.5) + 0.5×rel(0.333) = 0.4165` — repetition from angle `ai_powered` (3/4 rivals share it); relevance tier 1 (adoption / async (peripheral)) set by the word `digital adoption`.
- **Loom** 'Learn how Loom helps marketers eliminate' → **Stage 1** `0.6×persist(0.333) + 0.4×longev(0.16) = 0.2638` (1 distinct months, 42 days running). **Stage 2** `0.5×rep(0.5) + 0.5×rel(0.0) = 0.25` — repetition from angle `time_saved` (4/4 rivals share it); relevance tier 0 (unclassified) set by the word ``.

_Table links browse the brand's page narrowed to the ad's copy; the **exact-ad** Library-ID link (`?id=`) is in §5. ⚑ = Meta flags low-impression._

## 5. Primary winner (Product / how-it-works)
**Scribe — "The part nobody puts on the job description: spending hours writing up everything you do i"**
**→ [View the exact winning ad](https://www.facebook.com/ads/library/?id=1737809570795386)** (opens the single winning ad by Meta Library ID 1737809570795386) · [browse all Scribe ads](https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&view_all_page_id=110376044484488&search_type=page&q=The%20part%20nobody%20puts%20on%20the)

**How this ad's score is built** — Stage 1 proves it, Stage 2 ranks it:
- **Stage 1 (within Scribe):** `champion_score = 0.6×persistence(1.0) + 0.4×longevity(1.0) = 1.0`. It re-issued across 2 distinct months (5 versions), running 62 days, Scribe's most-proven ad.
- **Stage 2 (across the champions):** `final = 0.5×repetition(0.417) + 0.5×relevance(1.0) = 0.7085`.
    - *Repetition:* its strongest angle `problem_hook` is run by 3/4 competitors (from §4a).
    - *Relevance:* **tier 3 (core Guidde use case)**, matches Guidde's core on `guide`, the ad literally "builds a guide automatically" from a captured workflow, Guidde's exact job.
- **Full ad, not just the video:** headline "The SOP that used to take hours. Now takes minutes." · description "Document and share how work actually happens." · CTA "Learn more".
- **Format:** VIDEO · funnel stage MOFU · funnel prospecting·inferred.

## 6. Notable & honest limits
- **Funnel split fixes the apples-to-oranges problem:** WalkMe's "download the report" ad is now the TOFU winner in its own lane, not beating product ads on generic AI/stat angles.
- **Meta's own performance signal:** some ads carry an impression flag (`<100` = low-impression); WalkMe's report copies are flagged low, confirming they underperform. The signal is sparse (Scribe shows none), so it flags losers rather than ranking the field.
- **Clustering is a TF-IDF heuristic:** it can mis-group at the margins; the threshold (0.55) is tuned so different campaigns don't merge. True embeddings are the roadmap fix.
- **DCO ads can't be deep-linked**, and a single snapshot ages, so re-run before acting.
