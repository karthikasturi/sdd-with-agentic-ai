// Real, unedited output from feeding spec-over-specified.md to an agent — implemented
// exactly as specified, which is exactly the problem.
package escalation

import (
	"bytes"
	"encoding/json"
	"net/http"
	"time"

	"github.com/robfig/cron/v3" // new dependency, not previously in go.mod, not vetted
)

// escalationState is the new table the "spec" dictated — instead of using
// support-notifications' own existing `status: ESCALATED` enum value, this invents a
// second, parallel place to record the same fact.
type escalationState struct {
	NotificationID string
	EscalatedFlag  bool
}

func StartEscalationJob(store map[string]*escalationState, findOverdue func() []Notification) {
	c := cron.New()
	_, _ = c.AddFunc("*/5 * * * *", func() {
		for _, n := range findOverdue() {
			if time.Since(n.Created) <= 30*time.Minute {
				continue
			}
			store[n.ID] = &escalationState{NotificationID: n.ID, EscalatedFlag: true}

			// Nobody asked this feature to page anyone. The spec did — but the
			// spec was an implementation plan wearing a requirements document's
			// name, and it directly contradicts this project's own real
			// spec.md, which already ruled paging out of scope for this
			// feature's channel mechanism.
			body, _ := json.Marshal(map[string]string{"notificationId": n.ID})
			_, _ = http.Post("https://pager.internal/api/v1/page", "application/json", bytes.NewReader(body))
		}
	})
	c.Start()
}

type Notification struct {
	ID      string
	Created time.Time
}
