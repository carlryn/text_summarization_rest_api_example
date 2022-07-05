from sqlalchemy.orm import Session

from . import models, schemas


def create_text(db: Session, text: schemas.TextCreate) -> models.Text:
    db_text = models.Text(**text.dict())
    db.add(db_text)
    db.commit()
    db.refresh(db_text)
    return db_text


def get_text(db: Session, text_id: int):
    return db.query(models.Text).filter(models.Text.id == text_id).first()
