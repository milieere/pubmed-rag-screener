from typing import Optional, List
from pydantic import BaseModel


class ScientificAbstract(BaseModel):
    doi: Optional[str] = None
    title: Optional[str] = None
    authors: Optional[list] = None
    year: Optional[int] = None
    abstract_content: str

class UserQueryRecord(BaseModel):
    user_query_id: str
    user_query: str
    user_query_llm_simplified: Optional[str] = None