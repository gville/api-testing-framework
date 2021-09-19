from pydantic import BaseModel

class Error(BaseModel):
    detail: str
    status: int
    title: str
    type: str
