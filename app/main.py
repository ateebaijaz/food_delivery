from fastapi import FastAPI
from app.database import SessionLocal
from sqlalchemy import text  # <-- import text here

app = FastAPI()

@app.get("/")
def root():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))  # wrap raw SQL in text()
        return {"message": "Database connected!"}
    finally:
        db.close()