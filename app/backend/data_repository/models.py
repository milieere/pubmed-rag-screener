from typing import Optional, List
from pydantic import BaseModel


class ScientificAbstract(BaseModel):
    doi: Optional[str]
    title: Optional[str]
    authors: Optional[list]
    year: Optional[int]
    abstract_content: str

class UserQueryRecord(BaseModel):
    user_query_id: int
    user_query: str
    user_query_llm_simplified: Optional[str]