# Implementation TODO — Demo Monitoring Infrastructure

Small, AI-assisted increments aligned with [requirements.md](./requirements.md).  
**Goal:** local Flask demo only. Check off items as you complete them.

---

## Phase 0 — Project initialization & basic UI

### 0.1 Scaffold the project
- [x] Create repo layout: `app/`, `templates/`, `static/css/`, `static/js/`, `tests/`, `docs/`
- [x] Add `requirements.txt` with Flask (pin versions)
- [x] Add `.gitignore` (venv, `__pycache__`, `.env`, `*.db`, `.pytest_cache`)
- [x] **Security:** do not commit secrets, virtualenv, or local DB files
- [x] **Docs:** short `README.md` — what this is, how to create venv, install, run

### 0.2 Minimal Flask app + basic UI
- [x] Create `app.py` (or `app/__init__.py`) that serves a home/dashboard shell page
- [x] Add base template with attractive, read-only layout (nav, footer, placeholder content)
- [x] Add static CSS for a clean desktop-friendly look (no cards overload; clear hierarchy)
- [x] Confirm app starts locally: `python app.py` → listens on `0.0.0.0:5777`
- [x] **Security:** bind to `0.0.0.0:5777` as required; keep `debug` off unless env opts in; rely on auth because the app is reachable on all interfaces
- [x] **Docs:** update README with screenshot/placeholder note and URL `http://<host>:5777`

---

## Phase 1 — Sign-in & unit tests

### 1.1 Config & secrets hygiene
- [x] Load `SECRET_KEY` from environment (with a clearly marked local demo fallback)
- [x] Add example `.env.example` (no real secrets) documenting `SECRET_KEY`, `FLASK_DEBUG`
- [x] **Security:** never hardcode production secrets; document that demo defaults are local-only
- [x] **Docs:** document required env vars in README

### 1.2 SQLite + admin user (hashed password)
- [x] Add SQLite init / first-run seed for user `admin`
- [x] Store password with Werkzeug `generate_password_hash` / `check_password_hash` (or bcrypt)
- [x] Seed only if admin does not already exist
- [x] **Security:** never store or log plaintext passwords
- [x] **Docs:** document default demo username/password in README (local demo only)

### 1.3 Login / logout flows
- [x] Login page (username + password)
- [x] Session-based auth after successful login
- [x] Logout route that clears session
- [x] Protect dashboard routes: redirect unauthenticated users to login
- [x] **Security:** use POST for login; CSRF protection (Flask-WTF or equivalent); constant-time password check via library helpers; generic “invalid credentials” message
- [x] **Docs:** document login/logout steps in README

### 1.4 Unit tests for auth
- [x] Add `pytest` (+ Flask test client) to `requirements.txt` / `requirements-dev.txt`
- [x] Tests: login success, login failure, logout, protected route redirects when logged out
- [x] Test that stored password is hashed (not plaintext)
- [x] **Security:** ensure tests use a temp DB / isolated config (no real secrets)
- [x] **Docs:** document `pytest` command in README

---

## Phase 2 — Server registry (add Linux servers)

### 2.1 Server model & persistence
- [x] SQLite table/model: `name`, `hostname_or_ip`, optional `notes`, timestamps
- [x] Validate hostname/IP input (basic format checks; reject empty/dangerous input)
- [x] **Security:** sanitize inputs; parameterized queries / ORM only (no string-built SQL); no shell execution of host fields
- [x] **Docs:** document server fields in README or `docs/requirements.md` link

### 2.2 Add / list / delete servers (admin, authenticated)
- [x] Form to add a server (authenticated only)
- [x] List registered servers on dashboard
- [x] Delete server (authenticated only; confirm in UI)
- [x] **Security:** require login for all mutate actions; CSRF on forms; no remote commands on hosts
- [x] **Docs:** short “how to add a server” section in README

### 2.3 Unit tests for servers
- [x] Tests: create, list, delete; reject unauthenticated access; reject invalid input
- [x] **Security:** assert unauthenticated POST/DELETE cannot mutate data
- [x] **Docs:** note new tests in README test section

---

## Phase 3 — Mock metrics & monitoring UI

### 3.1 Mock metrics generator
- [x] Function/module that returns CPU %, memory used/total, network in/out, open ports per server
- [x] Values vary over time (deterministic or lightly randomized) for demo realism
- [x] Simple thresholds (e.g. >80% → Warning, else OK)
- [x] **Security:** metrics are simulated only — no SSH, no subprocess against user-supplied hosts
- [x] **Docs:** state clearly in README that metrics are mock/demo data

### 3.2 Dashboard & server detail (read-only)
- [x] Dashboard: server list with status badges (OK / Warning)
- [x] Detail view: CPU, memory, network, ports
- [x] UI remains read-only for metrics (no command/exec actions)
- [x] **Security:** authorize detail views (login required); do not reflect raw host input unsafely in HTML (autoescape / templates)
- [x] **Docs:** describe dashboard views briefly in README

### 3.3 Auto-refresh (5–10s)
- [x] Poll metrics endpoint or refresh partial UI every 5–10 seconds
- [x] Optional manual refresh control
- [x] **Security:** metrics JSON/API requires authentication; no sensitive debug dumps
- [x] **Docs:** note refresh interval in README

### 3.4 Unit tests for metrics
- [x] Tests: metrics shape/keys present; threshold status mapping; unauthenticated metrics API denied
- [x] **Security:** confirm no credentials or secrets in metrics payload
- [x] **Docs:** keep test run instructions up to date

---

## Phase 4 — Polish, hardening & CI/CD

### 4.1 UI polish (still minimal)
- [x] Consistent styling, empty states (“no servers yet”), clear error messages on forms
- [x] **Security:** avoid leaking stack traces to users when `debug` is off
- [x] **Docs:** optional UI notes / GIF placeholder in README

### 4.2 Final local security pass
- [x] Confirm default bind is `0.0.0.0:5777`
- [x] Confirm `SECRET_KEY` guidance and hashed admin password
- [x] Confirm CSRF on state-changing routes
- [x] Confirm no SSH/agent/shell usage anywhere
- [x] **Docs:** add a short “Security notes (demo)” section in README (note: `0.0.0.0` exposes the app on all NICs — use only on trusted networks)

### 4.3 GitHub Actions CI
- [x] Add `.github/workflows/ci.yml`
- [x] Jobs: install deps → run `pytest` on push/PR (Python 3.x matrix optional but keep minimal: one version is fine)
- [x] Fail CI on test failure
- [x] **Security:** no secrets required in CI for demo; use ephemeral test DB; do not print credentials in logs
- [x] **Docs:** document CI badge/status and that deploy remains local (no CD to cloud required)

### 4.4 Minimal “CD” for local demo (documentation only)
- [x] Document local “deploy” = pull/sync → venv → install → run (no cloud CD)
- [x] Optional: workflow that only runs tests (CI); skip remote deploy jobs
- [x] **Docs:** keep run steps to ≤5 bullets in README

---

## Phase 5 — Done checklist (PRD acceptance)

- [x] Read-only attractive UI with dashboard + detail views
- [x] Admin sign-in with hashed password; logout works
- [x] Add / list / delete Linux servers in SQLite
- [x] Mock CPU, memory, network, ports with auto-refresh
- [x] Unit tests covering auth, servers, metrics access
- [x] GitHub Actions CI running tests
- [x] README covers setup, login, adding servers, tests, security notes
- [x] App runs locally where Cursor is running, bound to `0.0.0.0:5777`

---

## Suggested order for AI-assisted sessions

Work **one checkbox group at a time** (e.g. only `0.1`, then only `0.2`).  
Do not skip security/docs checkboxes inside a group.

| Session | Focus |
| --- | --- |
| 1 | Phase 0.1–0.2 |
| 2 | Phase 1.1–1.4 |
| 3 | Phase 2.1–2.3 |
| 4 | Phase 3.1–3.4 |
| 5 | Phase 4.1–4.4 + Phase 5 |

---

## Out of scope (do not implement in this TODO)

- Real SSH / agent metrics  
- Alerts, SSO, Docker Compose, multi-user roles  
- Cloud deployment pipelines
