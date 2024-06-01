from pydantic import BaseModel
from typing import List

class TagResponse(BaseModel):
    new_tag: List[str]