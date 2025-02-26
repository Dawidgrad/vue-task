from datetime import date
from pydantic import BaseModel, Field

class Article(BaseModel):
    id: int = Field(None, description="Article ID (auto-generated)")
    title: str = Field(..., min_length=3, max_length=100, description="Article title")
    content: str = Field(..., min_length=10, description="Article content")
    release_date: date = Field(..., description="Release date in YYYY-MM-DD format")