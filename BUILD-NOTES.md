# news-image-20261120 V4 — BUILD NOTES

Competition: news-image-20261120 — "Sum up 20 November's world news in one image"
Account: @sami07 (wallet FYYrqRhbkk3qEj8megc2Y5c6dMvwAh2ijSeTniXnWgxZ)
Prize: $250 escrowed, top 50 pay. Entries close 2026-11-22T00:00:00Z (Nov 22, 06:00 +06).
Result due 2026-12-06T08:00:00Z.
Build requested by parent 2026-11-21 ~11:13 +06 ("Top 2/3 ay niya jao"). DO NOT SUBMIT — build only, present to user first; parent handles GitHub repo + submit.

## STEP 0 — Quota (checked live 2026-11-21 ~11:14 +06)
can_submit TRUE, day left 5/6, entries_made 2, kept 2, hard left 38. Proceed.

## V3 state (verified live ~11:10 +06)
V3 "The Friday Edition — V3" (01a1fc77-d297-73d6-8c23-9ce14cef2d0c): dev judge 984,446 (977,995–990,897), 12W/0L, rank 311/14,349, prize_rank 310. V1 (982,336) now superseded, off the leaderboard. Top-50 line 989,026. Gap V3→top 3 ≈ 7,206.

## STEP 1 — Top 1–4 analysis, one by one (posters fetched live ~11:15 +06)
- #1 samatch-we 992,057 (35 stories, 7 regions): cream classic. Huge serif "Friday 20 November 2026" masthead, red sub-dek, 6-stat strip (3 bridges / 300,000+ / −6.2% / 100,000 / 2.3% / 118), proportional region bar, 3 rich hero panels with red chips ON panels (Kyiv night scene, Akvan coast+spiral, AI dark chart+4 index rows), hero headlines below in big serif, 10 mids each with a dense drawn panel + red label chip + status/source tag, cream map + 22 briefs, rich date check (left-out + not-yet).
- #2 superskie 991,697 (33 stories): cream. Same masthead grammar. TWO strips: "THE DAY IN UTC" (7 timed moments) + "THE DAY IN NUMBERS" (111 missiles, 3 bridges, 372,000 evacuated, −3.7%, −14%, 60.7%). 3 heroes with yellow chips. 10 mids with panels + status tags top-right. Status-tag LEGEND (CONFIRMED 2+ outlets / OFFICIAL / REPORTED). Richest date check (left-out list + not-yet list).
- #3 888dao-sats 991,652 (36 stories, 6 continents): cream. Italic red sub-dek. 6-stat strip. Region ribbon + "ALL STORIES: FRI 20 NOV 2026, ANY TIME ZONE". 3 heroes (Akvan spiral, Kyiv ~30 missiles, COP31 globe+thermometer). 10 mids with panels + small tags. DARK navy map with tan continents, pins 1–13. 23 briefs. Date check (Thursday list).
- #4 kiencx 991,429 (33 stories, 13 drawn): cream. 6-stat strip (3 killed / 300,000+ / −4.9% Nikkei / 0 fossil-fuel mentions / 2.2% core CPI / 46 ships). "33 STORIES BY REGION" bar. 3 heroes (Kyiv, Akvan, AI intraday lows). 10 mids with panels + label chips. Cream map + 20 briefs. Date check with "not shown because it had not happened at press time" (COP31 outcome, Asia closing prices).

## Diagnosis — what V3 lacks vs all four leaders
1. LOOK: all four leaders are cream broadsheets with a black serif masthead. V3 is navy "night edition". V1→V3 gained only +2,110 while keeping navy — the cream grammar is the single most consistent difference between V3 (984,446) and the top 4 (991,429–992,057).
2. HEROES: leaders have 3 tall (~150–190px) scene-rich panels. V3 has 4 shorter (112px) panels; the 4th (Mercury, "arrives tomorrow") is a Saturday story as a hero — leaders put BepiColombo in the DATE CHECK "not yet" section instead. Date discipline is a stated judging dimension.
3. DATE CHECK: leaders' is two-part and detailed (left-out list + not-yet list). V3's is one line.
4. STATUS LEGEND: #2 explains its tags (CONFIRMED / OFFICIAL / REPORTED). V3 has tags but no legend.
5. STORY COUNT: leaders 33–36; V3 has 40. Density alone does not win (V2 lesson) — 40 stories crowd the briefs.
6. TIMELINE: #2's UTC timeline is a strong element V3's five-moment band only partly matches.

## DECISION: BUILD V4 — cream broadsheet, same verified facts, top 2–3 the target
- Cream paper, black serif masthead, red sub-dek, 6-stat strip, proportional region bar — the leaders' grammar.
- 3 tall heroes (Kyiv, Akvan, AI) at ~130px panels; UK–EU reset becomes mid #4. Mercury demoted to the date check "NOT YET".
- 35 stories (3 heroes + 10 mids + 22 briefs), 7 regions (EUROPE 7 · ASIA 11 · MIDDLE EAST 3 · AFRICA 3 · AMERICAS 5 · OCEANIA 1 · GLOBAL 5).
- Seven-moment timeline band (verified local times + AFTERNOON/EVENING/NIGHT for the two un-timed ones).
- Keep V3's differentiators no leader has: RECORDS OF THE DAY strip (4 records), status tags on every story + a status legend in the footer.
- Two-part date check (LEFT OUT / NOT YET), longer than V3's.
- All 35 facts are V3's verified set — no new stories, no new searches. Four V3 briefs fold into mid/hero decks (US chips→Nvidia, Akvan teams→Akvan hero, Poland jets→Poland mid, COP31 "35 by 35" dropped with the deck trim).
- Honest target: top 10 is realistic if the cream grammar is what the judge rewards; top 2–3 needs the judge to rate V4's craft (timeline + records + legend + date discipline) above #2/#3. No rank is promised — the judge grade decides.

## Files (all written fresh in-session, then frozen)
LICENSE (kit starter copy), .makefun/owner.json (wallet FYYr...), render.py (fresh PIL renderer — new file, NOT a copy of V3's render.py), main.ts (fresh, copies entry.png), package.json ({"type":"module"}), README.md (fresh, three live make.fun badges for repo news-image-20261120-v4 + bounty link + ref 7b8zsyv7), entry.png (generated by render.py in-session), BUILD-NOTES.md (this log).
- `makefun record` refuses for this competition ("does not take recorded transcripts") — bundle route, as in V2/V3. Kit: ~/workspace/makefun/news-image-20261120-v2-kit/ (level 29).
- Route: NEW GitHub repo sami30357/news-image-20261120-v4 (does NOT pre-exist; creation/upload + About via live browser by parent). About MUST be set before submit (website https://make.fun/bounty/news-image-20261120, topics makefun, ai-agents, bounties, growth). README carries the three live badges for the v4 repo.

## Build results (2026-11-21 ~11:21 +06)
- render.py written fresh in-session (~700 lines: helpers + story data + 3 hero panels + 10 mid panels + map + layout) + 1 fix round (final y 1047→1015: stat strip taller, hero/mid panels trimmed, AI chart line kept out of the index rows, CPI ¥ removed for a +2.3% tag, pins r=6, three truncating lines shortened).
- Poster: 1024x1024 RGB PNG, 185,278 bytes (< 1 MiB). Thumbnail check (256px): masthead + hero headlines + stat numbers legible; mid panels read as illustrated blocks with red label chips; map reads as tan continents with red pins.
- Remaining known nits: Europe map pins cluster (Kyiv/Antalya 9px apart at true positions); a few brief sources truncate with "…" (line width 248px).
- main.ts written fresh in-session. package.json {"type":"module"} added (silences the Node typeless-package warning).
## Verification results (2026-11-21 ~11:23 +06)
- Local commit: 90092133937e1b08a4e248ccefaa60a96ed37bf9, tree clean. Files: LICENSE, .makefun/owner.json, BUILD-NOTES.md, render.py, main.ts, package.json, README.md, entry.png.
- Grader sim: `node main.ts` as user nobody on a read-only repo copy — exit 0 twice, byte-identical output, sha256 5b5a340c72709599946df9fcd72200e4b5d6beef6254de98a3aecb285158b7e9 (matches repo entry.png). (First attempt failed MODULE_NOT_FOUND: the /tmp parent dir was drwxrwx---; fixed with chmod 755 on the parent.)
- Bundle: ~/workspace/makefun/news-image-20261120-v4-transcripts.tar.gz, 678,177 bytes, sha256 fcbe55ae36851567f103a3e957b2992cd9277ba29f6864a1108ae9543009d90e. 4 sessions discovered by repo dir (mine 568647e4 + parent 1e65f974 + V3 builder 940b0ce2 + V2 builder d123f5f1 as read-source sessions — I read V3's BUILD-NOTES.md + README.md for context). Prompt "Top 2/3 ay niya jao", handed-off. ⚠️ Only 11 usage records attached (parent's) — my session's usage row is written only when my run completes. PARENT MUST re-run the muse.db SELECT (agent ids 568647e4-9174-46bb-befc-3a21c25bf89b + 1e65f974-9b6d-4ce2-a750-21828d5508f3 + 940b0ce2-ce39-4ea2-83b8-ac967796e7cd + d123f5f1-1255-4c93-8ff0-5009ddfb962d) and RE-BUNDLE before submitting.
- Kit check (local, commit 9009213): **13 pass / 0 fail / 6 skip / 5 "submission"** (repo_public, repo_owner, repo_created_after_open, commit_in_repo, duplicate_snapshot — can only pass after the GitHub repo exists + is pushed). thinking_reproduces **99.3%** (762/767 authored, 0 copied, 0 pasted, 0 read, 5 absent; main.ts 6 authored lines). thinking_revised pass (render.py from 19 write/edit messages). thinking_priced pass (11 usage records). thinking_turns 170 ≥ 5. competition_open pass. entrypoint pass. license_osi pass. snapshot pass. thinking_own_work SKIP with a note (sessions fetched the top-4 leaders' artifact.webp posters for analysis — allowed, never a rejection).
- ⚠️ PARENT STEPS BEFORE SUBMIT (after user go-ahead): (1) create GitHub repo sami30357/news-image-20261120-v4 via live browser, upload the 8 files, set About (website https://make.fun/bounty/news-image-20261120, topics makefun, ai-agents, bounties, growth) BEFORE submit; (2) re-run the usage SELECT + re-bundle with the NEW GitHub HEAD commit SHA; (3) re-run the kit check on the fresh bundle; (4) submit from the kit cli dir.
- Submit command (after the steps above, with the fresh GitHub HEAD SHA and fresh bundle):
  cd ~/workspace/makefun/news-image-20261120-v2-kit/cli && node makefun.mjs submit --competition news-image-20261120 --repo-url https://github.com/sami30357/news-image-20261120-v4 --commit <NEW-GITHUB-SHA> --bundle ~/workspace/makefun/news-image-20261120-v4-transcripts.tar.gz --keypair ~/workspace/makefun/makefun-keypair.json --json
  (Suggested title: "The Friday Edition — V4".)
- Honest assessment: V4 matches the leaders' winning grammar (cream broadsheet, black serif masthead, 3 tall heroes, 6-stat strip, proportional region bar) while keeping V3's differentiators (seven-moment timeline, RECORDS OF THE DAY, status legend, two-part date check) and fixing V3's date-discipline gap (Mercury is a Saturday story — now in the date check, not a hero). Top 10 is realistic if the cream grammar is what the judge rewards; top 2–3 needs the judge to rate V4's craft above #2/#3. No rank is promised — the judge grade decides.
- DO NOT SUBMIT without the user's explicit go-ahead.
