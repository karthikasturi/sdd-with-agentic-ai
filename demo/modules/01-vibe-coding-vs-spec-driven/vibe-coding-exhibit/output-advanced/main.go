package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"
	"sync"
)

var (
	mu        sync.Mutex
	equipment = map[string]Equipment{}
	alerts    = []Alert{}
	nextID    = 1
)

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
	if err := json.NewDecoder(r.Body).Decode(&reading); err != nil {
		http.Error(w, "invalid request body", http.StatusUnprocessableEntity)
		return
	}

	mu.Lock()
	_, registered := equipment[reading.EquipmentID]
	mu.Unlock()
	if !registered {
		http.Error(w, "unknown equipment id", http.StatusNotFound)
		return
	}

	bounds, ok := Thresholds[reading.Type]
	if !ok {
		http.Error(w, "unknown measurement type", http.StatusUnprocessableEntity)
		return
	}

	severity := ""
	switch {
	case reading.Value >= bounds.Critical:
		severity = "critical"
	case reading.Value >= bounds.Warning:
		severity = "warning"
	}

	if severity != "" {
		// No debounce, no dedup: every single out-of-range reading creates a
		// brand-new alert, even if the last ten readings were already over
		// the same threshold for the same equipment. See NOTES.md.
		alert := Alert{
			ID: nextID, EquipmentID: reading.EquipmentID, Type: reading.Type,
			Value: reading.Value, Severity: severity,
		}
		mu.Lock()
		alerts = append(alerts, alert)
		nextID++
		mu.Unlock()
	}

	w.WriteHeader(http.StatusCreated)
}

func listAlerts(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()
	_ = json.NewEncoder(w).Encode(alerts)
}

func acknowledgeAlert(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.Atoi(r.URL.Query().Get("id"))
	if err != nil {
		http.Error(w, "invalid id", http.StatusUnprocessableEntity)
		return
	}

	mu.Lock()
	defer mu.Unlock()
	for i := range alerts { // indexes into the slice — mutation actually sticks
		if alerts[i].ID != id {
			continue
		}
		if alerts[i].Acknowledged {
			http.Error(w, "already acknowledged", http.StatusConflict)
			return
		}
		alerts[i].Acknowledged = true
		fmt.Fprintln(w, "ok")
		return
	}
	http.Error(w, "alert not found", http.StatusNotFound)
}

func main() {
	http.HandleFunc("/equipment", registerEquipment)
	http.HandleFunc("/readings", submitReading)
	http.HandleFunc("/alerts", listAlerts)
	http.HandleFunc("/alerts/ack", acknowledgeAlert)
	http.ListenAndServe(":8080", nil)
}
