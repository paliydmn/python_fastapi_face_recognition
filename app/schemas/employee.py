from pydantic import BaseModel

class EmployeeBase(BaseModel):
    name: str

class EmployeeCreate(BaseModel):
    name: str

class Employee(EmployeeBase):
    id: int
    photo_path: str

    class Config:
        orm_mode = True
