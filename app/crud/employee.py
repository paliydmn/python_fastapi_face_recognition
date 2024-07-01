import os
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.employee import Employee, WorkHour
from app.schemas.employee import EmployeeCreate

def get_employees(db: Session):
    return db.query(Employee).all()

def get_employee_work_hours(db: Session, employee_id: int):
    return db.query(WorkHour).filter(WorkHour.employee_id == employee_id).all()



def create_employee(db: Session, employee: EmployeeCreate, photo_path: str):
    db_employee = Employee(name=employee.name, photo_path=photo_path)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


# def create_employee(db: Session, name: str, photo: UploadFile):
#     employee = Employee(name=name)
#     db.add(employee)
#     db.commit()
#     db.refresh(employee)
#     # Here you should save the photo to a file and associate it with the employee
#     return employee

def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()

def delete_employee(db: Session, employee_id: int):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee:
        # Delete the photo file
        if employee.photo_path and os.path.exists(employee.photo_path):
            os.remove(employee.photo_path)
        db.query(WorkHour).filter(WorkHour.employee_id == employee.id).delete()
        db.delete(employee)
        db.commit()
    else:
        raise ValueError("Employee not found")