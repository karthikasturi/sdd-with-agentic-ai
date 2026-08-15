Build a Go service that ingests sensor readings for industrial equipment (temperature,
vibration, runtime-hours style values), each reading tagged with an equipment ID and a
resource/measurement type. Look up a configurable warning/critical threshold per
resource type — don't hardcode a single global threshold — and raise an alert when a
reading crosses one, with severity based on how far over. Reject a reading for
equipment that isn't registered, and reject non-numeric values, with an explicit error
either way — never silently drop or store something invalid. Let staff list open
alerts, see which equipment/resource/value triggered each one, and acknowledge an
alert exactly once — a second acknowledgment attempt should be rejected, not silently
accepted. Keep it idiomatic Go, structure the code across a few files instead of one,
and don't add any external integrations I didn't ask for.
