# from fastapi import APIRouter, Depends, Request
# from fastapi.templating import Jinja2Templates
# from sqlalchemy.orm import Session
# from app.database.database import SessionLocal
# from app.crud import employee as crud_employee
# from app.models.employee import WorkHour
# import face_recognition
# import cv2
# import numpy as np
# import base64
# from datetime import datetime

# router = APIRouter()
# templates = Jinja2Templates(directory="app/templates")

# # Load known faces and their encodings from the database
# def load_known_faces(db: Session):
#     employees = crud_employee.get_employees(db)
#     known_face_encodings = []
#     known_face_ids = []
#     for employee in employees:
#         image = face_recognition.load_image_file(employee.photo_path)
#         encoding = face_recognition.face_encodings(image)[0]
#         known_face_encodings.append(encoding)
#         known_face_ids.append(employee.id)
#     return known_face_encodings, known_face_ids

# # In-memory store for active employees and their start times
# active_employees = {}

# @router.get("/")
# def index(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @router.post("/face_recognition")
# def face_recognition_endpoint(image: dict, db: Session = Depends(SessionLocal)):
#     image_data = image['image'].split(",")[1]
#     nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#     # Find all face locations and face encodings in the current frame
#     face_locations = face_recognition.face_locations(img)
#     face_encodings = face_recognition.face_encodings(img, face_locations)

#     known_face_encodings, known_face_ids = load_known_faces(db)

#     recognized = False
#     for face_encoding, face_location in zip(face_encodings, face_locations):
#         matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#         face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#         best_match_index = np.argmin(face_distances)
        
#         if matches[best_match_index]:
#             employee_id = known_face_ids[best_match_index]
#             recognized = True
            
#             # Start or stop counting hours
#             if employee_id in active_employees:
#                 # Stop counting
#                 start_time = active_employees.pop(employee_id)
#                 end_time = datetime.now()
#                 hours_worked = (end_time - start_time).total_seconds() / 3600.0
#                 work_hour = WorkHour(employee_id=employee_id, date=start_time, hours_worked=hours_worked)
#                 db.add(work_hour)
#                 db.commit()
#             else:
#                 # Start counting
#                 active_employees[employee_id] = datetime.now()
                
#             return {
#                 "recognized": recognized,
#                 "face_location": face_location,
#                 "active_employees": [{"id": id, "name": crud_employee.get_employee(db, id).name} for id in active_employees.keys()]
#             }

#     return {
#         "recognized": recognized,
#         "face_location": None,
#         "active_employees": [{"id": id, "name": crud_employee.get_employee(db, id).name} for id in active_employees.keys()]
#     }

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.crud import employee as crud_employee
from app.models.employee import WorkHour
import face_recognition
import cv2
import numpy as np
import base64
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load known faces and their encodings from the database
def load_known_faces(db: Session):
    employees = crud_employee.get_employees(db)
    known_face_encodings = []
    known_face_ids = []
    for employee in employees:
        image = face_recognition.load_image_file(f'app/{employee.photo_path}')
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_ids.append(employee.id)
    return known_face_encodings, known_face_ids

# In-memory store for active employees and their start times
active_employees = {}

@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

start_count = False

@router.post("/face_recognition")
async def face_recognition_endpoint(image: dict, db: Session = Depends(get_db)):
    image_data = image['image'].split(",")[1]
    nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(img)
    face_encodings = face_recognition.face_encodings(img, face_locations)

    known_face_encodings, known_face_ids = load_known_faces(db)
    
    recognized = False
    global start_count
    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            employee_id = known_face_ids[best_match_index]
            employee = crud_employee.get_employee(db, employee_id)
            recognized = True

            return {
                "recognized": recognized,
                "face_location": face_location,
                "employee_id": employee_id,
                "employee_name": employee.name,
                "employee_photo": employee.photo_path.split('/')[-1],
                "active_employees": [{"id": id, "name": crud_employee.get_employee(db, id).name} for id in active_employees.keys()]
            }

    return {
        "recognized": recognized,
        "face_location": None,
        "active_employees": [{"id": id, "name": crud_employee.get_employee(db, id).name} for id in active_employees.keys()]
    }


@router.post("/confirm_employee")
async def confirm_employee(employee_id: dict, db: Session = Depends(get_db)):
    print(employee_id)
    _id = employee_id['employee_id']
    print(_id)

    if _id in active_employees:
        # Stop counting
        start_time = active_employees.pop(_id)
        end_time = datetime.now()
        hours_worked = (end_time - start_time).total_seconds() / 3600.0
        work_hour = WorkHour(employee_id=_id, date=start_time.date(), hours_worked=hours_worked)
        db.add(work_hour)
        db.commit()
    else:
        # Start counting
        active_employees[_id] = datetime.now()

    if _id in active_employees:
        raise HTTPException(status_code=400, detail="Employee already active")
#    active_employees[_id] = datetime.now()
    print(f'Start: {start_count}')
    return {
        "active_employees": [{"id": id,"start_count": start_count , "name": crud_employee.get_employee(db, id).name} for id in active_employees.keys()]
    }

@router.get("/get_active_employees")
async def get_active_employees(db: Session = Depends(get_db)):
    active_list = []
    for employee_id, start_time in active_employees.items():
        employee = crud_employee.get_employee(db, employee_id)
        active_list.append({
            "id": employee_id,
            "name": employee.name,
            "start_time": start_time.isoformat()
        })
    return active_list