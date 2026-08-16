# EdgeX Foundry & Industrial Protocols — A Primer

Read this **before** Module 1 if you've never touched EdgeX Foundry, OPC UA, or Modbus.
Everything below is real — either sourced from this course's own curated repos (cited
by file path, checkable yourself) or from the actual public specifications, not
simplified to the point of being wrong. Nothing here is invented for teaching purposes.

## The scenario

**Meridian Fabrication Group** ("Meridian") runs three plants. Each plant floor already
has PLCs and SCADA-adjacent equipment talking two protocols that have existed in
industrial automation for decades: **Modbus** (older, simpler, everywhere) and **OPC
UA** (newer, richer, increasingly the standard for anything modernizing). None of that
hardware is going away — replacing instrumented PLCs is a multi-year, multi-million-
dollar capital project, not a sprint. Meridian's ask is the textbook brownfield ask:
*"Get us live data and alerting off the floor we already have, into a modern stack,
without touching the floor."*

Meridian picked **EdgeX Foundry** as the platform sitting between "the floor" and "the
modern stack." Every module in this course, and every pair in `assignment-pool.md`,
is a piece of that same picture — you're not learning EdgeX in the abstract, you're
building a slice of what Meridian's actual team would build. Swap "Meridian" for your
own imagined client if it helps; the shape of the problem doesn't change.

## What EdgeX Foundry actually is

A **Linux Foundation / LF Edge**-governed, vendor-neutral, open-source **IoT edge
computing platform** — not a product any one company controls, which is exactly why an
organization like Meridian can adopt it without being locked into one vendor's device
support. It's a set of loosely-coupled microservices, most talking REST to each other
and to a message bus, that together do one job: **get data off physical devices, using
whatever protocol those devices speak, into a uniform shape a modern stack can consume**
— and let commands flow back the other way.

This course curates 5 real repos out of the ~120 in the EdgeX org. What they are, and
which layer of the architecture they play:

| Repo | Language | Layer | What it does for Meridian |
|---|---|---|---|
| `edgex-go` | Go | Core + support services | The platform's own backbone — see the real service list below |
| `device-opc-ua` | Go | Device service | Speaks OPC UA to Meridian's newer PLCs/SCADA |
| `device-modbus-go` | Go | Device service | Speaks Modbus to Meridian's older PLCs |
| `edgex-ui-go` | Angular | Operator dashboard | What Meridian's floor staff actually look at |
| `opc-ua-dotnet` | C# | Protocol implementation | The real OPC UA stack `device-opc-ua` talks to (standing in for a real PLC/SCADA endpoint via its `ConsoleReferenceServer` sample) |

## EdgeX's real architecture (from `edgex-go/cmd/`, not a generic diagram)

`edgex-go`'s own `cmd/` directory — checkable yourself, `repos/edgex-go/cmd/` — ships
these deployable services. Grouping them by role:

- **Core services** — the platform's data/metadata backbone:
  - `core-data` — ingests and stores sensor readings
  - `core-metadata` — the registry of what devices/profiles/services exist
  - `core-command` — routes commands (writes) back down to devices
  - `core-keeper` — configuration and service registry
- **Support services** — cross-cutting platform capability:
  - `support-notifications` — the service every pair in this course that "raises an
    alert" actually extends (see `support-notifications.yaml`'s OpenAPI contract)
  - `support-scheduler` — internal cron-like scheduling
- **Security services** (real, present in the repo, out of scope for this course's
  hands-on but worth knowing exist): `security-proxy-*`, `security-secretstore-setup`,
  `security-spire-*`, `security-spiffe-*` — EdgeX's zero-trust stack, referenced but not
  enabled in this course's Module 5 discussion of auth posture (`plan.md`'s "Security &
  Auth Path" section explains why it's out of scope for internal service calls here).
- **Device services** (separate repos, not in `edgex-go` itself) — protocol-specific
  connectors. This is where `device-opc-ua` and `device-modbus-go` live: each translates
  one wire protocol into EdgeX's uniform internal model, and nothing upstream of the
  device service needs to know or care which protocol a given device actually speaks.

## Core EdgeX vocabulary

- **Device** — one physical (or simulated) thing being connected, registered in
  `core-metadata`.
- **Device Profile** — a template describing a *class* of device: what data it exposes,
  how to read/write it, in protocol-specific terms (an OPC UA NodeId, a Modbus register
  address). This course's threshold-alerting work adds configuration onto the device
  profile precisely because that's the existing mechanism for "per-resource
  configuration" — see `plan.md`'s Design Decisions in
  `../brownfield-project/specs/001-opcua-threshold-alerting/plan.md`.
- **Resource** (Device Resource) — one specific data point on a device profile — one
  sensor value, one writable setpoint.
- **Reading** — one measured value, at one point in time, for one resource.
- **Event** — one or more Readings reported together, the unit `core-data` actually
  ingests.
- **Command** — a request to read or write a resource on a live device, routed through
  `core-command`.
- **Notification** — an alert raised through `support-notifications` — what every
  "threshold alerting" pair in `assignment-pool.md` ultimately produces.
- **Subscription** (EdgeX's, not OPC UA's — the two protocols reuse this word for
  different things, see below) — a rule for *who* gets notified when a Notification of
  a given category/severity is raised.
- **Provision Watcher** — a rule for auto-discovering and auto-registering new devices
  that match a pattern, instead of registering each one by hand.

## OPC UA vocabulary (`device-opc-ua`, `opc-ua-dotnet`)

OPC UA (**OPC Unified Architecture**) is the modern industrial-automation communication
standard, maintained by the OPC Foundation — what PLCs and SCADA systems increasingly
speak when they're not stuck on something older. Terms you'll actually hit in this
course's code:

- **Server** — the thing exposing data (a PLC, a SCADA system, or in this course, the
  real `opc-ua-dotnet/samples/ConsoleReferenceServer`, standing in for one).
- **Client** — the thing reading from a Server. `device-opc-ua` is an OPC UA Client.
- **Session** — an authenticated, stateful connection between Client and Server. Pair
  6's defect (`opc-ua-dotnet#2033`) is about Sessions being closed out from under a
  Client under load.
- **Subscription** (OPC UA's own meaning — a live connection concept, not EdgeX's rule
  concept above) — a Client asks a Server to push updates when data changes, instead of
  polling. `device-opc-ua/internal/driver/subscriptionlistener.go` is exactly this.
- **MonitoredItem** — one specific piece of data within a Subscription being watched for
  changes.
- **NodeId** — the address of one specific piece of data in a Server's **Address
  Space** (its whole exposed data model) — the OPC UA equivalent of a Modbus register
  address, but richer: typed, hierarchical, self-describing.
- **Historizing** — whether a Server retains historical values for a node, queryable
  later, not just the live value. Pair 5's defect (`opc-ua-dotnet#2520`) is a node
  claiming this capability without actually providing it.
- **Endpoint / Security Policy** — the URL plus the security mode (signed, encrypted, or
  neither) a Client connects with — real security posture, not a formality.

## Modbus vocabulary (`device-modbus-go`)

Modbus is older (1979), simpler, and still everywhere on real plant floors — a
request/response protocol built around a small set of **registers**, not a rich typed
address space. Real function calls straight from
`device-modbus-go/internal/driver/modbusclient.go`:

- **Coil** — one bit, read/write (`ReadCoils`, `WriteMultipleCoils`) — a discrete
  output, e.g. a relay.
- **Discrete Input** — one bit, read-only (`ReadDiscreteInputs`) — a discrete sensor,
  e.g. a limit switch.
- **Holding Register** — one 16-bit word, read/write (`ReadHoldingRegisters`) — the
  most common one, a setpoint or a general-purpose value.
- **Input Register** — one 16-bit word, read-only (`ReadInputRegisters`) — a measured
  value, e.g. a temperature.
- **Function Code** — which of the above operations a given Modbus request performs —
  the protocol's whole vocabulary is really just a small set of these.
- **Starting Address** — where in a register range a read/write begins. Pair 3's
  defect (`device-modbus-go#61`) is this value being silently decremented by 1 before
  use — a one-line bug with real consequences: every subsequent read/write on that
  resource points at the wrong physical register.
- **Unit ID** (sometimes "slave ID," legacy terminology still used in the spec and in
  some tooling) — which physical device on a shared Modbus line a request targets, since
  multiple devices can share one serial line or TCP connection.

## Why this matters for how you work this week

Notice what's *not* here: nothing about Meridian's org chart, ticketing conventions, or
internal jargon — because none of that exists yet for a brownfield adoption. What
exists is the protocol the floor already speaks, and the platform code already written
against it. Module 2's whole point is that discovering *this* — what's real, what's
documented, what only lives in source — is the actual first step, before a single spec
gets written. This primer gives you the vocabulary to read that code once you get
there; it doesn't do the discovery for you.

**Going deeper** (real, official, not course material):
[docs.edgexfoundry.org](https://docs.edgexfoundry.org),
[opcfoundation.org](https://opcfoundation.org) for OPC UA,
[modbus.org](https://modbus.org) for the Modbus spec itself.
