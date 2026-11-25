# MonitorLab — Demo Monitoring Infrastructure

Local Flask demo for a **read-only** Linux server monitoring UI. Admins register hosts; teams view **simulated** CPU, memory, network, and port metrics without SSH. See [docs/requirements.md](docs/requirements.md).

**Python:** 3.10+ (CI uses 3.10)

[![CI](https://github.com/SrujanaGH/Cursor_Monitorning_Application/actions/workflows/ci.yml/badge.svg)](https://github.com/SrujanaGH/Cursor_Monitorning_Application/actions/workflows/ci.yml)

## Quick start (local “deploy”)

1. `git pull` (or sync this repo)
2. `python3 -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `cp .env.example .env` (optional; set `SECRET_KEY` for stable sessions)
5. `python app.py` → open `http://<host>:5777`

There is **no cloud CD** — deploy means pull → venv → install → run on a trusted lab machine.

## Demo login (local only)

| Field | Value |
| --- | --- |
| Username | `admin` |
| Password | `admin123` |

Password is stored **hashed** (Werkzeug) in SQLite on first run. Change `ADMIN_PASSWORD` in `.env` **before** the first start if you want a different seed.

### Sign in / out

1. Open `http://<host>:5777` → redirected to `/login`
2. Sign in with the demo admin credentials
3. Use **Sign out** in the header (POST + CSRF)

## Add a Linux server

1. Sign in and use **Add Linux server** on the dashboard
2. Fields: **display name**, **hostname or IP**, optional **notes**
3. The host appears with mock OK/Warning status; open it for CPU, memory, network, and ports
4. **Remove** deletes the registry entry (confirm in the browser) — nothing is run on the remote host

## Metrics

All metrics are **mock/demo data** (no SSH, no agents, no subprocess against hosts). Dashboard and detail views auto-refresh every **7 seconds** (override with `METRICS_REFRESH_SECONDS`); use **Refresh now** for a manual poll.

## Verify

- [ ] `http://0.0.0.0:5777` or `http://<host-ip>:5777` shows sign-in, then the read-only dashboard after login

## Tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Env vars

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Flask sessions; required when `DEMO_MODE=0` |
| `DEMO_MODE` | `1` (default) allows ephemeral `SECRET_KEY` with warning |
| `FLASK_DEBUG` | Debug mode (default off) |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` | First-run admin seed only |
| `DATABASE_URL` | Optional SQLite URL |
| `METRICS_REFRESH_SECONDS` | Poll interval (default 7) |

## Security notes (demo)

- Binds to **`0.0.0.0:5777`** (all interfaces). Use **only on trusted/lab networks**; keep auth enabled.
- Do not commit `.env`, secrets, or `*.db` / `instance/` files.
- Demo defaults (`admin` / `admin123`) are local-lab only.
- CSRF on login, logout, and server mutate forms; monitoring views are read-only (no remote commands).
- Stack traces are not shown to users when debug is off.

## Project layout

```
app/                 # Factory, models, metrics, routes
templates/           # Jinja (login, dashboard, detail)
static/              # CSS / JS auto-refresh
tests/               # pytest (auth, servers, metrics)
.github/workflows/   # CI: install → pytest
docs/                # PRD + TODO
app.py               # Entry point (0.0.0.0:5777)
```
