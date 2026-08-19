# Demo video script (record with Guidde) — ~7 minutes

Format: screen recording + your voiceover. Timecodes are guides. `[SHOW]` = what's on screen, `[SAY]` = what you say. The heart of this is the reasoning, most of the time goes to how "best" is defined and why the winner won.

---

## 0:00-0:50 — What it is, and why the competitors aren't comparable as-is

`[SHOW]` The four brands, then the run report.

`[SAY]` "The brief: find a competitor's best Facebook ad and rebuild it as a creative brief and storyboard for Guidde. First thing I hit, the four competitors don't do the same thing. Scribe makes step-by-step documentation, which is closest to Guidde. Loom is async video messaging, basically replacing meetings. Camtasia is screen-recording and video editing. WalkMe is a digital-adoption platform that mostly runs lead-gen report ads. So you can't just line their ads up and rank them, half of them aren't even selling a Guidde-type product. That's the first filter: I only keep ads that sell one of Guidde's own use cases, checked against guidde.com. Everything after that is comparing like with like. And for every ad that clears the filter, I pull exactly what the brief listed per ad, the hook, the messaging angle, the format, image, video or carousel, the CTA, and how long it's been running. That's the raw table, `ranked.csv`, one row per ad, and the scoring is built on those fields."

## 0:50-1:40 — There's no 'best' button, and I focus on prospecting

`[SHOW]` The "How it was scored" section.

`[SAY]` "The core challenge: Meta hides spend and performance, so 'best' isn't something you look up, it's something you define and defend. Two scoping calls up front. One, I focus on **prospecting** ads, cold audience, not retargeting, because a retargeting ad is a warm-audience reminder, a totally different job, and the wrong thing to copy for a new-customer ad. I can actually tell them apart because Loom is the only brand that tags its links with retargeting tracking codes; the others don't tag at all, so I treat those as cold-audience. Two, everything the tool decides, which brands, how much each signal counts, the cutoffs, lives in one settings file I can open and change. Nothing hidden, nothing hard-coded. That's what makes every choice defensible: you can see each line I drew and move it."

## 1:40-2:40 — Two funnel lanes, and why I chose the product lane

`[SHOW]` The MOFU and TOFU sections of the report.

`[SAY]` "Ads also do two different jobs, and I split them so they don't compete unfairly. **TOFU** is awareness and lead-gen, 'download the report.' **MOFU** is product, 'here's how it works.' If you rank them together, a lead-gen ad and a product ad fight on totally different terms. So each lane crowns its own winner. WalkMe actually wins the awareness lane, it runs a ton of report ads, and that's a real result. But I go with the **product-lane winner**, because that's the ad Guidde should rebuild, a product ad you can adapt into a Guidde ad. And to be clear, this same machine would run just as well for the awareness lane, or for retargeting ads, or for any single brand, it's the same two rounds, just pointed at a different slice."

## 2:40-4:10 — The scoring, every number and why

`[SHOW]` The Stage 1 and Stage 2 tables.

`[SAY]` "Now the actual scoring, in two rounds.

**Round one judges each brand against only its own ads**, to answer 'which is this brand's most-proven ad.' Two signals: persistence, weighted 0.6, and longevity, weighted 0.4. Persistence is how many separate months a brand keeps re-launching the same message, and it's the heavier signal on purpose, a brand that keeps coming back to a message over months is the strongest sign it works. Longevity, days running, is 0.4, supporting evidence, not the main event. And I deliberately did *not* score by counting copies, because a brand can blast a hundred copies of one ad in a single day and that's noise, not staying power.

**Round two takes only those brand-champions** and asks which wins overall. Two signals, 0.5 and 0.5. Repetition: how many rivals run the same angle, the brief's own criterion, a message everyone copies is validated. Relevance: how close the message is to what Guidde actually does. Equal weight because both genuinely matter, one is 'the market likes it,' the other is 'it fits Guidde.' The alternative I tried first was repetition only, and I'll show you in a second why that failed."

## 4:10-4:55 — Why the winner won, and why the others lost

`[SHOW]` The Round 2 table, three finalists side by side.

`[SAY]` "Here's the payoff. The three product finalists, Scribe, Camtasia, Loom, **tie exactly on repetition**, they all have the same angle-shape. Repetition literally can't separate them. Relevance is what breaks it, and it breaks it on merit. Scribe's ad is about turning your work into documentation automatically, that's dead-center on Guidde, top score. Camtasia's is a training ad, close but not the core, second. Loom's is replace-your-meetings, which is Loom's whole identity and the one thing Guidde explicitly is *not*, so it comes last. That's why the winner is Scribe's 'The part nobody puts on the job description', it's Scribe's most-proven ad, its angle is validated across rivals, and it's the closest of anyone to Guidde. All three line up.

*(The 'trouble': that repetition-only tie is what told me repetition measures popularity, not fit, so I added the relevance signal. One line, then move on.)*"

## 4:55-6:00 — Part 2: the winner, rebuilt for Guidde

`[SHOW]` The real winning ad (its frames), then `01_winner_analysis.md`, then the storyboard artifact and the full ad copy, then play the produced video.

`[SAY]` "Part two. Here's the actual winning ad, a real person in a car, phone-selfie, talking to camera, 'you wasted time not knowing this exists.' I tear it down, hook, angle, structure, then rebuild it for Guidde as a full ad. Same concept on purpose: a UGC car monologue, so it inherits what already works, but adapted, two people instead of one, a British accent, and Guidde's real features from their site, capture any workflow, AI voiceover, 40-plus languages, share with one link. And it's a *full* ad, not just a video: here's the hook, 'Being the one who knows how everything works is a second full-time job'; the post caption; the call to action, Try For Free; and the end card. Then the finished video." `[play it]` "Side by side, you can see it: the winner is a car, ours is a car, same idea, adapted."

## 6:00-6:30 — Cost per run

`[SHOW]` README, the "External providers, credentials & cost" table.

`[SAY]` "On cost, I split it in two. Part 1, the analysis, is about a dollar a run, that's just the Apify scrape, four brands, under a thousand ads; the scoring itself is deterministic Python with zero API cost. Part 2, the creative, is generated on Higgsfield through Claude, images at roughly 0.12 credits each, video at about 27.5 credits per five seconds, so around 100 credits for one ad, roughly six frames plus a single ~18-second clip. The two halves are separate, the whole analysis runs on just an Apify token, no Higgsfield needed."

## 6:30-7:15 — Where it breaks, and 10x

`[SHOW]` README, failure + scaling sections.

`[SAY]` "Honest limits: 'best' is a defended inference, not a measured fact, because Meta hides performance. The tagging is keyword-based, transparent but not perfect. And the same framework I ran for prospecting product ads, I'd run separately for retargeting or for the awareness lane, they each deserve their own winner. At ten times the volume, two things bind, the scrape, which I'd queue and cache so re-runs only fetch what's new, and the ad-grouping step, which is quadratic today and would move to vector search. That's the pipeline, and that's why the winner is the winner."

---

### Delivery notes
- Spend your time on 1:40-4:55, the lanes, the weights and their reasons, and why each competitor won or lost. That's the graded thinking.
- Keep 'best' framed as *defined and defended*, never looked-up.
- On Part 2, actually show the hook, the caption and the CTA on screen, not just the video, and land the "winner is a car, ours is a car, adapted" line.
