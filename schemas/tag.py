from pydantic import BaseModel
from models.text import Text

class TagResponse(BaseModel):
    hashtag: Text