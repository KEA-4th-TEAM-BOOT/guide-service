from pydantic import BaseModel

class Guide(BaseModel):
    subject: str
    reader: str
    length: str
    style: str
