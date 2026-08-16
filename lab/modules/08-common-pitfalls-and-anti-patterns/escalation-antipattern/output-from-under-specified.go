// Real, unedited output from feeding spec-under-specified.md to an agent, cold.
package escalation

import "time"

// REASONABLE_TIME — the spec said "a reasonable time." The agent picked a number.
// Nobody asked for 15 minutes specifically; nobody would know to object to it either,
// since the spec never gave anyone something concrete to compare against.
const REASONABLE_TIME = 15 * time.Minute

type Notification struct {
	ID           string
	Severity     string // "MINOR" | "NORMAL" | "CRITICAL"
	Status       string // "NEW" | "PROCESSED" | "ESCALATED" — this field is never touched below
	Acknowledged bool
	Created      time.Time
}

type NotificationSender interface {
	Notify(n *Notification)
}

// EscalateOverdue is meant to escalate unacknowledged critical alerts. The spec never
// said "critical alerts" though — it said "alerts" — so this applies to every severity,
// not just CRITICAL, because nothing in the spec gave the agent a reason to narrow it.
func EscalateOverdue(notifications []*Notification, sender NotificationSender) {
	for _, n := range notifications {
		if n.Status == "NEW" && !n.Acknowledged && time.Since(n.Created) > REASONABLE_TIME {
			// Destructive overwrite: bumps Severity, never touches Status. The
			// platform's own Notification schema already has an ESCALATED status
			// value for exactly this — nothing here uses it, because nothing in
			// the spec told the agent it existed. No audit event recorded either.
			n.Severity = "CRITICAL"
			sender.Notify(n) // no idempotency guard — fires again every time this runs
		}
	}
}
