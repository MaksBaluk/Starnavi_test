from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

engine = create_engine(settings.get_sqlite_url)
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
