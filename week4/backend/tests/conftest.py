import os
import tempfile
from collections.abc import Generator

import pytest
from backend.app.db import get_db
from backend.app.main import app
from backend.app.models import Base
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# @pytest.fixture()
# def client() -> Generator[TestClient, None, None]:
#     db_fd, db_path = tempfile.mkstemp()
#     os.close(db_fd)

#     engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
#     TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     Base.metadata.create_all(bind=engine)

#     def override_get_db():
#         session = TestingSessionLocal()
#         try:
#             yield session
#             session.commit()
#         except Exception:
#             session.rollback()
#             raise
#         finally:
#             session.close()

#     app.dependency_overrides[get_db] = override_get_db

#     with TestClient(app) as c:
#         yield c

#     os.unlink(db_path)


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)

    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    # --- PERUBAHAN ADA DI SINI ---
    # Memastikan engine memutus semua koneksi sebelum file dihapus (khusus Windows)
    engine.dispose()

    # Tambahkan sedikit jeda dan try-except agar tidak crash jika masih terkunci
    import time

    time.sleep(0.1)
    try:
        os.unlink(db_path)
    except PermissionError:
        pass  # Abaikan jika Windows masih menahannya
