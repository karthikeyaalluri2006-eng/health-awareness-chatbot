"""
HealthAware AI - Database Connection Manager
Supports SQLite (local development zero-config) and PostgreSQL + pgvector (production).
Provides session management, table creation, and seed initialization.
"""

import os
from contextlib import contextmanager
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from database.models import Base

# Load environment variables
load_dotenv()

# Determine database path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_SQLITE_URL = f"sqlite:///{DATA_DIR / 'healthaware.db'}"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)

# Configure engine
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    pool_pre_ping=True
)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)


def init_db():
    """Create all tables and seed standard healthcare data if empty."""
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db_session():
    """Provide a transactional scope around a series of operations."""
    session: Session = SessionFactory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db():
    """Generator for dependency injection."""
    session: Session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
