from pydantic import BaseModel
from typing import List, Optional

class FaceEmbedding(BaseModel):
    name: str
    embedding: List[float]
    image_url: Optional[str] = None

class CelebrityMatch(BaseModel):
    name: str
    similarity: float
    image_url: Optional[str] = None
