from typing import Union

from sqlalchemy.orm import Session

from app.crud import get_text
from app.dependencies import model, tokenizer
from app.schemas import Summary


def summarize_text(db: Session, text_id: int) -> Union[Summary, None]:
    text = get_text(db, text_id)
    if not text:
        return None

    text = text.text

    input = tokenizer(text, return_tensors="pt")
    output = model.generate(**input)
    words = [tokenizer.decode(token) for token in output]
    return Summary(text=words[0])
