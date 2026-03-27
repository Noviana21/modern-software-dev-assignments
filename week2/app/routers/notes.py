from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import NoteCreateRequest, NoteResponse


router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteResponse)
def create_note(payload: NoteCreateRequest) -> NoteResponse:
    try:
        note_id = db.insert_note(payload.content)
        note = db.get_note(note_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc
    
    return NoteResponse(
        id=note["id"],
        content=note["content"],
        created_at=note["created_at"],
    )


@router.get("", response_model=list[NoteResponse])
def list_all_notes() -> list[NoteResponse]:
    try:
        rows = db.list_notes()
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc
    
    return [
        NoteResponse(
            id=row["id"],
            content=row["content"],
            created_at=row["created_at"],
        )
        for row in rows
    ]


@router.get("/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int) -> NoteResponse:
    try:
        row = db.get_note(note_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc
    
    if row is None:
        raise HTTPException(status_code=404, detail="note not found")
    return NoteResponse(
        id=row["id"],
        content=row["content"],
        created_at=row["created_at"],
    )


