"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create database engine with error handling
try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=10,
        max_overflow=20
    )
except Exception as e:
    print(f"❌ Database engine creation failed: {str(e)}")
    print("⚠️ Creating dummy engine to allow app startup")
    # Create a dummy engine that will fail gracefully when used
    engine = None

# Create session factory
try:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None
except Exception as e:
    print(f"❌ SessionLocal creation failed: {str(e)}")
    SessionLocal = None

# Create base class for models
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    if SessionLocal is None:
        raise Exception("Database not available - SessionLocal is None")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
