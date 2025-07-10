from pydantic import BaseModel

class DataCreate(BaseModel):
    name: str
    age: int

class DataOut(DataCreate):
    id: int

    class Config:
        orm_mode = True
