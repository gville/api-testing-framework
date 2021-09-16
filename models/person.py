from pydantic import BaseModel

class Person(BaseModel):
    fname: str
    lname: str
    person_id: int
    timestamp: str
