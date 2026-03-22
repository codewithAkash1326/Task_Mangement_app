from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker , declarative_base
from src.utils.setings import setting
Base = declarative_base()


engine = create_engine(url=setting.DB_CONNECTION)

LocalSession = sessionmaker(bind=engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()