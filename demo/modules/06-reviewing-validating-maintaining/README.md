# Module 6 — Reviewing, Validating, and Maintaining Agent Output

Covers: human-in-the-loop checkpoints that still matter after checklist and analyze
both pass, with added scrutiny for production systems; recognizing hallucinations,
unsafe changes, and weak assumptions no automated gate catches; and managing spec drift
so the spec, constitution, and agent instruction files stay an accurate audit trail as
the codebase evolves.

`flawed-change/` is instructor-provided, real, and green: 9/9 tests pass, including the
one that ships with the bug. `review.md` is the answer key — don't read it before
Step 1.

## Hands-on

### Step 1 — Review a flawed change

Open `flawed-change/offline_patch_excerpt.go` and its test,
`flawed-change/offline_patch_excerpt_test.go`. This candidate closes a real gap —
`tasks.md`'s deferred T013, node-offline detection (FR-013) — and its test passes.

Before reading `review.md`, try to find the bug yourself by reading, then confirm it by
actually running it — drop both files into the real package to do that (they depend on
`Evaluator`/`Thresholds` etc., which live there, not in this exhibit directory — a
realistic step, this is exactly how you'd sanity-check a candidate patch against the
real codebase):

```
cp flawed-change/offline_patch_excerpt.go flawed-change/offline_patch_excerpt_test.go \
   ../../../brownfield-project/repos/device-opc-ua/internal/threshold/
cd ../../../brownfield-project/repos/device-opc-ua
go test ./internal/threshold/... -run TestCheckOfflineNodes -v
# then remove the two copied files — this was a review exercise, not a real merge
rm internal/threshold/offline_patch_excerpt.go internal/threshold/offline_patch_excerpt_test.go
```

Then ask: what does `time.Since(st.lastSeenAt) > 60` actually compare, in what unit? What
would happen to a resource that reported a reading one second ago?

**Checkpoint**: compare your findings to `review.md`. The core issue: `60` is an
untyped constant converted to 60 *nanoseconds*, not 60 minutes — the check fires almost
immediately for any resource, not after an hour of silence. No automated gate could have
caught this: checklist and analyze both run against spec/plan/tasks, never
implementation code. The test itself is green because it was written to expect the
bug's behavior, not FR-013's.

### Step 2 — Document what should have caught it

Write down, specifically: which review step (not "more testing" in the abstract — which
actual step) should have caught this before merge, and why checklist/analyze structurally
couldn't have.

**Checkpoint**: compare against `review.md`'s "Why this matters beyond one bug" section
— the specific answer is a second, independent reader of the actual comparison line,
because the patch's own test shares its author's mistaken mental model and can't
self-detect it.

### Step 3 — Apply the same lens to your own Module-5 implementation

Re-read the task you implemented end-to-end in Module 5 — your own code, not an
exhibit. Look specifically for anything a green test suite wouldn't catch: a comparison
that silently means something other than what it looks like, an assumption about units,
timing, or ordering that happened to hold in your test but isn't guaranteed by your spec.

**Checkpoint**: if you find something, update your spec, constitution, or agent
instruction files to close the gap — the same way this project's constitution went from
1.0.0 to a documented, versioned change the one time a review finding required it (see
`../../../brownfield-project/.specify/memory/constitution.md`'s own Sync Impact Report
at the top of the file). If you don't find anything, that's a real outcome too — say so,
and say what you specifically checked for, not just "looks fine."

## Demo talk track (5–6 minutes) — "the highest-leverage moment in the whole course"

**Live vs. pre-built**: walk this from the real files. The point is *this* bug and *this*
green test, not "a" bug a live session might or might not reproduce.

1. Open `offline_patch_excerpt.go`, point at the doc comment one line above the bug —
   *"meant to run periodically... raise a... Notification for any resource that hasn't
   reported a new value in 60 minutes"* — then point at the actual comparison,
   `> 60`. *"The comment says the right thing. The code says something else, in a unit
   nobody wrote down anywhere."*

2. Run the test live (Step 1's drop-in commands). Green. *"This isn't a
   lazy test. It's a real assertion, that passes, that verifies the wrong thing — because
   whoever wrote the test had the same 60-nanoseconds-means-60-minutes mental model as
   whoever wrote the code. That's not a coincidence, and it's exactly why a second,
   independent reviewer is still load-bearing after every gate is green."*

3. Close by tying it back: Module 1's naive prompt hardcoded a threshold. Module 5's
   checklist caught a spec that never addressed recurrence. This is the same shape of
   gap, one stage later than either — implementation code, with a test that agrees with
   its own mistake. *"Every stage in this course catches a different class of failure.
   This is the class only a human, reading the actual line against the actual
   requirement, catches — and it's the last stage before this ships."*
