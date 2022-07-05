import pytest
from fastapi.testclient import TestClient

from app import crud, models, schemas
from app.database import SessionLocal, engine
from app.main import app
from app.services import summarize_text

models.Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def db():
    yield SessionLocal()
    with engine.begin() as conn:
        models.Text.__table__.drop(conn)


@pytest.fixture(scope="session")
def test_client():
    client = TestClient(app)
    return client


def test_create_and_read_text(db):
    text_str = "This is about a duck that swam in the lake. One day he ate bread and he was happy."
    text = schemas.TextCreate(text=text_str)
    res = crud.create_text(db, text=text)
    actual_text = crud.get_text(db, res.id)
    assert actual_text.text == text_str


def test_text_summarization(db):
    text_str = "This is about a duck that swam in the lake. One day he ate bread and he was happy."
    text = schemas.TextCreate(text=text_str)
    res = crud.create_text(db, text=text)
    summarized_text = summarize_text(db, res.id)
    assert type(summarized_text) == str


def test_e2e_text_id_exists(test_client):
    text_str = "This is about a duck that swam in the lake. One day he ate bread and he was happy."
    response = test_client.put("/add_text/", json={"text": text_str})
    text_id = response.json()["id"]
    assert response.status_code == 200
    assert type(text_id) == int
    response = test_client.get(f"/summary/{text_id}")
