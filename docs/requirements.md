# Product Requirements Document (PRD)
## Demo Monitoring Infrastructure — Linux Servers

| Field | Value |
| --- | --- |
| Status | Draft |
| Audience | Internal L1 / L2 / L3 (Infra & App Dev) |
| Type | Local demo application |
| Tech stack | Python, Flask, HTML/CSS/JS (attractive read-only UI) |
| Target | Run on the same machine where Cursor is running |

---

## 1. Problem

Operators currently SSH into Linux servers to check live memory, CPU, network, and port usage. There is no shared, read-only view for support and development teams.

## 2. Goal (Demo)

Provide a **local, minimal** Flask web app where an admin can register Linux servers and teams can view simulated real-time metrics in a friendly, read-only UI — without logging into each host.

## 3. Assumptions (Demo Defaults)

These defaults keep the demo small and easy to run:

| Topic | Demo choice |
| --- | --- |
| Metrics source | **Simulated / mock** metrics per registered server (no SSH/agent required) |
| Must-have metrics | CPU %, memory used/total, network in/out, listening / open ports |
| Refresh | Auto-refresh every **5–10 seconds** (plus manual refresh) |
| Auth | Single **admin** user; UI is **read-only** for monitoring views |
| Default login | Username `admin`; password stored **hashed** (demo password documented for local use) |
| Server fields | Display name + hostname/IP (optional notes) |
| Persistence | **SQLite** (servers + admin user survive restart) |
| Run method | `python app.py` or `flask run` (no Docker required for v1) |
| Listen address | `0.0.0.0` (all interfaces) |
| Port | `5777` |
| Platform | Linux servers only (as monitored targets in the registry) |

---

## 4. Users

| Role | Who | Capabilities |
| --- | --- | --- |
| Admin | Demo operator | Sign in, add/remove servers, view all metrics |
| Viewer (implicit) | L1 / L2 / L3 after sign-in | View dashboards and server metrics only (no destructive actions in UI beyond admin server CRUD for demo) |

For this demo, **one shared admin account** is enough. All monitoring screens remain read-only (no remote commands, no config changes on targets).

---

## 5. Core Features

### Feature 1 — Friendly read-only monitoring UI

**As a** support or app engineer  
**I want** a clear dashboard of server health  
**So that** I do not need to SSH for a quick check.

**Acceptance criteria**

- [ ] Dashboard lists registered servers with high-level status (e.g. OK / Warning based on simple thresholds).
- [ ] Server detail view shows CPU, memory, network, and port usage.
- [ ] UI is attractive, responsive enough for desktop browsers, and does not expose shell/command actions.
- [ ] Metrics refresh automatically every 5–10 seconds without a full page reload (or with a simple poll).

### Feature 2 — Admin sign-in (hashed password)

**As an** admin  
**I want** to sign in with a default username and hashed password  
**So that** the demo is not fully open on the local network.

**Acceptance criteria**

- [ ] Default username: `admin`.
- [ ] Password is stored hashed (e.g. Werkzeug / bcrypt); never stored in plaintext.
- [ ] Unauthenticated users cannot access dashboard or server APIs.
- [ ] Demo password is documented for local setup only (e.g. in README); changeable later if needed.
- [ ] Sign-out is available.

### Feature 3 — Add Linux servers to monitor

**As an** admin  
**I want** to register Linux servers  
**So that** they appear on the monitoring dashboard.

**Acceptance criteria**

- [ ] Form to add a server: **name**, **hostname or IP**, optional **notes**.
- [ ] List / remove registered servers.
- [ ] Each registered server shows mock real-time metrics on the UI.
- [ ] Data persisted in SQLite across app restarts.

---

## 6. Non-Goals (Out of Scope for This Demo)

- Real SSH / agent-based collection from remote hosts  
- Alerts, paging, email/Slack notifications  
- Historical graphs / long-term retention  
- Multi-user SSO / LDAP / OAuth  
- Windows or non-Linux targets  
- Docker Compose / Kubernetes deployment  
- Role-based access beyond single admin  
- Executing commands or changing anything on monitored hosts  

---

## 7. Functional Requirements (Minimal)

| ID | Requirement |
| --- | --- |
| FR-1 | App serves a login page and protected monitoring pages. |
| FR-2 | Admin credentials verified against hashed password in SQLite (or seeded on first run). |
| FR-3 | CRUD for server registry: create, list, delete (update optional). |
| FR-4 | Metrics endpoint (or page data) returns CPU, memory, network, ports per server. |
| FR-5 | Metrics values are generated/simulated for demo realism (vary over time). |
| FR-6 | Simple threshold coloring (e.g. CPU/memory > 80% → warning). |

---

## 8. Non-Functional Requirements (Minimal)

| ID | Requirement |
| --- | --- |
| NFR-1 | Runs locally on developer machine with Python 3.x. |
| NFR-2 | Setup limited to: create venv → install deps → run app → open browser. |
| NFR-3 | Single-process Flask app is acceptable for demo. |
| NFR-4 | UI usable in Chrome/Firefox on desktop. |
| NFR-5 | No secrets committed except clearly marked demo defaults. |
| NFR-6 | App listens on `0.0.0.0:5777`. |

---

## 9. Local Run (Minimal Steps)

1. Create and activate a virtualenv.  
2. `pip install -r requirements.txt`  
3. `python app.py` (or `flask run`)  
4. Open `http://<host>:5777` (app binds to `0.0.0.0:5777`)  
5. Sign in as `admin` with the documented demo password.  
6. Add one or more Linux servers and view metrics.

---

## 10. Success Criteria

- L1/L2/L3 can open the UI locally and see server metrics without SSH.  
- Admin can register servers and see them on the dashboard.  
- Password is hashed; monitoring views are read-only.  
- App starts with a short, documented local setup path.

---

## 11. Future Enhancements (Not Required Now)

- Collect real metrics over SSH or a lightweight agent  
- Historical charts and export  
- Multi-user roles and SSO  
- Alert rules and integrations  

---

## 12. Open Decisions (Locked for Demo)

| Decision | Choice |
| --- | --- |
| Metrics | Mock / simulated |
| DB | SQLite |
| Auth | Single admin, hashed password |
| Deploy | Local Flask only |
| UI mode | Read-only monitoring |
