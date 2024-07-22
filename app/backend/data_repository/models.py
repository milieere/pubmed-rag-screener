from typing import Optional
from pydantic import BaseModel


class ScientificAbstract(BaseModel):
    doi: Optional[str]
    title: Optional[str]
    authors: Optional[list]
    year: Optional[int]
    abstract_content: str