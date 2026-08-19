"""
Part 2, Stage 4 - Storyboard (HTML) with generated frames.

Self-contained output/04_storyboard.html: the six-shot storyboard for Guidde's ad,
adapted from the winning Scribe ad. Each shot is a real AI-generated 9:16 frame
(Higgsfield Soul 2.0 for the UGC creator shots, kept consistent across shots via a
character reference; a text-capable model for the product UI and brand card), shown
in a phone frame with its burned-in on-screen caption, and paired with timecode,
voiceover and direction. The real winning-ad frames are embedded as reference.
Regenerate after editing the shot list or swapping frames.
"""

from __future__ import annotations

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "data" / "champion_shots"      # real competitor reference frames
AI = ROOT / "output" / "storyboard_ai"        # generated Guidde frames
OUT = ROOT / "output" / "04_storyboard.html"


def _b64(path: Path) -> str:
    return ("data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()
            if path.exists() else "")


def _phone(frame: str, caption: str, tag: str = "", overlay: bool = True) -> str:
    tag_html = f'<span class="ptag">{tag}</span>' if tag else ""
    cap_html = f'<div class="cap">{caption}</div>' if (overlay and caption) else ""
    return (f'<div class="phone"><div class="screen">'
            f'<img class="ph" src="{_b64(AI / frame)}" alt="" loading="lazy">'
            f'{tag_html}{cap_html}</div><div class="notch"></div></div>')


# shot: (n, time, role, frame_file, tag, overlay, on-screen caption, VO, direction)
# Adapts the winning ad's format into a two-hander (matches the produced video):
# two people in one car, the driver vents the problem, the passenger gives the fix,
# with one cut to the real Guidde platform. Same car setting; copy is original.
SHOTS_META = [
    (1, "0.0–3.5s", "Hook", "pshot1_web.jpg", "0:00", True,
     "POV: being the one who knows how everything works is a second full-time job.",
     "POV: being the one who knows how everything works is a second full-time job.",
     "Two people, one car. The driver vents to camera, dry and fed up. No brand, no product yet."),
    (2, "3.5–7.0s", "Agitate", "pshot2_web.jpg", "", True,
     "I've rewritten the same SOP four times, and nobody's read it once.",
     "I've rewritten the same SOP four times, and nobody's read it once.",
     "Same driver, still dry. The specific chore, acted, not listed."),
    (3, "7.0–10.7s", "The fix", "pshot3_web.jpg", "the one product beat", True,
     "So stop writing it. You do the task once, and Guidde turns it into a video.",
     "So stop writing it. You do the task once, and Guidde turns it into a video.",
     "The passenger gives the fix, over a cut to the REAL Guidde platform (AI voiceover, captions, 40+ languages on screen). Product as the payoff, mouth off-screen."),
    (4, "10.7–14.3s", "Payoff", "pshot4_web.jpg", "", True,
     "Now I just send a link instead of explaining it for the hundredth time.",
     "Now I just send a link instead of explaining it for the hundredth time.",
     "Back to the driver, relieved. Sharing with one link is the whole win."),
    (5, "14.3–18.0s", "Kicker", "pshot5_web.jpg", "", True,
     "And it's free. Revolutionary, I know.",
     "And it's free. Revolutionary, I know.",
     "The passenger's deadpan kicker, the dry humour that mirrors the winner's tone."),
    (6, "18.0–20.5s", "Brand card", "pshot6_web.jpg", "", False,
     "Guidde · Try For Free",
     "",
     "Clean end card, single maroon pop. The only fully-branded moment."),
]

# The full ad, not just the video: hook, primary text (body), end card, CTA.
AD_COPY = {
    "hook": "POV: being the one who knows how everything works is a second full-time job.",
    "body": ("The part nobody warns you about when you're the one who knows how "
             "everything works: you become the office help desk, rewriting the same SOP "
             "nobody reads. It doesn't have to be that way. Guidde captures any workflow "
             "and turns it into a professional step-by-step video, with an AI voiceover, "
             "in 40+ languages, that you share across your whole team with one link. "
             "You do your job, the guide does the explaining. Start free at guidde.com"),
    "endcard": "The answer you keep repeating, recorded once.",
    "cta": "Try For Free",
}


def main() -> None:
    strip = "".join(
        f'''
      <article class="shot">
        {_phone(frame, cap, tag, overlay)}
        <div class="meta">
          <div class="tophdr"><span class="num">SHOT {n}</span>
            <span class="time">{time}</span><span class="role">{role}</span></div>
          <p class="onscreen">“{cap}”</p>
          <p class="vo"><span>VO</span> {vo}</p>
          <p class="dir">{direction}</p>
        </div>
      </article>''' for (n, time, role, frame, tag, overlay, cap, vo, direction) in SHOTS_META)

    html = f"""<title>Guidde Ad Storyboard</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root {{ --ground:#FCFCFE; --surface:#FFFFFF; --ink:#17161C; --muted:#6C6B77;
    --line:#E2E2EA; --faint:#F1F1F6; --accent:#6D4AFF; --accent-soft:#F1EEFF; }}
  @media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
    --ground:#121116; --surface:#1A1922; --ink:#ECECF2; --muted:#9C9BA8;
    --line:#2C2B37; --faint:#201F29; --accent:#9D89FF; --accent-soft:#211D33; }} }}
  :root[data-theme="dark"] {{ --ground:#121116; --surface:#1A1922; --ink:#ECECF2;
    --muted:#9C9BA8; --line:#2C2B37; --faint:#201F29; --accent:#9D89FF; --accent-soft:#211D33; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--ground); color:var(--ink); line-height:1.5;
    font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; -webkit-font-smoothing:antialiased; }}
  .wrap {{ max-width:1120px; margin:0 auto; padding:48px 24px 80px; }}
  header {{ border-bottom:1px solid var(--line); padding-bottom:26px; margin-bottom:20px; }}
  .eyebrow {{ text-transform:uppercase; letter-spacing:.13em; font-size:12px; font-weight:700; color:var(--accent); margin:0 0 10px; }}
  h1 {{ font-size:clamp(28px,4.6vw,42px); font-weight:800; letter-spacing:-.025em; margin:0 0 10px; text-wrap:balance; }}
  .sub {{ color:var(--muted); font-size:15.5px; margin:0; max-width:66ch; }}
  .specs {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:18px; }}
  .specs span {{ font-size:12.5px; font-weight:600; color:var(--ink); background:var(--faint);
    border:1px solid var(--line); border-radius:999px; padding:5px 11px; }}
  h2 {{ font-size:13px; text-transform:uppercase; letter-spacing:.09em; color:var(--muted);
    font-weight:700; margin:44px 0 16px; }}

  .refintro {{ font-size:14px; color:var(--muted); margin:0 0 16px; max-width:78ch; line-height:1.55; }}
  .refintro i {{ color:var(--ink); font-style:italic; }}
  .ref {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }}
  .ref4 {{ grid-template-columns:repeat(4,1fr); }}
  .ref figure {{ margin:0; background:var(--surface); border:1px solid var(--line); border-radius:14px; overflow:hidden; }}
  .ref img {{ display:block; width:100%; height:auto; }}
  .ref figcaption {{ font-size:12.5px; color:var(--muted); padding:10px 13px; }}
  .ref b {{ color:var(--ink); }}
  .note {{ font-size:12.5px; color:var(--muted); margin:14px 0 0; }}

  .strip {{ display:grid; grid-template-columns:repeat(3,1fr); gap:22px; }}
  .shot {{ background:var(--surface); border:1px solid var(--line); border-radius:16px; padding:14px; display:flex; flex-direction:column; gap:12px; }}

  .phone {{ position:relative; width:100%; aspect-ratio:9/16; border-radius:20px; padding:7px;
    background:linear-gradient(160deg,#2a2a30,#101014); box-shadow:0 10px 30px -18px rgba(0,0,0,.6); }}
  .screen {{ position:relative; width:100%; height:100%; border-radius:14px; overflow:hidden; background:#000; }}
  .ph {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
  .notch {{ position:absolute; top:13px; left:50%; transform:translateX(-50%); width:34%; height:6px; border-radius:99px; background:rgba(0,0,0,.4); z-index:6; }}
  .ptag {{ position:absolute; top:9px; left:9px; z-index:5; font-size:10px; font-weight:700; letter-spacing:.03em;
    background:rgba(20,18,30,.66); color:#fff; padding:3px 8px; border-radius:999px; text-transform:uppercase; }}
  .cap {{ position:absolute; left:7%; right:7%; bottom:8%; z-index:5; text-align:center;
    color:#fff; font-weight:800; font-size:13px; line-height:1.28; text-wrap:balance;
    text-shadow:0 1px 4px rgba(0,0,0,.85), 0 0 2px rgba(0,0,0,.95); }}

  .meta {{ display:flex; flex-direction:column; gap:7px; }}
  .tophdr {{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; }}
  .num {{ font-size:11px; font-weight:800; letter-spacing:.05em; color:var(--accent); }}
  .time {{ font-size:11px; font-weight:600; color:var(--muted); font-variant-numeric:tabular-nums; }}
  .role {{ font-size:10.5px; font-weight:700; text-transform:uppercase; letter-spacing:.04em; color:var(--ink); background:var(--accent-soft); padding:2px 8px; border-radius:999px; }}
  .onscreen {{ margin:0; font-size:14px; font-weight:700; line-height:1.35; text-wrap:balance; }}
  .vo {{ margin:0; font-size:12.5px; color:var(--muted); font-style:italic; }}
  .vo span {{ font-style:normal; font-weight:800; font-size:9.5px; letter-spacing:.05em; color:var(--accent); margin-right:5px; }}
  .dir {{ margin:2px 0 0; font-size:12px; color:var(--muted); line-height:1.45; }}

  .adcopy {{ display:flex; flex-direction:column; gap:14px; background:var(--surface); border:1px solid var(--line); border-radius:16px; padding:20px 22px; }}
  .acrow {{ display:grid; grid-template-columns:2fr 1fr; gap:14px 24px; }}
  .ack {{ font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.06em; color:var(--accent); }}
  .acv {{ margin:5px 0 0; font-size:15px; line-height:1.5; }}
  .acv.body {{ white-space:pre-line; }}
  footer {{ margin-top:44px; padding-top:22px; border-top:1px solid var(--line); color:var(--muted); font-size:13px; }}
  footer b {{ color:var(--ink); }}
  @media (max-width:560px) {{ .acrow {{ grid-template-columns:1fr; }} }}
  @media (max-width:900px) {{ .strip {{ grid-template-columns:repeat(2,1fr); }} .ref4 {{ grid-template-columns:repeat(2,1fr); }} }}
  @media (max-width:560px) {{ .strip, .ref {{ grid-template-columns:1fr; }} .ref4 {{ grid-template-columns:repeat(2,1fr); }} }}
</style>
<div class="wrap">
  <header>
    <p class="eyebrow">Creative deliverable · for Guidde</p>
    <h1>The ad Guidde should run</h1>
    <p class="sub">A six-shot UGC storyboard that reruns the winning competitor ad's exact move:
      a solo car-POV recommendation monologue (Scribe, the ad the scoring actually crowned), with a
      quick screen-recording insert and a free-to-start kicker. Same car setting and same
      enthusiastic register, only the creator, the wording and the product are Guidde's.</p>
    <div class="specs"><span>9:16 vertical</span><span>~30 seconds</span><span>UGC, one creator, in-car</span>
      <span>Sound-on, muted-legible</span><span>Prospecting</span></div>
  </header>

  <h2>The formula we're adapting: the real winning ad</h2>
  <p class="refintro">The winning Scribe ad (Library ID 1737809570795386, confirmed from its own video
    file) is a solo <b>car-POV monologue</b>: a creator to camera, <i>“POV you wasted too much time
    not knowing this exists,”</i> talks up how much it does, cuts once to a laptop screen recording,
    and lands on <i>“but it's free.”</i> The written copy carries the documentation angle; the video
    sells relatable enthusiasm. Frames below are from that actual ad.</p>
  <div class="ref ref4">
    <figure><img src="{_b64(SHOTS / 'carc_hook.jpg')}" alt="winner hook frame">
      <figcaption><b>Hook.</b> “POV you wasted too much time not knowing this exists.”</figcaption></figure>
    <figure><img src="{_b64(SHOTS / 'carc_relate.jpg')}" alt="winner relatable frame">
      <figcaption><b>Relatable.</b> Enthusiastic to-camera recommendation, no ad polish.</figcaption></figure>
    <figure><img src="{_b64(SHOTS / 'carc_product.jpg')}" alt="winner product frame">
      <figcaption><b>Product beat.</b> One quick cut to a laptop screen recording.</figcaption></figure>
    <figure><img src="{_b64(SHOTS / 'carc_value.jpg')}" alt="winner value frame">
      <figcaption><b>Kicker.</b> Back to camera, lands on “but it's free.”</figcaption></figure>
  </div>

  <h2>The full ad</h2>
  <div class="adcopy">
    <div class="ac"><span class="ack">Hook (on-screen, 0:00)</span>
      <p class="acv">“{AD_COPY['hook']}”</p></div>
    <div class="ac"><span class="ack">Primary text (the post body)</span>
      <p class="acv body">{AD_COPY['body']}</p></div>
    <div class="acrow">
      <div class="ac"><span class="ack">End card</span><p class="acv">“{AD_COPY['endcard']}”</p></div>
      <div class="ac"><span class="ack">CTA button</span><p class="acv">{AD_COPY['cta']}</p></div>
    </div>
  </div>

  <h2>The six shots</h2>
  <div class="strip">{strip}
  </div>

  <footer>
    <b>About these frames.</b> All generated for this concept: the hero creator on Higgsfield
    Soul 2.0, then the same creator carried across shots 2, 3 and 5 by feeding that hero back in as
    a reference image, so it is one person in one car for the whole monologue. The product UI and
    brand card are on a text-capable model. Each frame fixes the beat, the on-screen caption and the
    voiceover, so an editor can shoot or assemble straight from them. The lone product beat is shot 4.
    Copy is original to Guidde; only the winning ad's structure (car-POV hook, enthusiastic
    recommendation, one screen-recording insert, free-to-start kicker) is reused.
  </footer>
</div>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html)
    print(f"[storyboard] wrote {OUT.relative_to(ROOT)} ({len(html)//1024} KB)")


if __name__ == "__main__":
    main()
