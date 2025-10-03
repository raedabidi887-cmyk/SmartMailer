"""
Database models for SmartMailer
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

Base = declarative_base()


class Email(Base):
    """Email model for storing processed emails"""
    
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True, index=True, nullable=False)
    subject = Column(String, nullable=False)
    sender = Column(String, nullable=False)
    recipient = Column(String, nullable=False)
    date_received = Column(DateTime, nullable=False)
    content = Column(Text)
    classification = Column(String, nullable=False)  # 'normal' or 'important'
    auto_reply_sent = Column(Boolean, default=False)
    notification_sent = Column(Boolean, default=False)
    processed_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProcessingLog(Base):
    """Log model for tracking processing activities"""
    
    __tablename__ = "processing_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, nullable=False)
    action = Column(String, nullable=False)  # 'fetched', 'classified', 'replied', 'notified'
    status = Column(String, nullable=False)  # 'success', 'error'
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


# Database setup
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
