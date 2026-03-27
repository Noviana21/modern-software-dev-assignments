from collections.abc import Iterator

from backend.app.db import get_db
from backend.app.main import app


def test_get_stats_returns_note_count(client):
    client.post("/notes/", json={"title": "A", "content": "one"})
    client.post("/notes/", json={"title": "B", "content": "two"})

    r = client.get("/api/stats")

    assert r.status_code == 200, r.text
    data = r.json()
    assert "note_count" in data
    assert isinstance(data["note_count"], int)
    assert data["note_count"] == 2


def test_get_stats_returns_500_on_db_failure(client):
    class FailingSession:
        def execute(self, *_args, **_kwargs):
            raise RuntimeError("DB failure")

    def override_get_db() -> Iterator[FailingSession]:
        yield FailingSession()

    app.dependency_overrides[get_db] = override_get_db
    try:
        r = client.get("/api/stats")
        assert r.status_code == 500
        assert r.json() == {"detail": "Internal Server Error"}
    finally:
        app.dependency_overrides.pop(get_db, None)