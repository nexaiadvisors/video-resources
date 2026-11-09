# Sprite edit prompts (step 2)

Read at step 2. Run each as an image edit (Nano Banana `edit_image`, or any editor that takes a
reference image), then paste only the region with `scripts/paste.py`.

Order matters: make the neutral base first, then every mouth edit FROM the neutral base, so all
mouths share the same face around them.

| File | Edit from | Region | Prompt |
|---|---|---|---|
| s-closed.jpg | original portrait | mouth | Change ONLY the mouth and the cheeks right around it: a calm, neutral, attentive expression, NOT smiling. Mouth corners relaxed and level, lips relaxed and very slightly parted (a 2 mm gap, no teeth visible). Keep everything else identical: eyes, eyebrows, face shape, head position and angle, hair, clothes, background, lighting, framing and crop. |
| s-slight.jpg | s-closed | mouth | Change ONLY the mouth: mid-word in calm speech, lips parted about 1 cm, upper teeth edges visible, neutral expression (not smiling). Keep everything else identical. |
| s-ah.jpg | s-closed | mouth | Change ONLY the mouth and jaw: saying "ah" in calm speech, jaw dropped about 2.5 cm, upper teeth and dark mouth interior visible, neutral expression (not smiling, not laughing). Keep everything else identical. |
| s-oo.jpg | s-closed | mouth | Change ONLY the mouth: saying "oo" as in "two", lips gently rounded into a small open circle, neutral expression, natural not exaggerated. Keep everything else identical. |
| s-ee.jpg | s-closed | mouth | Change ONLY the mouth: saying "ee" as in "me", lips slightly spread and parted, upper and lower teeth close together and visible, neutral expression, not a grin. Keep everything else identical. |
| s-blink.jpg | s-closed | eyes | Mid-blink photo: both eyes COMPLETELY CLOSED, upper eyelids fully down covering the eyes, eyelashes resting on the lower lid, no iris or white visible. Relaxed, not squinting. Change nothing else. |
| s-lookL.jpg / s-lookR.jpg | s-closed | eyes | Change ONLY the eyes: they glance slightly to his left / right, irises shifted a few millimeters, eyelids normal. Keep everything else identical. |

Checks after pasting (look at crops of the face, not the full frame):
- Blink: the eyes must be fully shut. "Nearly closed" reads as a squint and no blink in motion.
- No sprite may change the head outline, hair or background; paste.py keeps only the region, but
  a bad alignment shows as a doubled edge. Redo that edit.
- The base must not grin. A smiling base makes every mouth look like talking through a fixed smile.
