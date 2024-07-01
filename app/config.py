import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./face_tracking.db")
