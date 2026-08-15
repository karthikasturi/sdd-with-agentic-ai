package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"
	"sync"
)

// Real, unedited output from feeding PROMPT.md to an agent cold, in an empty
// directory — no spec, no constitution, no repo context. It runs. It "works"
// if you don't look closely. See NOTES.md for exactly where it doesn't.

type Equipment struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

type Reading struct {
	EquipmentID string  `json:"equipmentId"`
	Value       float64 `json:"value"`
}

type Alert struct {
	ID           int     `json:"id"`
	EquipmentID  string  `json:"equipmentId"`
	Value        float64 `json:"value"`
	Acknowledged bool    `json:"acknowledged"`
}

var (
	mu        sync.Mutex
	equipment = map[string]Equipment{}
	alerts    = []Alert{}
	nextID    = 1
)

// threshold is a single global value the agent invented — it never asked
// what "bad" means for different equipment or measurement types, so neither
// did the code.
const threshold = 100.0

func registerEquipment(w http.ResponseWriter, r *http.Request) {
	var e Equipment
	_ = json.NewDecoder(r.Body).Decode(&e)
	mu.Lock()
	equipment[e.ID] = e
	mu.Unlock()
	w.WriteHeader(http.StatusCreated)
}

func submitReading(w http.ResponseWriter, r *http.Request) {
	var reading Reading
	_ = json.NewDecoder(r.Body).Decode(&reading)

	if reading.Value > threshold {
		alert := Alert{ID: nextID, EquipmentID: reading.EquipmentID, Value: reading.Value}
		mu.Lock()
		alerts = append(alerts, alert)
		nextID++
		mu.Unlock()

		// Nobody asked for paging. The agent added it anyway, and the error
		// from a URL that was never configured to exist is silently ignored.
		go notifyPager(alert)
	}

	w.WriteHeader(http.StatusCreated)
}

func notifyPager(alert Alert) {
	body, _ := json.Marshal(alert)
	resp, err := http.Post("http://pager.internal/notify", "application/json", bytes.NewReader(body))
	if err != nil {
		return // swallowed — nobody ever finds out paging never worked
	}
	defer resp.Body.Close()
}

func listAlerts(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()
	_ = json.NewEncoder(w).Encode(alerts)
}

func acknowledgeAlert(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(r.URL.Query().Get("id"))

	mu.Lock()
	defer mu.Unlock()
	for _, alert := range alerts { // ranges by value — see NOTES.md
		if alert.ID == id {
			alert.Acknowledged = true // mutates the loop copy, not alerts[i]
		}
	}
	fmt.Fprintln(w, "ok")
}

func main() {
	http.HandleFunc("/equipment", registerEquipment)
	http.HandleFunc("/readings", submitReading)
	http.HandleFunc("/alerts", listAlerts)
	http.HandleFunc("/alerts/ack", acknowledgeAlert)
	http.ListenAndServe(":8080", nil)
}
