from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    photo_path = Column(String)
    work_hours = relationship("WorkHour", back_populates="employee")

class WorkHour(Base):
    __tablename__ = "work_hours"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    date = Column(DateTime)
    hours_worked = Column(Integer)

    employee = relationship("Employee", back_populates="work_hours")
