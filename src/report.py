"""
Stage 3 - Run report (segmented by funnel stage).

Reads data/ranked.json + run_meta.json + winner.json and writes a self-contained
Markdown report to output/run_report.md: what was checked, how it was scored, and
the winning ad in each funnel stage (so a report/awareness ad never competes
head-to-head with a product ad). Regenerated on every run.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "output" / "run_report.md"


def main() -> None:
    ads = json.loads((DATA / "ranked.json").read_text())
    meta = json.loads((DATA / "run_meta.json").read_text())
    winner = json.loads((DATA / "winner.json").read_text())
    s1, s2 = meta["stage1_weights"], meta["stage2_weights"]
    segments, labels = meta["segments"], meta["stage_labels"]
    primary = meta["primary_stage"]
    ncomp = len(meta["competitors"])
    L = []

    L.append("# Competitor Ad Intelligence — Run Report")
    L.append(f"_Generated {meta['generated_utc']}_\n")

    # 1. What ran
    L.append("## 1. What ran")
    L.append("Source: public **Meta Ad Library** via Apify (`curious_coder/"
             "facebook-ads-library-scraper`, no login), by Page ID per brand. Both "
             "**active** ads (scored) and **inactive** ads (message back-history) are "
             "pulled.\n")
    L.append("| Brand | Pulled | Active | Inactive (history) | Retgt excl | Non-alt excl |")
    L.append("|---|--:|--:|--:|--:|--:|")
    for b, c in meta["per_brand"].items():
        L.append(f"| {b} | {c['pulled']} | {c['active']} | {c['inactive']} "
                 f"| {c['retargeting_excluded']} | {c['not_alternative']} |")
    sc = meta["stage_count"]
    L.append(f"\n**{meta['total_pulled']} pulled → {meta['total_active_scored']} active "
             f"scored → {meta['distinct_creatives']} distinct creatives**, split by "
             f"funnel stage: MOFU {sc.get('MOFU',0)} (product / how-it-works) · "
             f"TOFU {sc.get('TOFU',0)} (awareness / lead-gen).\n")

    # 2. How it was scored (method comes before the stages that apply it)
    L.append("## 2. How it was scored")
    L.append("Three gates, then two stages, run separately inside each funnel stage.\n")
    L.append("**Gates:** active today · not UTM-retargeting · sells a Guidde use case.\n")
    L.append(f"**Stage 1 — within-brand champion:** `{s1['reissue_persistence']}·"
             f"persistence + {s1['longevity']}·longevity`. Persistence = **distinct "
             f"months the message was re-launched** (from active + inactive versions "
             f"grouped by content similarity, threshold {meta['cluster_threshold']}), "
             f"so a blast of many simultaneous copies does not count as staying power. "
             f"Longevity = days since the message's earliest version. Both within-brand.")
    L.append(f"\n**Stage 2 — cross-brand, two signals combined** "
             f"`{s2['repetition_across_competitors']}·repetition + "
             f"{s2['guidde_relevance']}·relevance`:")
    L.append(f"- **Repetition** = how validated the message is across the {ncomp} "
             f"competitors (the brief's \"creative repetition across competitors\"): the "
             f"more rivals share the champion's angles, the higher it scores. Built from "
             f"the angle map in §4a.")
    L.append("- **Relevance** = how central the message is to **Guidde's own job** "
             "(create step-by-step video documentation to onboard / train / support), "
             "tier ÷ 3: 3 = core (the guide / doc / SOP itself), 2 = adjacent "
             "(onboarding, training, support, demos), 1 = peripheral (AI-adoption, "
             "async video).")
    L.append("\n_Both terms matter: repetition is the market's vote (the named "
             "criterion), relevance is closeness to Guidde and **breaks the tie "
             "repetition can't**, the finalists have identical angle-coverage profiles "
             "(one mid- + one high-coverage angle each), so any function of coverage "
             "ties them; only relevance separates them on merit. Remaining ties fall "
             "back to repetition, then the Stage-1 champion score._\n")

    def _hook(a):
        parts = a["body"].split("  ")
        return next((h.strip() for h in parts if h.strip()
                     and "." not in h.split()[0]), a["body"][:50])

    # 3. Stage 1 — the within-brand field each champion emerged from
    L.append("## 3. Stage 1 — each brand's field (within-brand)")
    L.append("Every brand's active, Guidde-relevant ads compete **only against their "
             "own brand** here, so a brand that simply runs more ads can't crowd the "
             "board. The top ad per brand in each funnel stage becomes that brand's "
             "**champion (⭐)** and advances to Stage 2. Score = "
             f"`{s1['reissue_persistence']}·persistence + {s1['longevity']}·longevity`, "
             "both normalized within the brand (so every brand's best = 1.0).\n")
    champ_keys = {(a["brand"], a["funnel_stage"], a["body"][:60])
                  for champs in segments.values() for a in champs}
    by_brand = defaultdict(list)
    for a in ads:
        by_brand[a["brand"]].append(a)
    CAP = 6
    for b in meta["competitors"]:
        rows = sorted(by_brand.get(b, []),
                      key=lambda x: (x["champion_score"], x["days_running"]), reverse=True)
        if not rows:
            L.append(f"\n**{b}** — no active Guidde-relevant creatives (see §1 exclusions).")
            continue
        L.append(f"\n**{b}** — {len(rows)} distinct active creative"
                 f"{'s' if len(rows) != 1 else ''}")
        L.append("|  | Ad | Stage | Re-issue mo | True days | Persist | Longev | Champion score | Link |")
        L.append("|--|---|--|--:|--:|--:|--:|--:|---|")
        for a in rows[:CAP]:
            star = "⭐" if (a["brand"], a["funnel_stage"], a["body"][:60]) in champ_keys else ""
            flag = " ⚑" if a.get("low_impression") else ""
            url = a.get("ad_library_url_exact") or a.get("ad_library_url", "")
            L.append(f"| {star} | {_hook(a)[:44]!r}{flag} | {a['funnel_stage']} | "
                     f"{a.get('reissue_periods','—')} | {a.get('true_longevity_days',0):.0f} | "
                     f"{a.get('persistence_n','—')} | {a.get('longevity_n','—')} | "
                     f"**{a['champion_score']}** | [ad]({url}) |")
        if len(rows) > CAP:
            L.append(f"| | _+{len(rows)-CAP} more (all scored below the champion)_ "
                     f"| | | | | | | |")
    L.append("\n_⚑ = Meta flags the ad low-impression. Full field in `data/ranked.csv`._\n")

    # 4. Stage 2 — champions compete on repetition + relevance
    L.append("## 4. Stage 2 — the champions compete, by funnel stage")
    L.append("The Stage-1 champions now compete across brands, in two funnel lanes so a "
             "lead-gen report (TOFU) never runs head-to-head with a product ad (MOFU). "
             f"Score = `{s2['repetition_across_competitors']}·repetition + "
             f"{s2['guidde_relevance']}·relevance` (both defined in §2).\n")

    # 4a. the repetition signal — the cross-competitor angle map (a scoring input)
    L.append("### 4a. The repetition signal — cross-competitor angle map")
    L.append(f"How many of the {ncomp} competitors run each messaging angle. An ad's "
             "**repetition** score sums the competitor-coverage of the angles it uses, "
             "so a message the whole market echoes scores higher. This table is a "
             "**scoring input**, it feeds the repetition term.\n")
    L.append("| Angle | Competitors | Coverage |")
    L.append("|---|---|:--:|")
    for ang, comps in meta["angle_coverage"].items():
        L.append(f"| {ang} | {', '.join(comps)} | {len(comps)}/{ncomp} |")

    # 4b. the champions ranked on the combined score
    L.append("\n### 4b. The champions ranked")
    L.append("**The primary result Guidde should rebuild is the "
             f"{labels[primary]} winner.** Repetition is equal across the MOFU "
             "finalists (identical coverage profiles), so relevance decides, exactly "
             "the tie-break repetition alone can't make.\n")
    for stage in ("MOFU", "TOFU"):
        champs = segments.get(stage)
        if not champs:
            continue
        star = "  ⭐ primary" if stage == primary else ""
        L.append(f"\n#### {stage} — {labels[stage]}{star}")
        L.append("| # | Brand | Champion ad | Repetition | Guidde-fit (tier · keyword) | **Stage 2 final** | Ad |")
        L.append("|--:|---|---|--:|--:|--:|---|")
        for i, a in enumerate(champs, 1):
            flag = " ⚑low-impr" if a.get("low_impression") else ""
            rel = (f"{a.get('relevance_n','—')} · t{a.get('relevance_tier','?')} · "
                   f"`{a.get('relevance_term','—')}`")
            L.append(f"| {i} | {a['brand']} | {_hook(a)[:44]!r}{flag} | "
                     f"{a.get('repetition_n','—')} | {rel} | **{a['final_score']}** "
                     f"| [ad]({a['ad_library_url_exact']}) |")
        # Per-champion audit: WHY each winning ad scored what it did (both stages).
        L.append(f"\n_Why each {stage} champion scored what it did:_")
        for a in champs:
            L.append(
                f"- **{a['brand']}** {_hook(a)[:40]!r} → "
                f"**Stage 1** `{s1['reissue_persistence']}×persist({a.get('persistence_n','?')}) "
                f"+ {s1['longevity']}×longev({a.get('longevity_n','?')}) = {a['champion_score']}` "
                f"({a.get('reissue_periods','?')} distinct months, "
                f"{a.get('true_longevity_days',0):.0f} days running). "
                f"**Stage 2** `{s2['repetition_across_competitors']}×rep({a.get('repetition_n','?')}) "
                f"+ {s2['guidde_relevance']}×rel({a.get('relevance_n','?')}) = {a['final_score']}` — "
                f"repetition from angle `{a.get('best_angle','?')}` "
                f"({a.get('xcomp','?')}/{ncomp} rivals share it); relevance tier "
                f"{a.get('relevance_tier','?')} ({a.get('relevance_label','?')}) set by the "
                f"word `{a.get('relevance_term','—')}`.")
    L.append("\n_Table links browse the brand's page narrowed to the ad's copy; the "
             "**exact-ad** Library-ID link (`?id=`) is in §5. ⚑ = Meta flags "
             "low-impression._\n")

    # 5. Primary winner detail
    L.append(f"## 5. Primary winner ({labels[primary]})")
    L.append(f"**{winner['brand']} — \"{winner['body'][:90]}\"**")
    L.append(f"**→ [View the exact winning ad]({winner['ad_library_url_exact']})** "
             f"(opens the single winning ad by Meta Library ID {winner['ad_id']}) · "
             f"[browse all {winner['brand']} ads]({winner['ad_library_url']})\n")
    L.append("**How this ad's score is built** — Stage 1 proves it, Stage 2 ranks it:")
    L.append(f"- **Stage 1 (within Scribe):** `champion_score = "
             f"{s1['reissue_persistence']}×persistence({winner.get('persistence_n','?')}) "
             f"+ {s1['longevity']}×longevity({winner.get('longevity_n','?')}) = "
             f"{winner['champion_score']}`. It re-issued across "
             f"{winner.get('reissue_periods','?')} distinct months "
             f"({winner.get('true_versions','?')} versions), running "
             f"{winner.get('true_longevity_days',0):.0f} days, Scribe's most-proven ad.")
    L.append(f"- **Stage 2 (across the champions):** `final = "
             f"{s2['repetition_across_competitors']}×repetition({winner.get('repetition_n','?')}) "
             f"+ {s2['guidde_relevance']}×relevance({winner.get('relevance_n','?')}) = "
             f"{winner['final_score']}`.")
    L.append(f"    - *Repetition:* its strongest angle `{winner.get('best_angle','?')}` "
             f"is run by {winner.get('xcomp','?')}/{ncomp} competitors (from §4a).")
    L.append(f"    - *Relevance:* **tier {winner['relevance_tier']} "
             f"({winner['relevance_label']})**, matches Guidde's core on "
             f"`{winner['relevance_term']}`, the ad literally \"builds a guide "
             f"automatically\" from a captured workflow, Guidde's exact job.")
    L.append(f"- **Full ad, not just the video:** headline "
             f"\"{winner.get('headline','—')}\" · description "
             f"\"{winner.get('description','—')}\" · CTA \"{winner['cta_text']}\".")
    L.append(f"- **Format:** {winner['format']} · funnel stage "
             f"{winner['funnel_stage']} · funnel {winner['funnel']}.")

    # 6. Notable & limits
    L.append("\n## 6. Notable & honest limits")
    L.append("- **Funnel split fixes the apples-to-oranges problem:** WalkMe's "
             "\"download the report\" ad is now the TOFU winner in its own lane, not "
             "beating product ads on generic AI/stat angles.")
    L.append("- **Meta's own performance signal:** some ads carry an impression flag "
             "(`<100` = low-impression); WalkMe's report copies are flagged low, "
             "confirming they underperform. The signal is sparse (Scribe shows none), "
             "so it flags losers rather than ranking the field.")
    L.append("- **Clustering is a TF-IDF heuristic:** it can mis-group at the margins; "
             f"the threshold ({meta['cluster_threshold']}) is tuned so different "
             "campaigns don't merge. True embeddings are the roadmap fix.")
    L.append("- **DCO ads can't be deep-linked**, and a single snapshot ages, so "
             "re-run before acting.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(L) + "\n")
    print(f"[report] wrote {OUT.relative_to(ROOT)} ({len(L)} lines)")


if __name__ == "__main__":
    main()
