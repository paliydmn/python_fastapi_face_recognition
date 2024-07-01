from fastapi import FastAPI
from app.routes import employee, index
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#app.include_router(employee.router, prefix="/employees", tags=["employees"])
app.include_router(employee.router)
app.include_router(index.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# CORS middleware (optional, add as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as per your security requirements
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Employee Working Hours Tracker!"}
