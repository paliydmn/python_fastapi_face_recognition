import os
from dotenv import load_dotenv
from app.database.database import Base, engine
from app.models import employee  # Ensure this imports all models

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = "sqlite:///./face_tracking.db"
engine = create_engine(DATABASE_URL)

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created.")
