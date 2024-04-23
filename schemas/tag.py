from pydantic import BaseModel
from models.text import Text

class TagResponse(BaseModel):
    original_text: Text
    new_tag: Text