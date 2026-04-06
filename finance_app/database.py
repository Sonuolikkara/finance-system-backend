"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Database URL - using SQLite for simplicity
DATABASE_URL = "sqlite:///./finance.db"

# Create engine with check_same_thread=False for SQLite
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for all models
Base = declarative_base()


def get_db():
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database and create all tables
    """
    Base.metadata.create_all(bind=engine)
