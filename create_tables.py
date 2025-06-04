from app.database import engine, Base
import app.models  # Make sure all models are imported
from app.models import user, restaurant 

def create_all_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_all_tables()
    print("Tables created!")
