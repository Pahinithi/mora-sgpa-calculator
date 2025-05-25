from pydantic import BaseModel
from typing import List


class Module(BaseModel):
    code: str
    title: str
    grade: str
    credits: float
    is_gpa: bool = True


class Semester(BaseModel):
    name: str
    modules: List[Module]
