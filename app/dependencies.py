from pathlib import Path

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from app.database import SessionLocal

HERE = Path("__file__").parent
MODEL_PATH = HERE.parent.joinpath("distilbart-cnn-6-6")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
