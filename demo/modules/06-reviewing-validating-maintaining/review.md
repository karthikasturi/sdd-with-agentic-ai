# Review: Candidate Node-Offline Patch (closes tasks.md's deferred T013)

## The change under review

`tasks.md` explicitly deferred FR-013 (node-offline detection) out of the original
implementation pass — flagged, not silently dropped (Module 4). This candidate patch
closes it: `offline_patch_excerpt.go` adds `CheckOfflineNodes`, meant to run
periodically and raise a MINOR Notification for any resource silent for 60 minutes.

## What automated gates already checked

Nothing — these gates run against spec/plan/tasks, before implementation exists.
`offline_patch_excerpt_test.go` ships with the change and is genuinely green: 1/1
passing, and it doesn't break any of the 8 existing tests either — 9/9 across the
package. A checklist or analyze pass has no way to catch what's wrong here; neither one
ever reads implementation code.

## What a human reviewer should catch

Read the actual comparison: `time.Since(st.lastSeenAt) > 60`. `time.Since` returns a
`time.Duration` — nanoseconds. The literal `60` is an untyped constant that the compiler
silently converts to `60` in whatever unit the comparison needs — here, **60
nanoseconds**, not 60 minutes. The correct comparison is
`time.Since(st.lastSeenAt) > 60*time.Minute`.

This is not a typo that jumps out. It compiles cleanly, `go vet` has nothing to say
about it, and the function's own doc comment states the right intent one line above the
bug. Verified live, not asserted — dropped into the real `internal/threshold` package
(where its dependencies actually live) and run for real:

```
go test ./internal/threshold/... -run TestCheckOfflineNodes -v
=== RUN   TestCheckOfflineNodes_DetectsOfflineResource
--- PASS: TestCheckOfflineNodes_DetectsOfflineResource (0.00s)
```

Green. Now look at what the test actually does: it calls `Evaluate` once (seeding
`lastSeenAt` to *right now*), then calls `CheckOfflineNodes` **immediately after**, and
asserts a notification was sent. Under the buggy comparison, `time.Since(justNow)` is a
few microseconds — comfortably greater than 60 *nanoseconds* — so it fires. The test
passes because it expects the bug's behavior. A resource that reported a value one
second ago would trigger a false "offline" alert under this code; FR-013 requires 60
*minutes* of silence, not 60 nanoseconds. In production, every thresholded resource
would generate an offline Notification almost immediately after every single reading —
a flood in the opposite direction from Finding 1's flood, same root cause: a duration
comparison that silently means something other than what it looks like it means.

## Why this matters beyond one bug

This is the same shape of gap `vibe-coding-exhibit/NOTES.md` (Module 1) and
`checklist.md` Finding 1 (Module 5) both already showed, one stage further downstream
each time: Module 1's naive output hardcoded a threshold nobody asked about. Module 5's
checklist caught a spec that never said what happens when a condition keeps recurring.
This one is worse in one specific way — it passed a real, green test, written by whoever
wrote the patch, testing exactly the behavior they intended to test. The test isn't
lazy or missing. It's wrong in the same direction as the code, because both came from
the same mistaken mental model of what the comparison meant. No automated gate catches
two independent artifacts sharing one author's blind spot — only a second, independent
read of the actual line does.

## Remediation

1. Reject this patch as-is — do not merge.
2. Fix: `time.Since(st.lastSeenAt) > 60*time.Minute`.
3. Fix the test too, not just the code: assert the notification is **not** sent
   immediately after a fresh reading, and **is** sent once enough time has actually
   elapsed (inject a clock/fake time rather than sleeping 60 real minutes in a test —
   left as an exercise; `Evaluator` doesn't currently support this and would need a
   small refactor to accept a clock, itself worth a line in a follow-up plan, not a
   silent addition to this patch).
