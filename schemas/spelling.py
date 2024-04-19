from pydantic import BaseModel
from models.text import Text

class SpellingResponse(BaseModel):
    text: Text