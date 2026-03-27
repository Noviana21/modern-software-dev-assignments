from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .db import apply_seed_if_needed, engine, get_db
from .models import Base, Note
from .routers import action_items as action_items_router
from .routers import notes as notes_router
from .schemas import StatsRead

app = FastAPI(title="Modern Software Dev Starter (Week 6)", version="0.1.0")

# Ensure data dir exists
Path("data").mkdir(parents=True, exist_ok=True)

# Mount static frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")


# Compatibility with FastAPI lifespan events; keep on_event for simplicity here
@app.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)
    apply_seed_if_needed()


@app.get("/")
async def root() -> FileResponse:
    return FileResponse("frontend/index.html")


@app.get("/api/stats", response_model=StatsRead)
def get_stats(db: Session = Depends(get_db)) -> StatsRead:
    try:
        note_count = db.execute(select(func.count(Note.id))).scalar_one()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc

    return StatsRead(note_count=note_count)


# Routers
app.include_router(notes_router.router)
app.include_router(action_items_router.router)


