# London Daily Dashboard

An automated data pipeline and dashboard that collects public data about London (exchange rates, weather and Tube status) scheduled hourly (GitHub may delay or skip runs, so the effective interval varies), stores it in SQLite and presents it in a Streamlit app.

**Live demo:** [https://london-dashboard-gxfawvqlj2iyd536fxmtea.streamlit.app/](https://london-dashboard-gxfawvqlj2iyd536fxmtea.streamlit.app/)

![Dashboard screenshot](docs/dashboard.png)

![Tests](https://github.com/matheuscyles-bot/london-dashboard/actions/workflows/tests.yml/badge.svg)

## What it shows

- **Exchange rates:** GBP to BRL, EUR and USD, with today's rate compared to the average over 30 days, 6 months or 1 year, plus a history chart for each period.
- **Weather:** current temperature, precipitation and the maximum chance of rain over the next 6 hours, for Woking.
- **London Underground:** the status of every Tube line, with the lines that have problems highlighted.

## How it works

```
scheduled hourly (GitHub may delay or skip runs, so the effective interval varies)
        |
        v
collectors (cambio.py, clima.py, metro.py)
        |
        v
SQLite (cambio.db, committed to the `data` branch)
        |
        v
Streamlit dashboard (downloads the database from the `data` branch)
```

Data sources (all public, no API key required):

| Data | API |
|---|---|
| Exchange rates | [Frankfurter](https://frankfurter.dev) |
| Weather | [Open-Meteo](https://open-meteo.com) |
| Tube status | [TfL Unified API](https://api.tfl.gov.uk) |

### Project structure

| File | Responsibility |
|---|---|
| `cambio.py`, `clima.py`, `metro.py` | Collectors: call one API each and return clean Python data, or `None` on failure |
| `database.py` | Creates the tables and saves collected data to SQLite |
| `run_pipeline.py` | Orchestrator: runs every collector and saves the results |
| `dashboard.py` | Streamlit app that reads the database and renders the charts |
| `test_cambio.py` | Unit tests for the exchange-rate summary logic |
| `.github/workflows/pipeline.yml` | Scheduled data collection |
| `.github/workflows/tests.yml` | Runs the tests on every push |

## Design decisions

- **Separation of responsibilities.** Collecting, storing, orchestrating and displaying are in separate files, so each part can change or be tested without touching the others.
- **Failures are isolated.** Each collector catches request errors and returns `None`. The pipeline skips what failed and still saves the rest, so one API outage never blocks the other two.
- **Database on a separate `data` branch.** Committing a database that changes every 3 hours to `main` would bury the code history under data commits. The workflow checks out the `data` branch, takes the latest scripts from `main`, runs the pipeline and commits only `cambio.db`.
- **SQLite instead of a database server.** The data volume is tiny and the workload is append-and-read, so SQLite needs no extra infrastructure and keeps the project free to run.
- **Dashboard reads the database from GitHub.** `dashboard.py` downloads `cambio.db` from the `data` branch (cached for 10 minutes) and falls back to a local copy if the download fails.
- **Tested logic.** The summary calculation is covered by tests, including the empty-history edge case that originally raised a `ZeroDivisionError`.

## Run locally

```bash
git clone https://github.com/matheuscyles-bot/london-dashboard.git
cd london-dashboard

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python run_pipeline.py        # collect data into cambio.db
streamlit run dashboard.py    # open the dashboard
```

Each collector can also be run on its own, for example `python cambio.py`, to see its output in the terminal.

## Tests and linting

```bash
pytest -v
ruff check .
ruff format .
```

## Limitations and next steps

- The scheduled workflow is best-effort: GitHub may delay cron runs, so collections are not guaranteed to happen at exact times.
- The weather collector covers a single location (Woking). Supporting several cities would require a `cidade` column and a city selector.
- Exchange-rate collectors assume a well-formed API response; a response without the expected fields would raise an error instead of being handled.
- A SQLite file in a Git branch does not scale. Moving to a hosted Postgres database would be the natural next step.
- Tests cover the calculation logic only; the collectors and database functions are not yet tested.