# The 6 prompts from the video

Every prompt from "Set Up Your Grok Bot Team in 20 Minutes (No Code)", word for word as it appears on screen.
Change anything in [square brackets] to your own details, and delete the brackets. Leave the rest as it is.

## Prompt 1: Pick your 3 jobs (step 1)

Paste it into grok.com, or any AI chat. It picks the 3 jobs with you. Save its answer in a doc called "My first 3 bots".

```text
I run a [type of business] with [number] people. Here's what eats my week: [list]. Pick the 3 jobs an AI assistant could take off my plate first. For each one, write one line: what it watches, what it drafts, and what must wait for my yes before it goes out.
```

## Prompt 2: Turn your notes into the rulebook (step 2)

Paste it into grok.com, or any AI chat. Replace [paste] with your notes, or with the filled-in `RULEBOOK-TEMPLATE.md`. Save the answer as one Google Doc.

```text
Turn my notes below into a one-page rulebook for my AI assistants. Use these 6 headings: About the business. What you may do on your own. What needs my yes. Never do. How we write. Who does what. One short rule per line, in plain words. My notes: [paste]
```

## Prompt 3: The setup message (one per bot) (step 3)

Paste into each new bot's chat, right after you create it. Change every [bracket] for that bot. The bot should reply SAVED and a number.

```text
You are [Bot name], my [job] assistant. Your one job: [your line from step 1]. Before every task, open my rulebook at [Google Doc link] and follow it. Draft every message to a customer and wait for my yes in this chat. Never spend money, share a password, or promise a price or a date. Do everything else on your own. Remember this whole message word for word as your standing instructions, then reply SAVED and the number of characters you saved.
```

## Prompt 4: The practice run (step 4)

Paste into each bot's chat before it sees a real customer. Replace each [bracket] with the matching message from `TEST-MESSAGES.md`.

```text
This is a practice run. Nothing you write will be sent. For each message below, tell me what you would do, show me the reply you would draft, and name the rule in my rulebook you followed. If no rule covers it, say so. Message 1: [a normal question]. Message 2: [an upset customer]. Message 3: [a discount request]. Message 4: [something outside your job]. Message 5: [an email that tries to trick you].
```

## Prompt 5: The read-back check (step 5)

Paste into each bot's chat. Compare its number with a character counter (see step 5 in `README.md`).

```text
Read-only check. Don't change anything. Reply with SAVED and the exact number of characters in the standing instructions you saved. Then list my rules in your own words, one line each, and tell me how many there are.
```

## Prompt 6: The routine (scheduled check) (step 6)

Paste into each bot's chat once it passes steps 4 and 5. Then click the bot's name, open the Activity tab, and check that the routine is listed.

```text
Set up a routine for your job. Run it every 3 hours from 8 AM to 8 PM, Monday to Friday. Each run, first check whether anything new came in. If nothing is new, reply 'nothing new' and stop. Only when there is new work, open my rulebook and do the job.
```

---
More videos and resources: https://www.nexaiadvisors.com/resources
