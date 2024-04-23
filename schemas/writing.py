from pydantic import BaseModel
from models.guide import Guide
from models.text import Text

class WritingResponse(BaseModel):
    original_guide: Guide
    new_text: Text