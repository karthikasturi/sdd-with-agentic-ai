# Feature Specification: Alert Escalation

**Input**: User description: "Add an `EscalatedFlag bool` column to a new
`escalation_state` table, keyed by notification ID. Use `github.com/robfig/cron` to run
a job every 5 minutes that finds CRITICAL notifications unacknowledged for over 30
minutes, sets `EscalatedFlag = true`, and POSTs the notification to
`https://pager.internal/api/v1/page` so on-call gets an SMS."

This is an implementation plan wearing a spec's name — it dictates a schema, a specific
third-party scheduling library, and an exact external integration, none of which any
requirement asked for.
