from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import (
    ActionItemExtractedResponse,
    ActionItemExtractRequest,
    ActionItemExtractResponse,
    ActionItemMarkDoneRequest,
    ActionItemMarkDoneResponse,
    ActionItemResponse,
)
from ..services.extract import extract_action_items, extract_action_items_llm


router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ActionItemExtractResponse)
def extract(payload: ActionItemExtractRequest) -> ActionItemExtractResponse:
    text = payload.text

    note_id: Optional[int] = None
    try:
        if payload.save_note:
            note_id = db.insert_note(text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc

    items = extract_action_items(text)
    try:
        ids = db.insert_action_items(items, note_id=note_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc

    return ActionItemExtractResponse(
        note_id=note_id,
        items=[ActionItemExtractedResponse(id=i, text=t) for i, t in zip(ids, items)],
    )


@router.post("/extract-llm", response_model=ActionItemExtractResponse)
def extract_llm(payload: ActionItemExtractRequest) -> ActionItemExtractResponse:
    text = payload.text

    note_id: Optional[int] = None
    try:
        if payload.save_note:
            note_id = db.insert_note(text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc

    try:
        items = extract_action_items_llm(text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc

    try:
        ids = db.insert_action_items(items, note_id=note_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc

    return ActionItemExtractResponse(
        note_id=note_id,
        items=[ActionItemExtractedResponse(id=i, text=t) for i, t in zip(ids, items)],
    )


@router.get("", response_model=list[ActionItemResponse])
def list_all(note_id: Optional[int] = None) -> list[ActionItemResponse]:
    rows = db.list_action_items(note_id=note_id)
    return [
        ActionItemResponse(
            id=r["id"],
            note_id=r["note_id"],
            text=r["text"],
            done=bool(r["done"]),
            created_at=r["created_at"],
        )
        for r in rows
    ]


@router.post("/{action_item_id}/done", response_model=ActionItemMarkDoneResponse)
def mark_done(action_item_id: int, payload: ActionItemMarkDoneRequest) -> ActionItemMarkDoneResponse:
    done = payload.done
    db.mark_action_item_done(action_item_id, done)
    return ActionItemMarkDoneResponse(id=action_item_id, done=done)


