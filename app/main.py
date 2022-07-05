from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import engine
from app.dependencies import get_db
from app.services import summarize_text

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

from logging import getLogger

logger = getLogger("Main")


@app.put("/add_text/", response_model=schemas.TextReturn)
def create_text(text: schemas.TextCreate, db: Session = Depends(get_db)):
    text_model = crud.create_text(db, text=text)
    return schemas.TextReturn(id=text_model.id)


@app.get("/summary/{text_id}", response_model=schemas.Summary)
def get_summary(text_id: int, db: Session = Depends(get_db)):
    try:
        summary = summarize_text(db, text_id)
    except Exception as e:
        logger.error("Error caught for text id: {text_id}")
        raise e

    if not summary:
        raise HTTPException(status_code=404, detail="Text id not found")

    return summary
