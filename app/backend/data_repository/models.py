from pydantic import BaseModel


class ScientificAbstract(BaseModel):
    doi: str
    title: str
    author: str
    abstract_content: str