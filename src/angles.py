"""
Cross-competitor angle tagging.

The task's repetition signal is "creative repetition ACROSS competitors": an
angle that shows up in multiple competitors' ads is a validated pattern, unlike
one advertiser running many copies of itself. This module tags each ad with the
messaging angles it uses (reading the body AND the DCO card copy), so we can
count how many distinct competitors share each angle.

Tags are keyword-based: transparent and reproducible, if imperfect. The keyword
sets are declared here so they can be audited and tuned.
"""

from __future__ import annotations

import json
import re

# angle -> keyword/phrase patterns (lowercased substring match)
ANGLES = {
    "time_saved": ["save time", "faster", "minutes, not hours", "win back time",
                   "hours a week", "75%", "saves you", "less time", "in seconds"],
    "ai_powered": ["ai ", "ai-", " ai", "artificial intelligence"],
    "problem_hook": ["still ", "stuck", "stop ", "can't", "can’t", "out of office",
                     "?", "tired of", "nobody", "the problem"],
    "async_vs_meetings": ["meeting", "swap meetings", "skip the call", "async",
                          "record and share", "quick update", "video update"],
    "documentation_sop": ["sop", "document", "documentation", "process doc",
                          "training guide", "how-to", "step-by-step", "guide"],
    "onboarding_training": ["train", "onboard", "learner", "teams who train"],
    "repetitive_questions": ["same task", "same question", "keeps asking",
                             "walk people through", "walking people through",
                             "skip the call", "fewer questions"],
    "stat_proof": ["%", "survey", "data", "report", "state of", "trusted by",
                   "ranked", "g2", "winner"],
    "tool_overload": ["too many", "managing tools", "tech stack", "tools instead",
                      "lives in too many places", "workflow"],
}


def tag(text: str) -> set[str]:
    t = (text or "").lower()
    return {a for a, kws in ANGLES.items() if any(k in t for k in kws)}


def ad_text(ad: dict) -> str:
    """All human copy in an ad: body + card titles/bodies (skips DCO templates)."""
    s = ad.get("snapshot", {}) or {}
    parts = []
    b = s.get("body")
    bt = b.get("text") if isinstance(b, dict) else b
    if bt and "{{" not in bt:
        parts.append(bt)
    for key in ("title", "caption", "link_description"):
        v = s.get(key)
        if isinstance(v, str) and v and "{{" not in v:
            parts.append(v)
    for c in s.get("cards") or []:
        for key in ("title", "body"):
            v = c.get(key)
            if isinstance(v, str) and v and "{{" not in v:
                parts.append(v)
    return " \n ".join(parts)


def ad_angles(ad: dict) -> set[str]:
    return tag(ad_text(ad))


# --- Guidde-alternative relevance gate --------------------------------------
#
# Guidde captures a workflow and turns it into professional video documentation
# to train teams. An ad is a "clear Guidde alternative" if it sells any of
# Guidde's OWN use cases (per guidde.com): creating guides / docs / SOPs,
# onboarding, training, customer support / self-serve answers, software
# implementation / rollout, product demos, AI adoption / enablement, and in-app
# guidance. This is wider than pure "how-to guides" and deliberately still
# EXCLUDES async-messaging / meeting-replacement (Loom's positioning, which Guidde
# explicitly is not). Keyword-based, so imperfect, but auditable and tunable.
GUIDDE_ALT = [
    # guides / docs / SOPs / how-to
    "how-to", "how to do", "step-by-step", "step by step", "walkthrough",
    "walk through", "walk people through", "walking people through", "guide",
    "guidance", "get guidance", "while actually doing", "in-app", "documentation",
    "document ", "documenting", "sop", "standard operating", "process doc",
    "screenshots", "instructions", "knowledge base", "knowledge", "playbook",
    "how work gets done", "capture knowledge",
    # onboarding / training / enablement
    "onboarding", "onboard", "train teams", "train your team", "train everyone",
    "train new", "new hires", "training guide", "training video", "tutorial",
    "enablement", "upskill", "scale talent",
    # customer support / self-serve
    "customer support", "support team", "help center", "self-serve", "self serve",
    "instant answers", "deflect", "reduce tickets",
    # software implementation / rollout
    "implementation", "roll out", "rollout", "go-live", "go live",
    # product demos
    "product demo", "demo video", "product tour", "demos in minutes", "high-impact demo",
    # AI adoption / enablement
    "ai adoption", "digital adoption", "software adoption", "drive adoption",
    "actually use the ai", "actually use ai", "use the ai tools",
    # producing / sharing screen content (Loom-style creation, not meeting-replace)
    "notate", "ready-to-share", "create, edit", "capture recordings",
    "presentations", "explain ideas",
]


def is_guidde_alternative(ad: dict) -> bool:
    t = ad_text(ad).lower()
    return any(k in t for k in GUIDDE_ALT)


# --- Guidde-relevance: graded (the Stage 2 winner-picking signal) ------------
#
# is_guidde_alternative() above is a BINARY gate: it decides who gets to compete.
# This function is GRADED: it decides who wins. It scores how central an ad's
# message is to Guidde's OWN job, capturing a real workflow and turning it into
# step-by-step video documentation that teams use to onboard, train and self-serve.
#
# Three tiers, from Guidde's core outward:
#   3 CORE      - the ad is about creating the guide / doc / SOP / how-to itself.
#   2 ADJACENT  - the ad is about the JOB the guide does: onboarding, training,
#                 support deflection, product demos, rollout.
#   1 PERIPHERAL- a neighbouring video / AI-adoption story Guidde touches but is
#                 not really about (async video, meeting-replacement, "use your AI").
#
# An ad scores on its MOST-central message (the highest tier it hits), NOT a sum,
# so a documentation ad outranks a meeting-replacement ad even if the latter
# name-drops more keywords. Keyword-based, so auditable and tunable.
GUIDDE_RELEVANCE = {
    3: [  # CORE: create the guide / doc / SOP / how-to, Guidde's exact output
        "how-to", "how to", "step-by-step", "step by step", "walkthrough",
        "walk through", "walk people through", "walking people through", "guide",
        "documentation", "document ", "documenting", "sop", "standard operating",
        "process doc", "knowledge base", "playbook", "instructions", "screenshots",
        "how work gets done", "capture knowledge", "capture the process", "in-app",
    ],
    2: [  # ADJACENT: the job the guide does, onboard / train / support / demo
        "onboard", "onboarding", "new hire", "new hires", "train", "training",
        "tutorial", "enablement", "upskill", "ramp", "customer support",
        "support team", "help center", "self-serve", "self serve", "deflect",
        "reduce tickets", "product demo", "demo video", "product tour",
        "implementation", "rollout", "roll out", "go-live", "go live",
    ],
    1: [  # PERIPHERAL: neighbouring video / AI story Guidde touches, not about
        "ai adoption", "digital adoption", "software adoption", "drive adoption",
        "actually use the ai", "actually use ai", "async", "record and share",
        "video update", "quick update", "meeting", "swap meetings", "skip the call",
        "presentations", "explain ideas", "notate", "ready-to-share",
    ],
}
RELEVANCE_LABEL = {3: "core Guidde use case", 2: "onboard / train / support",
                   1: "adoption / async (peripheral)", 0: "unclassified"}


# A lead-magnet "guide" is a FALSE POSITIVE for tier-3 core. "The Modern Marketer's
# Guide to X", "get the guide", a downloadable ebook/report, is NOT a step-by-step
# how-to guide (Guidde's product), it just contains the word "guide". When the only
# core signal is such a lead-magnet "guide", it must not score tier 3. Real
# documentation ads are unaffected: they still match tier 3 on "document",
# "step-by-step", "sop", "how-to", "screenshots", etc.
_LEADMAGNET_GUIDE = [
    "get the guide", "download the guide", "download our guide", "free guide",
    "ultimate guide", "'s guide to", "s guide to", "the guide to",
    "modern marketer", "marketer's guide", "marketers guide", "ebook", "e-book",
]


def _is_leadmagnet_guide(t: str) -> bool:
    return any(p in t for p in _LEADMAGNET_GUIDE)


def guidde_relevance(ad: dict) -> tuple[int, str]:
    """(tier, matched term) for the ad's most Guidde-central message; (0, "") if none."""
    t = ad_text(ad).lower()
    leadmagnet = _is_leadmagnet_guide(t)
    for tier in (3, 2, 1):
        for kw in GUIDDE_RELEVANCE[tier]:
            if kw in t:
                # Guard: a bare lead-magnet "guide" is not a core (tier-3) signal.
                if tier == 3 and kw == "guide" and leadmagnet:
                    continue
                return tier, kw.strip()
    return 0, ""


# --- Funnel stage -----------------------------------------------------------
#
# A separate axis from prospecting/retargeting (that is audience temperature).
# This is what the ad is trying to DO. Two stages only:
#   TOFU - awareness / lead-gen (a report, "download the data", a webinar)
#   MOFU - show the solution / how it works (everything else, the product ads)
# We deliberately do NOT split out a BOFU stage: a "Sign up" CTA does not make a
# product ad bottom-of-funnel, so those stay in MOFU with the other product ads.
_TOFU_CTA = {"download", "get offer", "get quote", "sign up for webinar"}
_TOFU_COPY = ["download", "the report", "get the data", "state of", "research",
              "survey", "study", "ebook", "e-book", "whitepaper", "white paper",
              "webinar", "register", "the data on"]


def funnel_stage(ad: dict) -> str:
    s = ad.get("snapshot", {}) or {}
    cta = (s.get("cta_text") or "").strip().lower()
    text = ad_text(ad).lower()
    if cta in _TOFU_CTA or any(k in text for k in _TOFU_COPY):
        return "TOFU"
    return "MOFU"
