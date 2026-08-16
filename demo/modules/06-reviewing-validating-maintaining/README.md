# Module 6 — Reviewing, Validating, and Maintaining Agent Output (Demo)

Covers: human-in-the-loop checkpoints that still matter after checklist and analyze
both pass; recognizing hallucinations, unsafe changes, and weak assumptions no
automated gate catches; managing spec drift.

Participant hands-on material for this module: `../../../lab/modules/06-reviewing-validating-maintaining/README.md`.
This file is the presenter-facing talk track only.

## Demo talk track (5–6 minutes) — "the highest-leverage moment in the whole course"

**Live vs. pre-built**: walk this from the real files. The point is *this* bug and *this*
green test, not "a" bug a live session might or might not reproduce.

1. Open `../../../lab/modules/06-reviewing-validating-maintaining/flawed-change/offline_patch_excerpt.go`,
   point at the doc comment one line above the bug — *"meant to run periodically... raise
   a... Notification for any resource that hasn't reported a new value in 60 minutes"* —
   then point at the actual comparison, `> 60`. *"The comment says the right thing. The
   code says something else, in a unit nobody wrote down anywhere."*

2. Run the test live (the hands-on guide's Step 1 drop-in commands, against
   `../../../brownfield-project/repos/device-opc-ua`). Green. *"This isn't a lazy test.
   It's a real assertion, that passes, that verifies the wrong thing — because whoever
   wrote the test had the same 60-nanoseconds-means-60-minutes mental model as whoever
   wrote the code. That's not a coincidence, and it's exactly why a second, independent
   reviewer is still load-bearing after every gate is green."*

3. Close by tying it back: Module 1's naive prompt hardcoded a threshold. Module 5's
   checklist caught a spec that never addressed recurrence. This is the same shape of
   gap, one stage later than either — implementation code, with a test that agrees with
   its own mistake. *"Every stage in this course catches a different class of failure.
   This is the class only a human, reading the actual line against the actual
   requirement, catches — and it's the last stage before this ships."*
