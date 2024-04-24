from pydantic import BaseModel

class Guide(BaseModel):
    subject: str
    reader: str
    length: int
    style: str
