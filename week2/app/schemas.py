from __future__ import annotations

from pydantic import BaseModel, field_validator


class NoteCreateRequest(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("content is required")
        return cleaned


class NoteResponse(BaseModel):
    id: int
    content: str
    created_at: str


class ActionItemExtractRequest(BaseModel):
    text: str
    save_note: bool = False

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("text is required")
        return cleaned


class ActionItemExtractedResponse(BaseModel):
    id: int
    text: str


class ActionItemExtractResponse(BaseModel):
    note_id: int | None
    items: list[ActionItemExtractedResponse]


class ActionItemResponse(BaseModel):
    id: int
    note_id: int | None
    text: str
    done: bool
    created_at: str


class ActionItemMarkDoneRequest(BaseModel):
    done: bool = True


class ActionItemMarkDoneResponse(BaseModel):
    id: int
    done: bool