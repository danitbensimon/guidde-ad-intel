"""
Stage 1 - Collect.

Collects active US video ads for each brand from the public Meta Ad Library
(no login) via the Apify actor, and saves raw JSON per brand to
data/raw/<brand>.json.

We collect BY PAGE ID (resolved during discovery) rather than by keyword, so the
results are the brand's own ads, not everyone who happens to use the word.

Failure handling: a brand with no page_id (WalkMe) is written as an empty file;
a brand whose run errors is logged and written empty. One bad query never sinks
the run.
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from config import (
    ACTIVE_STATUS,
    APIFY_ACTOR,
    BRANDS,
    COUNTRY,
    MAX_ADS_PER_PAGE,
    MEDIA_TYPE,
)

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def build_page_url(page_id: str, status: str) -> str:
    """Public Meta Ad Library URL for one advertiser's page, one active_status."""
    params = {
        "active_status": status,
        "ad_type": "all",
        "country": COUNTRY,
        "view_all_page_id": page_id,
        "search_type": "page",
    }
    # Only constrain media_type when we are narrowing; "all" means omit it.
    if MEDIA_TYPE and MEDIA_TYPE != "all":
        params["media_type"] = MEDIA_TYPE
    return "https://www.facebook.com/ads/library/?" + urllib.parse.urlencode(params)


def run_actor(token: str, url: str) -> list:
    endpoint = (
        f"https://api.apify.com/v2/acts/{APIFY_ACTOR}"
        f"/run-sync-get-dataset-items?token={token}"
    )
    payload = {"urls": [{"url": url, "method": "GET"}], "count": MAX_ADS_PER_PAGE}
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("APIFY_TOKEN not set. Copy .env.example to .env and add your token.")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    summary = {}
    for brand in BRANDS:
        name, page_id = brand["name"], brand["page_id"]
        out = RAW_DIR / f"{name.lower()}.json"
        if not page_id:
            out.write_text("[]")
            summary[name] = {"active": 0, "inactive": 0}
            print(f"[collect] {name}: no page found, wrote empty")
            continue
        # Two pulls: ACTIVE (the ads we score) + INACTIVE (the message back-history).
        # A single "all" pull front-loads inactive ads and can return zero active.
        merged, counts = {}, {"active": 0, "inactive": 0}
        for status in ("active", "inactive"):
            url = build_page_url(page_id, status)
            try:
                items = run_actor(token, url)
            except Exception as exc:  # noqa: BLE001
                print(f"[collect] {name}/{status} FAILED: {exc}", file=sys.stderr)
                items = []
            counts[status] = len(items)
            for a in items:
                merged[a.get("ad_archive_id")] = a  # dedupe by archive id
        out.write_text(json.dumps(list(merged.values()), indent=2))
        summary[name] = counts
        print(f"[collect] {name}: {counts['active']} active + {counts['inactive']} "
              f"inactive -> {len(merged)} unique -> {out.name}")

    print("\n[collect] pulled per brand:")
    for name, n in summary.items():
        print(f"  {name:10s} {n}")


if __name__ == "__main__":
    main()
