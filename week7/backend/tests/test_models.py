from backend.app.models import Base, Note, Tag


def test_note_tag_many_to_many_mapping_exists():
    assert "tags" in Base.metadata.tables
    assert "note_tags" in Base.metadata.tables

    note = Note(title="N1", content="C1")
    tag = Tag(name="urgent")
    note.tags.append(tag)

    assert tag in note.tags
    assert note in tag.notes
