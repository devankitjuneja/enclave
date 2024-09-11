import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import functools


# Fetch environment variables
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL, )

# Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

@contextmanager
def db_session():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def with_db_session(func):
    """Decorator to inject a SQLAlchemy session into the decorated function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with db_session() as session:
            return func(*args, db_session=session, **kwargs)
    return wrapper

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
