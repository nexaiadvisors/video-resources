# Gesture library: which gesture goes with which words

Use this when writing the cue file for `talk_longcat.py`: read the script, find the trigger phrases, and write one cue
line per gesture.

## How to choose cues from a script

1. Read the whole script and mark every phrase that matches a trigger in the table below.
2. **Lists come first, and they must be complete.** If the script says "first ... second ... third", cue all of them
   (one, two, three fingers). A clip that shows one finger on "first" and nothing on "second" and "third"
   looks like a mistake.
3. Keep the rest sparse. Aim for at most one gesture per sentence and about one every 5 to 8 seconds. Most of the clip
   should be the resting prompt. Coaches and the research agree that a gesture should clarify the words, not run all
   the time.
4. Prefer the gesture that shows the meaning (a count, a size, a contrast) over a generic emphasis beat.
5. Check spacing: `talk_longcat.py` needs 2.5 s between cues and 1 s of talking before the first one. When two triggers
   are closer than that, keep the one that carries more meaning.
6. Read the cue list back (phrase and gesture) before rendering. A render is slow, so catch mistakes on paper.
7. After rendering, make a frame sheet (5 frames per second) around each cue and check the hand shape. A wrong finger
   count is fixed by re-rendering that one segment with another seed.

## How to write the gesture sentence

- Write an **action with a start, a hold and a return**: "raises ..., holds it for a moment, then lowers his hand back
  to his lap." A pose ("talks with his hand on his chest") does nothing.
- Name the hand ("his right hand") and say what the other hand does only if it matters. Left alone, the other hand
  stays at rest.
- Say where the hand ends ("back to his lap" for a seated look, "back to his side" for a standing look).
- For a finger count, name the fingers that are up and say the others are closed.
- The cue phrase is the first word of the trigger ("First", "I have"). The script starts the gesture segment 0.2 s
  before that word and the hand arrives about 0.3 s after the word starts. This timing looked right in testing.

## The table

Status: **Tested** means it was rendered and judged good. **Seed-sensitive** means it rendered correctly only with some
seeds. **Untested** means the sentence follows the tested pattern but has not been rendered.

| Meaning | Trigger words in the script | Gesture sentence for the cue file | Status |
|---|---|---|---|
| Personal admission, sincerity | "I have", "honestly", "I believe", "for me", "I care", "from my experience" | He raises his right hand and places his open palm flat on the centre of his chest, holds it there for a moment, then lowers it back to his lap. | Tested |
| List item 1 | "first", "number one", "one reason", "the first thing" | He raises his right hand and points his index finger straight up to show the number one. Only one finger is extended; his other fingers are curled into a fist. He holds it for a moment, then lowers his hand back to his lap. | Tested, seed-sensitive (seed 7 gave one finger, seed 42 gave two) |
| List item 2 | "second", "number two", "two things" | He raises his right hand and holds up two fingers, his index and middle finger, with his palm facing the camera and his other fingers closed. He holds it for a moment, then lowers his hand back to his lap. | Untested (the model made this shape by itself) |
| List item 3 | "third", "and third", "number three", "three reasons" | He raises his right hand and holds up three fingers, his index, middle and ring finger, with his palm facing the camera and his thumb holding down his little finger. He holds it for a moment, then lowers his hand back to his lap. | Untested |
| Announcing a count | "three things", "two options", "five steps" | The same finger shape as the number said. | Untested |
| Precision, the key detail | "exactly", "the key point", "one detail", "specifically" | He raises his right hand with his thumb and index fingertip pressed together in a small pinch, gives one short downward tap in the air, then lowers his hand back to his lap. | Untested |
| Emphasis | a stressed claim, "this matters", "never", "always" | He raises his right hand, open and edge-on, and makes one short firm downward chop in front of his chest, then lowers his hand back to his lap. | Untested |
| Big, growing, a lot | "huge", "massive", "grew", "all of", "everything" | He raises both hands and moves them apart to shoulder width, palms facing each other, holds for a moment, then lowers both hands back to his lap. | Untested |
| Small, shrinking, a little | "tiny", "small", "just a bit", "shrinks", "ten minutes" | He raises his right hand and holds his thumb and index finger a few centimetres apart to show a small amount, holds for a moment, then lowers his hand back to his lap. | Untested |
| Contrast, two options | "on one hand ... on the other", "this, not that", "versus", "before and after" | He raises his left hand, palm up, to his left side, then raises his right hand, palm up, to his right side, as if weighing two options, then lowers both hands back to his lap. | Untested (needs both phrases inside one 3.7 s segment, or two cues) |
| Sequence, timeline | "then", "next", "after that", "from ... to", "over time" | He raises his right hand and moves it in one smooth step from his left to his right at chest height, then lowers it back to his lap. | Untested |
| Offering, explaining, inviting | "here's what I learned", "let me show you", "consider", "imagine" | He raises both hands slightly with open palms turned up toward the camera, holds for a moment, then lowers them back to his lap. | Untested |
| You, the viewer | "you", "your", "all of us", "we" | He raises his right hand, open with the palm up, and extends it toward the camera in a small offering motion, then lowers it back to his lap. | Untested (open hand, never a pointed finger) |
| Putting together | "combine", "together", "connect", "fits", "the whole picture" | He raises both hands apart, then brings them together until his fingers interlock in front of his chest, holds for a moment, then lowers them back to his lap. | Untested |
| Not sure | "I don't know", "maybe", "who knows", "it depends" | He lifts both shoulders slightly and turns both palms up beside his lap in a small shrug, then relaxes. | Untested |
| No, stop, caution | "don't", "stop", "wait", "never do this", "careful" | He raises his right hand with his open palm facing the camera at chest height, holds it still for a moment, then lowers it back to his lap. | Untested (use rarely: it reads as confrontational) |
| Surprise | "this one surprised me", "I didn't expect" | He raises his eyebrows and lifts both hands slightly off his lap with open palms, then lowers them. | Untested |
| Call to action | "try this", "go do it", "start today", "ask for help" | He leans slightly forward, raises his right hand, open with the palm up, toward the camera, makes one small forward push, then lowers it back to his lap. | Untested |
| Relief, it worked | "it worked", "I finished early", "done" | He opens both hands outward from his lap with palms up, with a small smile, then rests them again. | Untested |

For a standing or walking look, replace "back to his lap" with "back to his side". Placed gestures on a walking look
are not reliable yet.

## Gestures to avoid

- **Pointing an index finger at the camera.** It reads as accusing, and it is rude in some cultures. Use an open hand.
- **The OK sign, the thumbs-up, and two fingers with the palm facing inward.** Their meanings change between
  countries. For "two", keep the palm toward the camera.
- **Hands that cover the face, touch the face or hair, or leave the frame.** Keep gestures between the chest and chin.
- **Large or fast movements.** They blur in generated video and can disappear at the frame edge.
- **A gesture on every sentence.** It stops meaning anything.

## What the sources say, and how sure they are

- **Timing.** The strongest moment of a gesture (the stroke) usually falls on or just before the stressed word. This
  comes from gesture research (McNeill; Kendon) and a small study of TED talks. It is a tendency, not a law.
- **Four kinds of gesture** (McNeill): iconic (shows a thing or action), metaphoric (shows an abstract idea, such as
  two options), deictic (points), and beat (a small rhythmic emphasis). The table above uses the first three for
  meaning and beats for emphasis.
- **Fixed meanings are coaching advice, not proven facts.** "Open palms mean honesty" and "hand on chest means
  sincerity" come from presentation coaches. The academic evidence supports matching the gesture to the words and to
  the timing. It does not support a universal dictionary.
- **More gestures is not better.** Vanessa Van Edwards' count (popular TED speakers used about 465 gestures in 18
  minutes) is a correlation from one analysis. Do not chase a number.
- **Finger counting differs by country** (general knowledge, not from the brief): much of Europe starts with the
  thumb. The table uses the US style, index finger first.

Sources (from a web research pass on 2026-11-23):
- McNeill, "Gesture: a psycholinguistic approach": https://mcneilllab.uchicago.edu/pdfs/gesture.a_psycholinguistic_approach.cambridge.encyclop.pdf
- Kita and others, "Speech-accompanying gesture", Oxford Handbook chapter: https://wrap.warwick.ac.uk/id/eprint/65931/1/WRAP_Speech_accompanying_gesture_for_Oxford_Handbook_v2.pdf
- Gesture and prosody timing in TED talks: https://hal.science/hal-04370544v1/document
- BEAT2 / EMAGE co-speech gesture dataset (CVPR 2024): https://cvpr.thecvf.com/virtual/2024/poster/30938
- Science of People, "What to do with your hands": https://www.scienceofpeople.com/what-to-do-with-hands/
- BIGVU, on-camera body language: https://bigvu.tv/blog/master-your-video-brand-expert-body-language/
- Granary, hands on camera: https://www.granary.digital/hands-on-camera-in-frame-or-out-never-both.html
