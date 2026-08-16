package main

// Real, unedited output from feeding PROMPT-ADVANCED.md to an agent cold —
// still no spec, no constitution, no repo context, just one more thoughtful
// prompt than Exhibit A. See NOTES.md for what improved and what's still
// missing even here.

type Equipment struct {
	ID   string `json:"id"`
	Name string `json:"name"`
	Type string `json:"type"` // measurement type this equipment reports
}

type Reading struct {
	EquipmentID string  `json:"equipmentId"`
	Type        string  `json:"type"`
	Value       float64 `json:"value"`
}

type Alert struct {
	ID           int     `json:"id"`
	EquipmentID  string  `json:"equipmentId"`
	Type         string  `json:"type"`
	Value        float64 `json:"value"`
	Severity     string  `json:"severity"`
	Acknowledged bool    `json:"acknowledged"`
}

type threshold struct {
	Warning  float64
	Critical float64
}

// Thresholds fixes Exhibit A's global-constant bug: bounds are looked up per
// measurement type instead of one number applied to everything.
var Thresholds = map[string]threshold{
	"temperature": {Warning: 80, Critical: 95},
	"vibration":   {Warning: 5, Critical: 8},
	"runtime":     {Warning: 8000, Critical: 10000},
}
