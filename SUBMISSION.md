# Submission index — Competitor Ad Intelligence → Guidde Creative

One pipeline, two halves: it finds the single best competitor Facebook ad on a defended definition of "best," then rebuilds that winner as a Guidde creative brief, storyboard, and a produced ad. Everything below is from a **real run** against Scribe, Loom, Camtasia and WalkMe.

**The winner:** Scribe, *"The part nobody puts on the job description"* — a car-POV UGC video with documentation-pain copy · [exact ad on Meta (Library ID 1737809570795386)](https://www.facebook.com/ads/library/?id=1737809570795386)

---

## Start here
- **README** — the full write-up: data source, how "best" is defined, scoping decisions, cost, failure modes, and what breaks at 10x → [`README.md`](README.md)
- **How it works (diagram)** — the pipeline in six plain steps → [`output/ARCHITECTURE.md`](output/ARCHITECTURE.md)
- **Demo walkthrough** (recorded in Guidde) → https://app.guidde.com/share/playbooks/ibuuuyDSoVoJFcdjhn2usm?origin=cKI57TOVvpYojjMkKZKKJjSlQFo1&mode=videoAndDoc
- **Demo script** — [`output/DEMO_SCRIPT_HE.md`](output/DEMO_SCRIPT_HE.md)

## Part 1 — finding the winning ad
- **Run report** — every scoring stage, the gates, Round 1 (within-brand) and Round 2 (cross-brand), and why the winner won → [`output/run_report.md`](output/run_report.md)
- **Winners board** (designed, with the real ad frames) → [rendered](https://htmlpreview.github.io/?https://github.com/danitbensimon/guidde-ad-intel/blob/main/output/champions_report.html)
- **Per-ad extraction** — the brief's five fields (hook, angle/messaging, format, CTA, how long running) for every ad, one row each → `data/ranked.csv`
- **Code** — the pipeline → [`src/`](src/) (config, collect, angles, matching, rank, report, gallery)

## Part 2 — the teardown and the Guidde ad
- **Teardown** of the winning ad (hook, angle, structure, visual style, why it works) → [`output/01_winner_analysis.md`](output/01_winner_analysis.md)
- **Creative brief** → [`output/02_creative_brief.md`](output/02_creative_brief.md)
- **Storyboard** — text: [`output/03_storyboard.md`](output/03_storyboard.md) · [designed with frames (rendered)](https://htmlpreview.github.io/?https://github.com/danitbensimon/guidde-ad-intel/blob/main/output/04_storyboard.html)
- **The produced Guidde ad** — full ad copy (primary text, headline, description, CTA) plus the video → [watch it (rendered)](https://htmlpreview.github.io/?https://github.com/danitbensimon/guidde-ad-intel/blob/main/output/demo_video.html) · [video file](output/storyboard_ai/guidde_ad_final.mp4)

---

## How it maps to the brief
- **Extract per ad** (hook · angle/messaging · format · CTA · how long running): all five, every ad, in `data/ranked.csv`.
- **Narrow with a reason:** kept all four competitors (a brand only drops if the data removes it), focused on prospecting (not retargeting), and scored product ads (MOFU) separately from lead-gen (TOFU). Each choice is documented in README §2–§3 and lives in `src/config.py`.
- **The single winning ad:** identified, scored, and linked by its exact Meta Library ID.
- **Analysis → brief → storyboard with images:** Part 2 above, all built around the real winner.
- **Real output from a real run:** every number and artifact is from an actual scrape and score, not a hypothetical.
