import os
import pytest

from ..app.services import extract
from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


def test_extract_action_items_llm_with_bulleted_note(monkeypatch):
    note = """
    Meeting notes:
    - Set up database
    - Write tests
    """.strip()

    captured = {}

    def fake_chat(**kwargs):
        captured.update(kwargs)
        return {
            "message": {
                "content": '["Set up database", "Write tests"]',
            }
        }

    monkeypatch.setattr(extract, "chat", fake_chat)

    items = extract_action_items_llm(note)

    assert items == ["Set up database", "Write tests"]
    assert captured["model"] == "llama3.1:8b"
    assert captured["format"] == "json"


def test_extract_action_items_llm_with_keyword_prefixed_note(monkeypatch):
    note = """
    TODO: Update onboarding docs
    ACTION: Notify the QA team
    NEXT: Schedule release meeting
    """.strip()

    def fake_chat(**kwargs):
        return {
            "message": {
                "content": (
                    '["Update onboarding docs", '
                    '"Notify the QA team", '
                    '"Schedule release meeting"]'
                ),
            }
        }

    monkeypatch.setattr(extract, "chat", fake_chat)

    items = extract_action_items_llm(note)

    assert items == [
        "Update onboarding docs",
        "Notify the QA team",
        "Schedule release meeting",
    ]


def test_extract_action_items_llm_with_empty_input(monkeypatch):
    def fake_chat(**kwargs):
        return {
            "message": {
                "content": "[]",
            }
        }

    monkeypatch.setattr(extract, "chat", fake_chat)

    items = extract_action_items_llm("")

    assert items == []
