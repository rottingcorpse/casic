from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import settings

_connect_args = {}
if settings.DB_URL.startswith("sqlite"):
    _connect_args = {"check_same_thread": False}

engine = create_engine(settings.DB_URL, connect_args=_connect_args)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@contextmanager
def transaction(db: Session) -> Generator[Session, None, None]:
    """
    Context manager for handling database transactions.
    
    Automatically commits the transaction if no exception occurs,
    and rolls back if an exception is raised.
    
    Args:
        db: SQLAlchemy session
        
    Yields:
        The database session
        
    Example:
        with transaction(db):
            # Perform database operations
            db.add(some_object)
            db.flush()
            # If no exception, transaction will be committed
            # If exception occurs, transaction will be rolled back
    """
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
