"""
Central configuration for the Guidde competitor-ad-intelligence pipeline.

Every scoping decision lives here in one place so it is easy to audit and defend.
See README.md for the reasoning behind each choice.
"""

# --- Scope: brands ----------------------------------------------------------
#
# We started from a KEYWORD search on all four suggested competitors (see
# discovery_keywords below). That run revealed two things that made the cut for
# us, from data rather than from a guess:
#
#   1. Keyword search is polluted. "Loom" returns Fruit of the Loom and knitting
#      looms; "Scribe" returns medical AI scribes (Commure, Heidi, MedWriter);
#      "WalkMe" returns language-learning apps. So we resolved each real brand's
#      Facebook Page ID and now collect BY PAGE for clean, complete results.
#   2. Coverage is uneven. WalkMe runs 0 identifiable active FB video ads and
#      Camtasia runs 0 produced video ads (only dynamic catalog ads). They fall
#      out of contention because the data removed them, and that is reported.
#
# Loom advertises its product under its parent "Atlassian" page, so we collect
# the Atlassian page and keep only ads whose creative links to /loom.

BRANDS = [
    {"name": "Scribe",   "page_id": "110376044484488", "link_contains": None},
    {"name": "Camtasia", "page_id": "14531695471",     "link_contains": None},
    {"name": "Loom",     "page_id": "115407078489594", "link_contains": "loom"},
    # WalkMe page id resolved via the Ad Library advertiser typeahead (the
    # keyword "WalkMe" tokenizes to "walk me" and returns junk, so keyword
    # discovery missed it; the advertiser lookup is the reliable path).
    {"name": "WalkMe",   "page_id": "180728395378883", "link_contains": None},
]

# The keyword queries used for the initial discovery pass (documented for repro).
DISCOVERY_KEYWORDS = ["Loom", "Scribe", "Camtasia", "WalkMe"]

# --- Scope: format ----------------------------------------------------------

# ALL formats. The task asks for "the single winning ad," full stop, so Part 1
# (find the best ad) must survey image, video, and carousel, not pre-filter to
# one format. We rank every format together and label each ad's format in the
# output. Which execution we then storyboard for Part 2 is a separate decision
# made AFTER we see the true cross-format winner.
MEDIA_TYPE = "all"

# Do NOT drop DCO here. DCO (Dynamic Creative Optimization) ads have templated
# copy ("{{product.brand}}") and are a poor source for a creative brief, but
# excluding them from the "best ad" measurement would silently narrow the field.
# We keep them in the ranking, label them, and note the storyboard limitation
# if one wins. Set to False = nothing is excluded from contention.
EXCLUDE_DCO = False

COUNTRY = "US"          # Guidde and these competitors run US acquisition ads.
# Scrape ALL statuses (active + inactive). We still only SCORE active ads (the
# is_active gate in rank.py), but the inactive ads are the message's back-history:
# they let us measure how long a message has REALLY run across its re-issued
# versions, instead of just the current version's age (see rank.py true longevity).
ACTIVE_STATUS = "all"

# --- "Best" definition: TWO-STAGE scoring -----------------------------------
#
# Meta hides spend and performance, so we infer "best" in two stages that ask two
# different questions. Stage 1 asks, WITHIN each brand, "which ad has this brand
# most PROVEN?" Stage 2 asks, ACROSS the brand champions, "which is the best ad for
# GUIDDE to rebuild?" — answered by two cross-brand signals combined:
#
#   REPETITION  - how validated the message is ACROSS competitors (the brief's own
#                 "creative repetition across competitors" criterion): the more of
#                 the four rivals share a champion's angles, the more the market has
#                 confirmed the pattern. This is the market's vote.
#   RELEVANCE   - how central the message is to GUIDDE's OWN job (create step-by-step
#                 video documentation to onboard/train/support), graded in tiers.
#                 This is what makes it the best ad *for Guidde*, and it BREAKS TIES
#                 that repetition structurally cannot: the finalists have identical
#                 angle-coverage profiles (one mid- + one high-coverage angle each),
#                 so any function of coverage ties them. Only relevance separates
#                 them on merit. See angles.py.
#
# Both are real weighted terms, so an ad well-validated by rivals AND close to
# Guidde's core wins; repetition alone (brief criterion) never gets dropped, and
# relevance decides when the market's vote is a tie.
#
# THREE GATES first (an ad must pass all to compete):
#   ACTIVE            - the ad must be live today.
#   NOT RETARGETING   - UTM-confirmed retargeting ads are excluded (only Loom tags
#                       its links; those are warm-audience feature reminders).
#   GUIDDE ALTERNATIVE- the copy must sell one of Guidde's own use cases.
#
# STAGE 1 - PURELY WITHIN each brand: pick the brand's champion from its own ads,
# never against competitors (competitors only enter in Stage 2).
#   S1_PERSISTENCE - how many DISTINCT MONTHS the brand re-launched this message
#                    (from the active + inactive message history). This rewards a
#                    message the brand keeps coming back to over time, NOT a message
#                    printed in many simultaneous copies (a blast). Within-brand.
#   S1_LONGEVITY   - days since the message's earliest version (within-brand).
#
# STAGE 2 - the brand champions compete on TWO cross-brand signals (sum to 1.0):
#   S2_REPETITION - cross-competitor angle validation (the market's vote).
#   S2_RELEVANCE  - closeness to Guidde's core job (the tie-breaker on merit).
S1_PERSISTENCE = 0.60
S1_LONGEVITY = 0.40
S2_REPETITION = 0.50
S2_RELEVANCE = 0.50

EXCLUDE_RETARGETING = True
REQUIRE_GUIDDE_ALTERNATIVE = True

# Content-similarity threshold for grouping active + inactive ads into one
# "message" (TF-IDF cosine, see matching.py). Higher = stricter (only near-
# identical copy groups); lower = looser (paraphrases group too). 0.45 chains
# re-issued versions of a message while keeping distinct messages apart.
CLUSTER_THRESHOLD = 0.55

# DCO (dynamic) ads ARE eligible to win. Their top-level copy is a template
# ("{{product.brand}}"), but the real creative lives in the cards (e.g. "Spruce
# up your screenshots"), which carry a genuine hook, angle, format, and CTA. And
# Guidde can run a dynamic ad too, so a DCO winner is a valid, rebuildable output
# (as a dynamic feature-ad concept rather than a linear video storyboard). We
# read the card copy for angles/hooks and let DCO ads compete on equal footing.
DCO_ELIGIBLE = True

# --- Apify ------------------------------------------------------------------

APIFY_ACTOR = "curious_coder~facebook-ads-library-scraper"
# Raised to capture the inactive back-history for the true-longevity signal.
# 4 brands x up to 500 ads ~= about $2 per full run.
MAX_ADS_PER_PAGE = 500
