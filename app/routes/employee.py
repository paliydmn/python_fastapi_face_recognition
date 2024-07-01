import os
import math
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.database.database import SessionLocal, engine
from app.crud import employee as crud_employee
from app.schemas.employee import EmployeeCreate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/employees")
def employee_management(request: Request):
    return templates.TemplateResponse("employees.html", {"request": request})
@router.get("/employee_list")
def employee_list(request: Request):
    return templates.TemplateResponse("employee_list.html", {"request": request})

@router.get("/employees/list")
def get_employees(db: Session = Depends(get_db)):
    employees = crud_employee.get_employees(db)
    employees_data = []

    for employee in employees:
        work_hours = crud_employee.get_employee_work_hours(db, employee.id)
        work_hours_by_day = defaultdict(float)
        for wh in work_hours:
            work_hours_by_day[wh.date.strftime('%d-%m-%Y')] += wh.hours_worked

        # Format the data
        work_hours_summary = [
            {"date": date, "hours_worked": f'{int(hours // 1)}h. {int((hours % 1) * 60)}m.'}
            for date, hours in work_hours_by_day.items()
        ]

        employees_data.append({
            "id": employee.id,
            "name": employee.name,
            "photo_path": employee.photo_path,
            "work_hours": work_hours_summary
        })

    return JSONResponse(content={"employees": employees_data})


@router.post("/employees/delete")
def delete_employee(employee_id: int = Form(...), db: Session = Depends(get_db)):
    try:
        crud_employee.delete_employee(db=db, employee_id=employee_id)
        return JSONResponse(content={"status": "success"})
    except ValueError:
        return JSONResponse(content={"status": "error", "message": "Employee not found"}, status_code=404)

@router.post("/employees/add")
async def add_employee(request: Request, name: str = Form(...), photo: UploadFile = File(...), db: Session = Depends(get_db)):
    if not photo:
        raise HTTPException(status_code=400, detail="Photo file is required")
    
    photo_path = f"app/static/uploads/{photo.filename}"
    
    # Save the uploaded photo file
    with open(photo_path, "wb") as file:
        file.write(await photo.read())
    
    employee_data = EmployeeCreate(name=name)
    crud_employee.create_employee(db=db, employee=employee_data, photo_path=f"static/uploads/{photo.filename}")
    
    return templates.TemplateResponse("employees.html", {"request": request, "msg": "Employee added successfully"})
