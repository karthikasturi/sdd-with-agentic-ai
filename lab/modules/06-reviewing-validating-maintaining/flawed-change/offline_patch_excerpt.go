// Candidate patch closing tasks.md's deferred T013 (node-offline detection, FR-013).
// A real excerpt — package/import lines trimmed for review, logic unchanged.
package threshold

import "time"

// CheckOfflineNodes is meant to run periodically (e.g. every minute) and raise a
// MINOR-severity "node offline" Notification for any resource that hasn't reported a
// new value in 60 minutes (FR-013).
func (e *Evaluator) CheckOfflineNodes(deviceName string) {
	e.mu.Lock()
	defer e.mu.Unlock()

	for resourceName, st := range e.state {
		if time.Since(st.lastSeenAt) > 60 { // 60 minutes of silence — FR-013
			if st.openSeverity == Warning {
				continue // FR-015 — don't duplicate an already-open one
			}
			_ = e.sender.Send(deviceName, resourceName, Warning, 0, 0)
			st.openSeverity = Warning
		}
	}
}
