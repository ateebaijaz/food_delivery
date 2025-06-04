from fastapi import FastAPI
from app.database import SessionLocal
from sqlalchemy import text
from app.routes import auth
from app.routes import user # <-- import text here
from app.routes import restaurant  # <-- import text here
app = FastAPI()

@app.get("/")
def root():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))  # wrap raw SQL in text()
        return {"message": "Database connected!"}
    finally:
        db.close()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(restaurant.router)