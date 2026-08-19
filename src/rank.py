"""
Scoring - pick each brand's champion (Stage 1), then the overall winner (Stage 2).

Two stages that ask two different questions, run separately inside each funnel stage:
  Stage 1 (within-brand): champion_score = w_pers*persistence_n + w_long*longevity_n
  Stage 2 (cross-brand):  final_score    = w_rel*relevance_n   (closeness to Guidde)

Every score is stored broken into its weighted terms so the number is auditable.

Outputs:
  data/ranked.csv   - every active ad, scored, sorted, with score terms + link.
  data/ranked.json  - same, full records (used by report.py).
  data/winner.json  - the top-scoring ELIGIBLE ad (produced creative, not DCO).
  data/run_meta.json- run metadata: counts, weights, angle coverage, timestamp.
"""

from __future__ import annotations

import csv
import json
import re
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

from angles import (
    ANGLES,
    RELEVANCE_LABEL,
    ad_angles,
    ad_text,
    funnel_stage,
    guidde_relevance,
    is_guidde_alternative,
)
from matching import cluster
from config import (
    BRANDS,
    CLUSTER_THRESHOLD,
    COUNTRY,
    DCO_ELIGIBLE,
    EXCLUDE_RETARGETING,
    REQUIRE_GUIDDE_ALTERNATIVE,
    S1_LONGEVITY,
    S1_PERSISTENCE,
    S2_RELEVANCE,
    S2_REPETITION,
)

DATA = Path(__file__).resolve().parent.parent / "data"
RAW_DIR = DATA / "raw"
NOW = datetime.now(timezone.utc).timestamp()
N_COMPETITORS = len(BRANDS)


def _body(snap: dict) -> str:
    b = snap.get("body")
    if isinstance(b, dict):
        b = b.get("text")
    return (b or "").strip()


def _media(snap: dict):
    for v in snap.get("videos") or []:
        if isinstance(v, dict) and (v.get("video_hd_url") or v.get("video_sd_url")):
            return "video", v.get("video_hd_url") or v.get("video_sd_url")
    for c in snap.get("cards") or []:
        if isinstance(c, dict) and (c.get("video_hd_url") or c.get("video_sd_url")):
            return "video", c.get("video_hd_url") or c.get("video_sd_url")
    for img in snap.get("images") or []:
        if isinstance(img, dict) and img.get("original_image_url"):
            return "image", img["original_image_url"]
    for c in snap.get("cards") or []:
        if isinstance(c, dict) and c.get("original_image_url"):
            return "image", c["original_image_url"]
    return None, None


def _funnel(ad: dict) -> str:
    u = json.dumps(ad).lower()
    if "t:retargeting" in u:
        return "retargeting"
    if any(k in u for k in ("t:prospecting", "t:lookalike", "t:interest", "t:broad")):
        return "prospecting"
    return "unknown"


def _prospecting(funnel: str, angles: list, cta: str) -> tuple[str, float]:
    """Classify prospecting for EVERY brand, not just those with UTM tags.

    UTM target tags are hard evidence when present. Otherwise we infer from the
    creative: a problem/stat hook or a lead-magnet CTA is a cold-audience
    (prospecting) pattern; a bare feature reminder is treated as neutral. This
    removes the bias where only Loom (the one brand that tags links) could score
    1.0 on prospecting.
    """
    if funnel == "retargeting":
        return "retargeting", 0.0
    if funnel == "prospecting":
        return "prospecting·utm", 1.0
    cta = (cta or "").lower()
    if {"problem_hook", "stat_proof"} & set(angles) or "download" in cta:
        return "prospecting·inferred", 1.0
    return "neutral", 0.5


def load_ads():
    """Return (relevant ads active+inactive, angle->set(active competitors), counts).

    We keep INACTIVE ads too: they are the message back-history used to measure how
    long a message has really run across its re-issued versions. Only active ads
    are scored later; inactive ads only feed the message-history clustering.
    Cross-competitor coverage is built from ACTIVE ads (the current market).
    """
    ads, coverage, counts = [], {}, {}
    for brand in BRANDS:
        path = RAW_DIR / f"{brand['name'].lower()}.json"
        raw = json.loads(path.read_text()) if path.exists() else []
        c = {"pulled": len(raw), "active": 0, "inactive": 0,
             "retargeting_excluded": 0, "not_alternative": 0}
        lc = brand["link_contains"]
        for a in raw:
            snap = a.get("snapshot", {}) or {}
            if lc and lc not in json.dumps(a).lower():
                continue  # Loom: keep only Loom-linked ads on the Atlassian page
            start = a.get("start_date")
            if not start:
                continue
            funnel_utm = _funnel(a)
            if EXCLUDE_RETARGETING and funnel_utm == "retargeting":
                c["retargeting_excluded"] += 1
                continue
            if REQUIRE_GUIDDE_ALTERNATIVE and not is_guidde_alternative(a):
                c["not_alternative"] += 1
                continue
            angs = ad_angles(a)
            rtier, rterm = guidde_relevance(a)   # graded closeness to Guidde (Stage 2)
            active = bool(a.get("is_active"))
            if active:
                c["active"] += 1
                for ang in angs:
                    coverage.setdefault(ang, set()).add(brand["name"])
            else:
                c["inactive"] += 1
            kind, media = _media(snap)
            body = (ad_text(a) or _body(snap)).replace("\n", " ").strip()
            # Narrow the link by searching the brand's page for this ad's own copy
            # (first distinctive words, skipping the domain token). Per-ad ?id=
            # links do not work for these multi-version DCO ads, but a keyword
            # search within the page narrows ~170 ads down to a handful.
            qwords = [w for w in body.split() if "." not in w and "/" not in w][:6]
            q = urllib.parse.quote(" ".join(qwords))
            impr = (a.get("impressions_with_index") or {}).get("impressions_text")
            ads.append({
                "brand": brand["name"],
                "ad_id": a.get("ad_archive_id"),
                "is_active": active,
                "funnel_stage": funnel_stage(a),
                "impressions": impr,          # e.g. "<100" = Meta's low-impression flag
                "low_impression": impr == "<100",
                "format": snap.get("display_format"),
                "start_date": start,
                "days_running": round((NOW - start) / 86400, 1),
                "collation_count": a.get("collation_count") or 1,
                "angles": sorted(angs),
                "relevance_tier": rtier,
                "relevance_term": rterm,
                "relevance_label": RELEVANCE_LABEL[rtier],
                "relevance_n": round(rtier / 3, 3),
                "funnel": _prospecting(funnel_utm, sorted(angs), snap.get("cta_text"))[0],
                "cta_text": snap.get("cta_text"),
                # A Meta ad is more than its video: capture the other text elements too.
                "headline": snap.get("title"),
                "description": snap.get("link_description"),
                "body": body[:300],
                "_text": ad_text(a) or _body(snap),  # for message clustering
                "media_kind": kind,
                "media_url": media,
                "link_url": snap.get("link_url"),
                # Exact per-ad link = Meta's canonical Library-ID URL. It resolves to
                # the single ad when Meta exposes it standalone (verified for the
                # winner); some multi-version ads fall back to the advertiser's
                # library, hence the copy-narrowed search below as a fallback.
                "ad_library_url_exact":
                    f"https://www.facebook.com/ads/library/?id={a.get('ad_archive_id')}",
                "ad_library_url": (
                    f"https://www.facebook.com/ads/library/?active_status=active"
                    f"&ad_type=all&country={COUNTRY}&view_all_page_id="
                    f"{brand['page_id']}&search_type=page&q={q}"),
            })
        counts[brand["name"]] = c
    return ads, coverage, counts


def add_message_history(ads):
    """Cluster each brand's ads (active + inactive) into messages by content
    similarity, then record, for every ad, the message's TRUE longevity (days
    since the earliest version, active or inactive) and TRUE version count."""
    from collections import defaultdict
    by_brand = defaultdict(list)
    for a in ads:
        by_brand[a["brand"]].append(a)
    for group in by_brand.values():
        labels = cluster([a["_text"] for a in group], CLUSTER_THRESHOLD)
        buckets = defaultdict(list)
        for a, lab in zip(group, labels):
            a["cluster"] = lab
            buckets[lab].append(a)
        for cads in buckets.values():
            earliest = min(a["start_date"] for a in cads)
            versions = len(cads)
            active_versions = sum(1 for a in cads if a["is_active"])
            # DISTINCT re-issue periods = how many separate calendar months the
            # brand launched a version of this message. Rewards re-running over
            # time, not a blast of many copies in one window.
            months = {datetime.fromtimestamp(a["start_date"], timezone.utc)
                      .strftime("%Y-%m") for a in cads}
            for a in cads:
                a["true_longevity_days"] = round((NOW - earliest) / 86400, 1)
                a["true_versions"] = versions
                a["active_versions"] = active_versions
                a["reissue_periods"] = len(months)


def add_repetition(ads, coverage):
    """Cross-competitor repetition (the brief's criterion): for each ad, how many
    competitors share its angles. rep_raw = sum of per-angle competitor coverage;
    repetition_n normalizes it across the active field. best_angle/xcomp record the
    ad's single most-validated angle for reporting."""
    for a in ads:
        per = {ang: len(coverage.get(ang, ())) for ang in a["angles"]}
        a["angle_coverage"] = per
        a["rep_raw"] = sum(per.values())
        best = max(a["angles"], key=lambda ang: per[ang]) if a["angles"] else None
        a["best_angle"] = best
        a["best_angle_competitors"] = sorted(coverage.get(best, ())) if best else []
        a["xcomp"] = per.get(best, 0)
    max_rep = max((a["rep_raw"] for a in ads), default=1) or 1
    for a in ads:
        a["repetition_n"] = round(a["rep_raw"] / max_rep, 3)


def stage1_score(ads):
    """STAGE 1: PURELY within-brand. Score each active ad against its OWN brand and
    pick the brand's champion. No competitor signal here.

    persistence = distinct months the brand re-launched the message (rewards
    re-running over time, not a blast of copies), longevity = days since the
    message's earliest version. Both normalized within the brand.
    """
    brand_max_long, brand_max_per = {}, {}
    for a in ads:
        b = a["brand"]
        brand_max_long[b] = max(brand_max_long.get(b, 0.0), a["true_longevity_days"])
        brand_max_per[b] = max(brand_max_per.get(b, 1), a["reissue_periods"])
    for a in ads:
        b = a["brand"]
        a["longevity_n"] = round(a["true_longevity_days"] / (brand_max_long[b] or 1.0), 3)
        a["persistence_n"] = round(a["reissue_periods"] / (brand_max_per[b] or 1), 3)
        a["champion_score"] = round(
            S1_PERSISTENCE * a["persistence_n"] + S1_LONGEVITY * a["longevity_n"], 4)
    return brand_max_long


def dedupe(ads):
    """Collapse identical creatives (same brand + same message) to one concept,
    keeping the strongest Stage-1 instance and recording how many copies it runs."""
    groups = {}
    for a in ads:
        key = (a["brand"], re.sub(r"\W+", " ", a["body"].lower()).strip()[:120])
        groups.setdefault(key, []).append(a)
    out = []
    for g in groups.values():
        g.sort(key=lambda a: (a["champion_score"], a["days_running"]), reverse=True)
        rep = g[0]
        rep["copies_running"] = len(g)
        out.append(rep)
    out.sort(key=lambda a: (a["champion_score"], a["days_running"]), reverse=True)
    return out


def pick_champions(ads):
    """The single top-scoring ad per brand after Stage 1."""
    champions = {}
    for a in sorted(ads, key=lambda x: (x["champion_score"], x["days_running"]),
                    reverse=True):
        champions.setdefault(a["brand"], a)
    return list(champions.values())


def stage2_final(champions):
    """STAGE 2: the brand champions compete on TWO cross-brand signals combined:
    cross-competitor repetition (the market's vote, the brief's criterion) and
    Guidde-relevance (closeness to Guidde's core, which breaks ties repetition
    structurally can't). Remaining ties fall back to the Stage-1 champion score,
    then true longevity. Retargeting is excluded by the gate, so no prospecting
    term is needed."""
    for a in champions:
        a["final_score"] = round(
            S2_REPETITION * a["repetition_n"] + S2_RELEVANCE * a["relevance_n"], 4)
        a["eligible"] = a["format"] != "DCO" or DCO_ELIGIBLE
    champions.sort(
        key=lambda a: (a["final_score"], a["repetition_n"], a["champion_score"],
                       a["true_longevity_days"]),
        reverse=True)
    return champions


STAGE_ORDER = ["MOFU", "TOFU"]
STAGE_LABEL = {"MOFU": "Product / how-it-works", "TOFU": "Awareness / lead-gen"}


def slim(a):
    return {k: a[k] for k in (
        "brand", "format", "is_active", "funnel_stage", "impressions",
        "low_impression", "days_running", "true_longevity_days", "true_versions",
        "active_versions", "reissue_periods", "copies_running", "persistence_n",
        "longevity_n", "champion_score", "repetition_n", "best_angle", "xcomp",
        "relevance_n", "relevance_tier", "relevance_term", "relevance_label",
        "final_score", "funnel", "cta_text", "headline", "description", "body",
        "ad_library_url", "ad_library_url_exact") if k in a}


def main() -> None:
    ads, coverage, counts = load_ads()       # active + inactive relevant ads
    add_message_history(ads)                  # cluster + true longevity/versions
    active = [a for a in ads if a["is_active"]]
    total_active = len(active)
    stage1_score(active)                      # champion_score per ad (within-brand)
    add_repetition(active, coverage)          # repetition_n per ad (cross-brand)
    active = dedupe(active)
    for a in active:
        a.pop("_text", None)

    # SEGMENT by funnel stage: each stage crowns its own winner, so a report
    # (TOFU) ad never competes head-to-head with a product (MOFU) ad.
    segments = {}
    for stage in STAGE_ORDER:
        seg = [a for a in active if a["funnel_stage"] == stage]
        if not seg:
            continue
        champs = stage2_final(pick_champions(seg))
        segments[stage] = champs
    # Primary winner = the Product/how-it-works (MOFU) stage, what Guidde rebuilds.
    primary_stage = next((s for s in STAGE_ORDER if s in segments), None)
    winner = next(a for a in segments[primary_stage] if a["eligible"])

    meta = {
        "generated_utc": datetime.fromtimestamp(NOW, timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "competitors": [b["name"] for b in BRANDS],
        "stage1_weights": {"reissue_persistence": S1_PERSISTENCE, "longevity": S1_LONGEVITY},
        "stage2_weights": {"repetition_across_competitors": S2_REPETITION,
                           "guidde_relevance": S2_RELEVANCE},
        "gates": "active + not-retargeting + is-Guidde-alternative",
        "cluster_threshold": CLUSTER_THRESHOLD,
        "primary_stage": primary_stage,
        "stage_labels": STAGE_LABEL,
        "total_pulled": sum(c["pulled"] for c in counts.values()),
        "total_active": sum(c["active"] for c in counts.values()),
        "total_inactive_history": sum(c["inactive"] for c in counts.values()),
        "retargeting_excluded": sum(c["retargeting_excluded"] for c in counts.values()),
        "not_alternative_excluded": sum(c["not_alternative"] for c in counts.values()),
        "total_active_scored": total_active,
        "distinct_creatives": len(active),
        "stage_count": {s: sum(1 for a in active if a["funnel_stage"] == s)
                        for s in STAGE_ORDER},
        "segments": {s: [slim(a) for a in champs] for s, champs in segments.items()},
        "per_brand": counts,
        "angle_coverage": {k: sorted(v) for k, v in sorted(
            coverage.items(), key=lambda kv: -len(kv[1]))},
        "angle_keywords": ANGLES,
    }

    cols = ["champion_score", "repetition_n", "relevance_n", "relevance_tier",
            "final_score", "brand", "funnel_stage", "format", "impressions",
            "true_longevity_days", "true_versions", "reissue_periods", "funnel",
            "cta_text", "headline", "description", "ad_id", "body", "ad_library_url"]
    with (DATA / "ranked.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(active)

    (DATA / "ranked.json").write_text(json.dumps(active, indent=2))
    (DATA / "run_meta.json").write_text(json.dumps(meta, indent=2))
    (DATA / "winner.json").write_text(json.dumps(winner, indent=2))

    print(f"[rank] {total_active} active scored; stages {meta['stage_count']}")
    for stage, champs in segments.items():
        w0 = champs[0]
        print(f"  [{stage}] winner: {w0['brand']} final={w0['final_score']} "
              f"(rep={w0['repetition_n']} + rel={w0['relevance_n']} tier{w0['relevance_tier']}) "
              f"trueLong={w0['true_longevity_days']:.0f}d | {w0['body'][:42]!r}")


if __name__ == "__main__":
    main()
