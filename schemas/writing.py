from pydantic import BaseModel
from models.text import Text

class WritingResponse(BaseModel):
    text: Text