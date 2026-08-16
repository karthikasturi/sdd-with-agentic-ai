// The test that shipped with offline_patch_excerpt.go. Real, unedited, and it passes —
// 1/1 green. Before reading review.md: what does this test actually verify, and what
// value would you expect `time.Since(st.lastSeenAt) > 60` to hold after only 5ms?
package threshold

import "testing"

func TestCheckOfflineNodes_DetectsOfflineResource(t *testing.T) {
	sender := &fakeSender{}
	e := NewEvaluator(sender)
	e.Configure(testResource, Thresholds{Warning: 80.0, Critical: 95.0})

	// Seed lastSeenAt via a normal in-range reading.
	_ = e.Evaluate(testDevice, testResource, 10.0, true)

	// Check immediately — the resource was JUST seen.
	e.CheckOfflineNodes(testDevice)

	if len(sender.sent) != 1 {
		t.Fatalf("want 1 offline notification, got %d", len(sender.sent))
	}
	if sender.sent[0].severity != Warning {
		t.Errorf("want severity %q, got %q", Warning, sender.sent[0].severity)
	}
}
