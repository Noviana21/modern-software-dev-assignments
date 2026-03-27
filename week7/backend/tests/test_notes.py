def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"


def test_list_notes_pagination_skip_0_limit_5(client):
    marker = "pagination-skip0"
    for i in range(10):
        r = client.post(
            "/notes/",
            json={"title": f"{marker}-{i}", "content": f"content-{i}"},
        )
        assert r.status_code == 201, r.text

    r = client.get(
        "/notes/",
        params={"q": marker, "skip": 0, "limit": 5, "sort": "id"},
    )
    assert r.status_code == 200, r.text
    items = r.json()

    assert len(items) == 5
    assert [item["title"] for item in items] == [
        f"{marker}-0",
        f"{marker}-1",
        f"{marker}-2",
        f"{marker}-3",
        f"{marker}-4",
    ]


def test_list_notes_pagination_skip_5_limit_5(client):
    marker = "pagination-skip5"
    for i in range(10):
        r = client.post(
            "/notes/",
            json={"title": f"{marker}-{i}", "content": f"content-{i}"},
        )
        assert r.status_code == 201, r.text

    r = client.get(
        "/notes/",
        params={"q": marker, "skip": 5, "limit": 5, "sort": "id"},
    )
    assert r.status_code == 200, r.text
    items = r.json()

    assert len(items) == 5
    assert [item["title"] for item in items] == [
        f"{marker}-5",
        f"{marker}-6",
        f"{marker}-7",
        f"{marker}-8",
        f"{marker}-9",
    ]


