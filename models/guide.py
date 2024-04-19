from pydantic import BaseModel

class Guide(BaseModel):
    subject: str
    length: int
