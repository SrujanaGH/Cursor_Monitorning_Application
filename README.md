# MonitorLab — Demo Monitoring Infrastructure

Local Flask demo for a **read-only** Linux server monitoring UI. Admins will register hosts; teams view **simulated** CPU, memory, network, and port metrics without SSH. See [docs/requirements.md](docs/requirements.md) for the full PRD.

**Python:** 3.10+ (developed against 3.10)

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # optional; edit SECRET_KEY for stable sessions
python app.py
```

Open `http://<host>:5777` (binds to `0.0.0.0:5777`).

Alternate: `flask --app app run --host 0.0.0.0 --port 5777`

## Demo login (local only)

| Field | Value |
| --- | --- |
| Username | `admin` |
| Password | `admin123` |

Auth lands in Phase 1; password will be stored hashed. Change via `ADMIN_PASSWORD` in `.env` before first seed.

## Verify

- [ ] Browser loads the shell at `http://0.0.0.0:5777` or `http://<host-ip>:5777` and shows “Monitoring — read-only demo”.

## Security notes (demo)

- Listens on **`0.0.0.0:5777`** (all interfaces). Reachable on the network — **use only on trusted/lab networks**. Keep auth enabled (Phase 1+).
- Do not commit `.env` or local DB files. Demo defaults (`admin` / `admin123`) are for lab use only.
- If `SECRET_KEY` is missing and `DEMO_MODE=1` (default), an ephemeral key is generated with a console warning. Set `DEMO_MODE=0` to require `SECRET_KEY` at startup.
- `FLASK_DEBUG` defaults to off; enable only when needed locally.

## Project layout

```
app/           # Flask factory, config, routes
templates/     # Jinja layouts
static/        # CSS / JS
tests/         # pytest smoke tests
docs/          # PRD and implementation TODO
app.py         # Entry point (0.0.0.0:5777)
```
