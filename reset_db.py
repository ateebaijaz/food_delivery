# reset_db.py
from app.database import Base, engine
from app.models import user, restaurant  # make sure all models are imported

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)

print("Creating all tables...")
Base.metadata.create_all(bind=engine)

print("✅ Tables recreated successfully.")
