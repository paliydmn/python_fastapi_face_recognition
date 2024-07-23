from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.database.database import Base, engine
from app.models import employee

DATABASE_URL = "sqlite:///./face_tracking.db"
engine = create_engine(DATABASE_URL)

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created.")
