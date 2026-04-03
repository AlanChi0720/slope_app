# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Available Skills

- `/frontend-design` — Generate distinctive, production-grade frontend UI (components, pages, layouts).
- `/webapp-testing` — Test the running app with Playwright (screenshots, browser logs, UI verification).

## Running the App

All commands must be run from the project root using the project venv:

```bash
# Activate venv (PowerShell)
venv\Scripts\Activate.ps1

# Run the Flask dev server on http://localhost:3000
python app.py
```

There are no tests or a linter configured. `main.py` is a local script for running the processing pipeline outside Flask (useful for quick debugging without the web server).

## Architecture

The app is a single-user local Flask tool. Data flows one-way: upload → process → static files → display.

**Processing pipeline** (`process_data.py`):
- `SlopeDataProcessor` parses a GPX file into a flat DataFrame of every trackpoint (lat, lon, elevation, time, segment_id). It then enriches it with shifted-row comparisons to compute `distance_to_prev(m)`, `speed_m/s`, and an `is_lift` boolean per segment (lift = net elevation gain).
- `SlopeSummary` takes that DataFrame and produces: matplotlib charts saved to `static/summary.png` / `static/summary_sep.png`, and a `get_stats()` dict with per-run metrics (distance, vertical drop, avg/max speed in km/h, duration).

**Map** (`visualize_data.py`):
- `SlopeVisualizer` builds a folium map colored by speed (coolwarm colormap, lifts in gray) and saves it to `static/ski_map.html`.

**Web layer** (`app.py`):
- POST `/upload` → runs the full pipeline, writes `static/stats.json`, redirects to `/result`.
- GET `/result` → reads `stats.json` and passes it to `result.html` as `stats`. If `stats.json` doesn't exist, redirects to `/`.
- `static/stats.json` is the only state persisted between requests. It always reflects the last upload.

**Frontend** (`templates/`, `static/`):
- `upload.html` + `upload.js`: drag-and-drop GPX upload with loading spinner.
- `result.html`: Jinja2 template rendering stat cards, per-run table (speeds already in km/h from `get_stats()`), map iframe, and chart images.
- `style.css`: dark navy theme (`--bg: #0d1b2a`, `--accent: #4fc3f7`).

## Key Data Details

- GPX segments (`<trkseg>`) map 1:1 to `segment_id`. Lifts are identified by net elevation gain (`end_ele > start_ele`).
- The first point of each segment has `NaN` for distance/speed (no previous point). All speed calculations must use `.dropna()` or `.fillna(0)`.
- Speeds are stored internally as m/s; `get_stats()` converts to km/h before writing to `stats.json`.
- `avg_gradient_pct` in `stats.json` is negative for downhill runs (end lower than start). Templates display `abs()`.
