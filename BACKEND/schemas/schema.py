from pydantic import BaseModel
from typing import List

# Image Schema
class ImageBase(BaseModel):
    id: int
    filename: str   # ✅ matches your model

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode


# Summary Schema
class SummaryBase(BaseModel):
    id: int
    filename: str
    content: str
    summary: str    # ✅ matches your model

    class Config:
        from_attributes = True


# PDF Schema with nested relations
class PDFBase(BaseModel):
    id: int          # ✅ use id (matches Fileupload model)
    filename: str
    images: List[ImageBase] = []
    summaries: List[SummaryBase] = []

    class Config:
        from_attributes = True
