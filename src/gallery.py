"""
Stage 4 - Winners gallery (HTML).

Self-contained output/champions_report.html: the winning ad in each funnel stage
with its real screenshot embedded (base64), and, for the primary (product) winner,
the earlier versions of the SAME ad, so its persistence is visible. Regenerate
after a run.
"""

from __future__ import annotations

import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SHOTS = DATA / "champion_shots"
OUT = ROOT / "output" / "champions_report.html"

STAGE_SHOT = {"MOFU": "winner_car.jpg", "TOFU": "tofu_winner.jpg"}
# The winning ad's real arc, actual frames from its own video file (a solo
# car-POV recommendation monologue), so the card shows how the ad actually plays.
ARC = [
    ("Hook", "“POV you wasted too much time…”", "carc_hook.jpg"),
    ("Relatable", "to-camera recommendation", "carc_relate.jpg"),
    ("Product", "one screen-recording cut", "carc_product.jpg"),
    ("Kicker", "“but it's free”", "carc_value.jpg"),
]
ARC_CAPTION = ("A solo car-POV UGC monologue. The written copy carries the "
               "documentation angle; the video sells relatable enthusiasm.")


def _b64(name: str) -> str:
    p = SHOTS / name
    return ("data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode()
            if p.exists() else "")


def _history_html() -> str:
    steps = "".join(f"""
        <figure class="hstep">
          <img src="{_b64(f)}" alt="{label} frame" loading="lazy">
          <figcaption><span class="hdate">{label}</span>
            <span class="hstate off">{note}</span></figcaption>
        </figure>""" for label, note, f in ARC)
    return f"""
        <div class="history">
          <p class="hlabel">◆ How the winning ad actually plays — {ARC_CAPTION}</p>
          <div class="hrow arc4">{steps}</div>
        </div>"""


def main() -> None:
    meta = json.loads((DATA / "run_meta.json").read_text())
    segments, labels = meta["segments"], meta["stage_labels"]
    primary = meta["primary_stage"]
    gen = meta["generated_utc"]

    cards = []
    for stage in ("MOFU", "TOFU"):
        champs = segments.get(stage)
        if not champs:
            continue
        a = champs[0]
        is_primary = stage == primary
        img = _b64(STAGE_SHOT.get(stage, ""))
        head = a["body"].split("  ")
        head = next((h.strip() for h in head if h.strip()
                     and "." not in h.split()[0]), a["body"][:60])
        lowimp = ('<span class="flag">Meta: low-impression</span>'
                  if a.get("low_impression") else "")
        cards.append(f"""
      <article class="card{' winner' if is_primary else ''}">
        <div class="shot"><img src="{img}" alt="{a['brand']} ad" loading="lazy"></div>
        <div class="meta">
          <div class="rank">
            <span class="badge">{'PRIMARY WINNER' if is_primary else stage}</span>
            <span class="stage">{labels[stage]}</span>
          </div>
          <p class="brand">{a['brand']} {lowimp}</p>
          <p class="copy">{head[:120]}</p>
          <dl class="stats">
            <div><dt>Stage 2 score</dt><dd class="big">{a['final_score']}</dd><dd class="tier">repetition {a.get('repetition_n','—')} + Guidde-fit {a.get('relevance_n','—')} ({a.get('relevance_label','')})</dd></div>
            <div><dt>Re-issue months</dt><dd>{a.get('reissue_periods','—')}</dd></div>
            <div><dt>Message running for</dt><dd>{a.get('true_longevity_days',0):.0f} days</dd></div>
            <div><dt>Total copies</dt><dd>{a.get('true_versions','—')}</dd></div>
          </dl>
          <a class="link" href="{a.get('ad_library_url_exact') or a['ad_library_url']}" target="_blank" rel="noopener">{'View the exact ad in the Ad Library →' if is_primary else 'Find it in the Ad Library →'}</a>
          {_history_html() if is_primary else ''}
        </div>
      </article>""")

    html = f"""<title>Winning Ads by Funnel Stage</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root {{ --ground:#FCFCFE; --surface:#FFFFFF; --ink:#17161C; --muted:#6C6B77;
    --line:#E2E2EA; --faint:#ECECF2; --accent:#6D4AFF; --accent-soft:#F1EEFF; --warn:#B4540A; }}
  @media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
    --ground:#121116; --surface:#1A1922; --ink:#ECECF2; --muted:#9C9BA8;
    --line:#2C2B37; --faint:#26252F; --accent:#9D89FF; --accent-soft:#211D33; --warn:#E0925A; }} }}
  :root[data-theme="dark"] {{ --ground:#121116; --surface:#1A1922; --ink:#ECECF2;
    --muted:#9C9BA8; --line:#2C2B37; --faint:#26252F; --accent:#9D89FF; --accent-soft:#211D33; --warn:#E0925A; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--ground); color:var(--ink); line-height:1.5;
    font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; -webkit-font-smoothing:antialiased; }}
  .wrap {{ max-width:920px; margin:0 auto; padding:48px 24px 72px; }}
  header {{ border-bottom:1px solid var(--line); padding-bottom:24px; margin-bottom:34px; }}
  .eyebrow {{ text-transform:uppercase; letter-spacing:.12em; font-size:12px; font-weight:600; color:var(--accent); margin:0 0 10px; }}
  h1 {{ font-size:clamp(27px,4.4vw,38px); font-weight:800; letter-spacing:-.02em; margin:0 0 8px; text-wrap:balance; }}
  .sub {{ color:var(--muted); font-size:15px; margin:0; max-width:62ch; }}
  .runline {{ color:var(--muted); font-size:13px; margin-top:14px; font-variant-numeric:tabular-nums; }}
  .grid {{ display:flex; flex-direction:column; gap:20px; }}
  .card {{ display:grid; grid-template-columns:300px 1fr; gap:24px; background:var(--surface); border:1px solid var(--line); border-radius:16px; padding:18px; }}
  .card.winner {{ border-color:var(--accent); box-shadow:0 0 0 1px var(--accent), 0 12px 34px -20px var(--accent); }}
  .shot {{ border-radius:10px; overflow:hidden; background:var(--faint); align-self:start; }}
  .shot img {{ display:block; width:100%; height:auto; }}
  .meta {{ display:flex; flex-direction:column; gap:12px; min-width:0; }}
  .rank {{ display:flex; align-items:center; gap:10px; flex-wrap:wrap; }}
  .badge {{ font-size:11px; font-weight:700; letter-spacing:.07em; text-transform:uppercase; padding:4px 9px; border-radius:999px; background:var(--accent-soft); color:var(--accent); }}
  .winner .badge {{ background:var(--accent); color:#fff; }}
  .stage {{ font-size:12px; color:var(--muted); text-transform:uppercase; letter-spacing:.05em; }}
  .brand {{ font-weight:700; font-size:18px; margin:0; display:flex; align-items:center; gap:8px; }}
  .flag {{ font-size:11px; font-weight:600; color:var(--warn); border:1px solid var(--warn); border-radius:999px; padding:1px 7px; text-transform:none; letter-spacing:0; }}
  .copy {{ margin:0; font-size:15px; }}
  .stats {{ display:grid; grid-template-columns:1fr 1fr; gap:10px 20px; margin:2px 0 0; }}
  .stats div {{ display:flex; flex-direction:column; gap:2px; }}
  dt {{ font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:.05em; }}
  dd {{ margin:0; font-weight:600; font-size:15px; font-variant-numeric:tabular-nums; }}
  dd.big {{ font-size:22px; color:var(--accent); }}
  dd.tier {{ font-size:12px; font-weight:600; color:var(--muted); margin-top:1px; }}
  .link {{ color:var(--accent); text-decoration:none; font-weight:600; font-size:14px; width:fit-content; }}
  .link:hover {{ text-decoration:underline; }}
  .history {{ margin-top:6px; padding-top:14px; border-top:1px dashed var(--line); }}
  .hlabel {{ font-size:11px; text-transform:uppercase; letter-spacing:.06em; color:var(--accent); margin:0 0 12px; font-weight:700; }}
  .hrow {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }}
  .hrow.arc4 {{ grid-template-columns:repeat(4,1fr); gap:10px; }}
  @media (max-width:640px) {{ .hrow.arc4 {{ grid-template-columns:repeat(2,1fr); }} }}
  .hstep {{ margin:0; }}
  .hstep img {{ width:100%; height:auto; border-radius:8px; border:1px solid var(--line); }}
  .hstep figcaption {{ display:flex; align-items:center; gap:8px; margin-top:8px; }}
  .hdate {{ font-weight:700; font-size:13px; font-variant-numeric:tabular-nums; }}
  .hstate {{ font-size:11px; text-transform:uppercase; letter-spacing:.05em; padding:2px 7px; border-radius:999px; }}
  .hstate.off {{ background:var(--faint); color:var(--muted); }}
  .hstate.on {{ background:var(--accent-soft); color:var(--accent); font-weight:600; }}
  footer {{ margin-top:38px; padding-top:22px; border-top:1px solid var(--line); color:var(--muted); font-size:13px; }}
  footer b {{ color:var(--ink); }}
  @media (max-width:640px) {{ .card {{ grid-template-columns:1fr; }} }}
</style>
<div class="wrap">
  <header>
    <p class="eyebrow">Competitor Ad Intelligence · for Guidde</p>
    <h1>The winning ad in each funnel stage</h1>
    <p class="sub">Ads are separated by what they're trying to do, so a lead-gen report never
      competes head-to-head with a product ad. The primary result Guidde should rebuild is the
      product (MOFU) winner.</p>
    <p class="runline">{gen} · {meta['total_active_scored']} active ads scored against
      {meta['total_inactive_history']} inactive versions for history</p>
  </header>
  <div class="grid">{''.join(cards)}</div>
  <footer>
    <b>How it was scored.</b> Three gates (active · not retargeting · sells a Guidde use case), then,
    inside each funnel stage: Stage 1 picks each brand's champion within its own ads
    (persistence = distinct months the message was re-launched, from active + inactive history);
    Stage 2 ranks those champions on two combined signals: cross-competitor repetition (how many
    rivals share the angle) and Guidde-fit (how close the message sits to Guidde's own job, graded
    core → adjacent → peripheral). Meta's own low-impression flag is surfaced where present.
  </footer>
</div>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html)
    print(f"[gallery] wrote {OUT.relative_to(ROOT)} ({len(html)//1024} KB)")


if __name__ == "__main__":
    main()
