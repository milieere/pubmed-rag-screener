from typing import Optional, List
from pydantic import BaseModel


class ScientificAbstract(BaseModel):
    doi: Optional[str]
    title: Optional[str]
    authors: Optional[list]
    year: Optional[int]
    abstract_content: str

class UserQueryRecord(BaseModel):
    user_query: str
    abstracts: List[ScientificAbstract]