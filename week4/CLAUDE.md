# Claude Guidance for Week 4 Starter App

## Setup & Execution
- To run the application: `make run` (runs on http://localhost:8000)
- To run tests: `make test`
- To format code: `make format`
- To lint code: `make lint`

## Architecture
- **Backend:** FastAPI, located in `backend/`. Routers are in `backend/app/routers/`.
- **Database:** SQLite using SQLAlchemy, seed data is in `data/`.
- **Frontend:** Static files served by FastAPI in `frontend/`.

## Workflow Rules
1. **Testing First:** When adding a new endpoint in `backend/app/routers/`, always write the corresponding test in `backend/tests/` first.
2. **Formatting:** Before committing, always run `make format` to ensure Black formatting.
3. **Linting:** Ensure no Ruff errors by running `make lint`.

## Safe Commands
- `pytest backend/tests/`
- `black backend/`
- `ruff check backend/`