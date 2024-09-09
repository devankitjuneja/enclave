import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import functools


DATABASE_URL = os.environ.get('SQLALCHEMY_URI')

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
