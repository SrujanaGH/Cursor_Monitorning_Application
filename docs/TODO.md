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
- [ ] Load `SECRET_KEY` from environment (with a clearly marked local demo fallback)
- [ ] Add example `.env.example` (no real secrets) documenting `SECRET_KEY`, `FLASK_DEBUG`
- [ ] **Security:** never hardcode production secrets; document that demo defaults are local-only
- [ ] **Docs:** document required env vars in README

### 1.2 SQLite + admin user (hashed password)
- [ ] Add SQLite init / first-run seed for user `admin`
- [ ] Store password with Werkzeug `generate_password_hash` / `check_password_hash` (or bcrypt)
- [ ] Seed only if admin does not already exist
- [ ] **Security:** never store or log plaintext passwords
- [ ] **Docs:** document default demo username/password in README (local demo only)

### 1.3 Login / logout flows
- [ ] Login page (username + password)
- [ ] Session-based auth after successful login
- [ ] Logout route that clears session
- [ ] Protect dashboard routes: redirect unauthenticated users to login
- [ ] **Security:** use POST for login; CSRF protection (Flask-WTF or equivalent); constant-time password check via library helpers; generic “invalid credentials” message
- [ ] **Docs:** document login/logout steps in README

### 1.4 Unit tests for auth
- [ ] Add `pytest` (+ Flask test client) to `requirements.txt` / `requirements-dev.txt`
- [ ] Tests: login success, login failure, logout, protected route redirects when logged out
- [ ] Test that stored password is hashed (not plaintext)
- [ ] **Security:** ensure tests use a temp DB / isolated config (no real secrets)
- [ ] **Docs:** document `pytest` command in README

---

## Phase 2 — Server registry (add Linux servers)

### 2.1 Server model & persistence
- [ ] SQLite table/model: `name`, `hostname_or_ip`, optional `notes`, timestamps
- [ ] Validate hostname/IP input (basic format checks; reject empty/dangerous input)
- [ ] **Security:** sanitize inputs; parameterized queries / ORM only (no string-built SQL); no shell execution of host fields
- [ ] **Docs:** document server fields in README or `docs/requirements.md` link

### 2.2 Add / list / delete servers (admin, authenticated)
- [ ] Form to add a server (authenticated only)
- [ ] List registered servers on dashboard
- [ ] Delete server (authenticated only; confirm in UI)
- [ ] **Security:** require login for all mutate actions; CSRF on forms; no remote commands on hosts
- [ ] **Docs:** short “how to add a server” section in README

### 2.3 Unit tests for servers
- [ ] Tests: create, list, delete; reject unauthenticated access; reject invalid input
- [ ] **Security:** assert unauthenticated POST/DELETE cannot mutate data
- [ ] **Docs:** note new tests in README test section

---

## Phase 3 — Mock metrics & monitoring UI

### 3.1 Mock metrics generator
- [ ] Function/module that returns CPU %, memory used/total, network in/out, open ports per server
- [ ] Values vary over time (deterministic or lightly randomized) for demo realism
- [ ] Simple thresholds (e.g. >80% → Warning, else OK)
- [ ] **Security:** metrics are simulated only — no SSH, no subprocess against user-supplied hosts
- [ ] **Docs:** state clearly in README that metrics are mock/demo data

### 3.2 Dashboard & server detail (read-only)
- [ ] Dashboard: server list with status badges (OK / Warning)
- [ ] Detail view: CPU, memory, network, ports
- [ ] UI remains read-only for metrics (no command/exec actions)
- [ ] **Security:** authorize detail views (login required); do not reflect raw host input unsafely in HTML (autoescape / templates)
- [ ] **Docs:** describe dashboard views briefly in README

### 3.3 Auto-refresh (5–10s)
- [ ] Poll metrics endpoint or refresh partial UI every 5–10 seconds
- [ ] Optional manual refresh control
- [ ] **Security:** metrics JSON/API requires authentication; no sensitive debug dumps
- [ ] **Docs:** note refresh interval in README

### 3.4 Unit tests for metrics
- [ ] Tests: metrics shape/keys present; threshold status mapping; unauthenticated metrics API denied
- [ ] **Security:** confirm no credentials or secrets in metrics payload
- [ ] **Docs:** keep test run instructions up to date

---

## Phase 4 — Polish, hardening & CI/CD

### 4.1 UI polish (still minimal)
- [ ] Consistent styling, empty states (“no servers yet”), clear error messages on forms
- [ ] **Security:** avoid leaking stack traces to users when `debug` is off
- [ ] **Docs:** optional UI notes / GIF placeholder in README

### 4.2 Final local security pass
- [ ] Confirm default bind is `0.0.0.0:5777`
- [ ] Confirm `SECRET_KEY` guidance and hashed admin password
- [ ] Confirm CSRF on state-changing routes
- [ ] Confirm no SSH/agent/shell usage anywhere
- [ ] **Docs:** add a short “Security notes (demo)” section in README (note: `0.0.0.0` exposes the app on all NICs — use only on trusted networks)

### 4.3 GitHub Actions CI
- [ ] Add `.github/workflows/ci.yml`
- [ ] Jobs: install deps → run `pytest` on push/PR (Python 3.x matrix optional but keep minimal: one version is fine)
- [ ] Fail CI on test failure
- [ ] **Security:** no secrets required in CI for demo; use ephemeral test DB; do not print credentials in logs
- [ ] **Docs:** document CI badge/status and that deploy remains local (no CD to cloud required)

### 4.4 Minimal “CD” for local demo (documentation only)
- [ ] Document local “deploy” = pull/sync → venv → install → run (no cloud CD)
- [ ] Optional: workflow that only runs tests (CI); skip remote deploy jobs
- [ ] **Docs:** keep run steps to ≤5 bullets in README

---

## Phase 5 — Done checklist (PRD acceptance)

- [ ] Read-only attractive UI with dashboard + detail views
- [ ] Admin sign-in with hashed password; logout works
- [ ] Add / list / delete Linux servers in SQLite
- [ ] Mock CPU, memory, network, ports with auto-refresh
- [ ] Unit tests covering auth, servers, metrics access
- [ ] GitHub Actions CI running tests
- [ ] README covers setup, login, adding servers, tests, security notes
- [ ] App runs locally where Cursor is running, bound to `0.0.0.0:5777`

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
