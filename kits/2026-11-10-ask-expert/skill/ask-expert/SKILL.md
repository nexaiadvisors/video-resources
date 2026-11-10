---
name: ask-expert
description: "Answers a question from your 'YT:' NotebookLM notebooks (each one holds the best creators' videos on one topic), after checking that the chosen notebook has videos from the last 7 days on the question's subject and adding new ones if not. Use for /ask-expert <question>, 'ask the expert', 'what do the experts say about X', 'review this draft against the experts'."
argument-hint: "<question> [--notebook \"YT: Topic\"] [--days 7] [--no-refresh]"
---

# Ask expert

## Overview

You keep one NotebookLM notebook per topic, named `YT: <Topic>` (for example `YT: Cold Outreach`).
Each holds YouTube videos from the creators you trust on that topic. This skill picks the notebook
that covers a question, makes sure it is current, asks it, and answers with the videos each point
came from. A stale notebook gives an old answer that still sounds confident, so freshness is
checked before every question.

Needs: the `nlm` CLI (`uv tool install notebooklm-mcp-cli`, then `nlm login`). Optional:
`YOUTUBE_API_KEY` for fast upload-date lookups; without it `yt-dlp` is used.

Keep every command's output in a run folder: `RUN=./ask-expert-runs/<YYYY-MM-DD>-<question-slug>/`.

## Steps

### 1. Pick the notebooks

`nlm notebook list --json > RUN/notebooks.json`. Choose the one `YT:` notebook whose topic best
covers the question. Add a second only when the question clearly spans two topics.
`--notebook` overrides the choice. If no `YT:` notebook fits, say so and offer to build one
(create it with `nlm notebook create "YT: <Topic>"`, then fill it as in step 3). Never answer from
an unrelated notebook.
Done when: 1-2 notebooks are named with one line on why each fits, or the gap is reported.

### 2. Check freshness

For each notebook:
`python3 scripts/freshness.py --notebook <id> --days 7 --out RUN/fresh-<slug>.json`
It lists the notebook's videos with upload dates and ranks the creators by how many videos each has.
Then judge the topic, not only the date. Read the `recent` titles. The notebook is current for this
question only if at least one video from the last 7 days is on the question's subject.
Done when: each notebook is marked current or stale for this question, with the newest relevant
video's title and date (or "none in 7 days").

### 3. Refresh a stale notebook

Skip with `--no-refresh`, and say the answer may be dated. Otherwise:
- Find up to 2 recent long-form videos (no Shorts) on the question's subject from each of the top 5
  creators in the freshness file, plus 2-3 new creators found by searching YouTube for the subject.
- If nobody posted on the subject in 7 days, widen to 14 days, then 30, and say so.
- Add them: `nlm source add <id> --youtube <url> --youtube <url> --wait`.
- Report any source that fails to load.

Done when: new videos were added and finished loading, or the report says why none were.

### 4. Ask

`nlm notebook query <id> "<question>" --json --new-conversation --timeout 240 > RUN/answer-<slug>.json`.
With two notebooks, query each one separately so each answer keeps its own citations. Append to
the question: "Name the videos and creators each point comes from, and say plainly what the
sources do not cover."
Done when: each query returned success, or the error is reported.

### 5. Answer

Lead with the answer in plain words. Then:
- each claim's source: the video title linked to its YouTube URL, and the creator;
- freshness: per notebook, current, refreshed (with the videos added), or stale and why;
- gaps: what the notebooks said they do not cover. If the question needs that gap filled, use web
  search and label that part "from the web, not the notebook".

End with a recommendation when the question asks for one.
Done when: every claim has a source or the web label, and freshness is stated.

## Drafting outreach with it

The pattern that works: ask the notebook for the rules first, then draft, then ask it to review.
1. Ask: "What do the experts say makes a cold [email / DM / follow-up] to [audience] get a reply?
   Length, structure, opener, ask, follow-up timing."
2. Have your agent draft the message from those rules plus real facts about the recipient.
3. Ask again with the draft pasted in: "Review this draft against the experts. What would they cut
   or change?"
4. Revise and repeat 2-3 times until it reads like you wrote it to one person. The human reads
   and sends every message.
