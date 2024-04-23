from pydantic import BaseModel
from models.text import Text

class SpellingResponse(BaseModel):
    original_text: Text
    new_text: Text