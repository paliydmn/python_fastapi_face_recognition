
## Setup Instructions

1. **Clone the repository:**
    ```bash
   git clone https://github.com/paliydmn/python_fastapi_face_recognition.git employee_hours_tracker
   cd employee_hours_tracker
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Initialize the database:**
    ```bash
    python init_db.py
    ```

## Running the Project

1. **Run the FastAPI application using Uvicorn:**
    ```bash
    uvicorn app.main:app --reload
    ```

2. **Open your browser and navigate to:**
    ```
    http://127.0.0.1:8000
    ```

## API Documentation

The FastAPI framework provides interactive API documentation at the following URLs:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Usage
Important - the web Camera is required for application work!

- **Home Page:** View the live video stream for face recognition.
- **Employee Management:** Add new employees, view the list of employees, and manage employee data.
- **Employee List:** View the list of all employees along with their work hours.



