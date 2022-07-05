from pydantic import BaseModel


class TextBase(BaseModel):
    text: str

    class Config:
        orm_mode = True


class TextCreate(TextBase):
    pass


class TextReturn(BaseModel):
    id: int


class Summary(BaseModel):
    text: str
