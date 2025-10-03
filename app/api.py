"""
FastAPI application for SmartMailer
Provides REST API endpoints for email management
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from loguru import logger

from app.models import Email, ProcessingLog, get_db, create_tables
from app.database import DatabaseManager
from app.config import settings
from app.notifications import NotificationManager


# Pydantic models for API
class EmailResponse(BaseModel):
    id: int
    uid: str
    subject: str
    sender: str
    recipient: str
    date_received: datetime
    classification: str
    auto_reply_sent: bool
    notification_sent: bool
    processed_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class EmailStats(BaseModel):
    total_emails: int
    normal_emails: int
    important_emails: int
    auto_replies_sent: int
    notifications_sent: int
    processing_rate: float


class ProcessingLogResponse(BaseModel):
    id: int
    email_id: int
    action: str
    status: str
    message: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    database_connected: bool
    email_connected: bool
    telegram_connected: bool


# Initialize FastAPI app
app = FastAPI(
    title="SmartMailer API",
    description="API pour l'application intelligente de gestion d'emails",
    version=settings.app_version
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
db_manager = DatabaseManager()
notification_manager = NotificationManager()


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    try:
        # Create database tables
        create_tables()
        logger.info("Database tables created successfully")
        
        # Test connections
        await test_connections()
        
    except Exception as e:
        logger.error(f"Startup error: {e}")


async def test_connections():
    """Test all external connections"""
    try:
        # Test database
        stats = db_manager.get_processing_stats()
        logger.info("Database connection: OK")
        
        # Test Telegram
        telegram_test = notification_manager.test_all_notifications()
        if telegram_test.get('telegram_connection'):
            logger.info("Telegram connection: OK")
        else:
            logger.warning("Telegram connection: FAILED")
            
    except Exception as e:
        logger.error(f"Connection test error: {e}")


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "SmartMailer API",
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Test database
        db_connected = True
        try:
            db_manager.get_processing_stats()
        except:
            db_connected = False
        
        # Test Telegram
        telegram_connected = notification_manager.telegram.test_connection()
        
        return HealthResponse(
            status="healthy" if db_connected else "unhealthy",
            timestamp=datetime.utcnow(),
            version=settings.app_version,
            database_connected=db_connected,
            email_connected=True,  # Will be tested in worker
            telegram_connected=telegram_connected
        )
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")


@app.get("/emails", response_model=List[EmailResponse])
async def get_emails(
    classification: Optional[str] = Query(None, description="Filter by classification"),
    limit: int = Query(50, ge=1, le=1000, description="Number of emails to return"),
    db: Session = Depends(get_db)
):
    """Get emails with optional filtering"""
    try:
        if classification:
            emails = db_manager.get_emails_by_classification(classification, limit)
        else:
            emails = db_manager.get_recent_emails(limit)
        
        return [EmailResponse.from_orm(email) for email in emails]
        
    except Exception as e:
        logger.error(f"Error getting emails: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve emails")


@app.get("/emails/{email_id}", response_model=EmailResponse)
async def get_email(email_id: int, db: Session = Depends(get_db)):
    """Get specific email by ID"""
    try:
        email = db.query(Email).filter(Email.id == email_id).first()
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        
        return EmailResponse.from_orm(email)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting email {email_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve email")


@app.get("/stats", response_model=EmailStats)
async def get_stats():
    """Get processing statistics"""
    try:
        stats = db_manager.get_processing_stats()
        return EmailStats(**stats)
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")


@app.get("/logs", response_model=List[ProcessingLogResponse])
async def get_logs(
    email_id: Optional[int] = Query(None, description="Filter by email ID"),
    limit: int = Query(100, ge=1, le=1000, description="Number of logs to return")
):
    """Get processing logs"""
    try:
        logs = db_manager.get_processing_logs(email_id, limit)
        return [ProcessingLogResponse.from_orm(log) for log in logs]
        
    except Exception as e:
        logger.error(f"Error getting logs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve logs")


@app.post("/test/telegram")
async def test_telegram():
    """Test Telegram notification"""
    try:
        results = notification_manager.test_all_notifications()
        
        if results.get('telegram_message'):
            return {"status": "success", "message": "Test message sent successfully"}
        else:
            return {"status": "error", "message": "Failed to send test message"}
            
    except Exception as e:
        logger.error(f"Telegram test error: {e}")
        raise HTTPException(status_code=500, detail="Telegram test failed")


@app.post("/emails/{email_id}/resend-notification")
async def resend_notification(email_id: int, db: Session = Depends(get_db)):
    """Resend notification for an email"""
    try:
        email = db.query(Email).filter(Email.id == email_id).first()
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        
        if email.classification != 'important':
            raise HTTPException(status_code=400, detail="Only important emails can have notifications resent")
        
        # Prepare email data
        email_data = {
            'sender': email.sender,
            'subject': email.subject,
            'date_received': email.date_received,
            'content': email.content
        }
        
        # Send notification
        success = notification_manager.notify_important_email(email_data)
        
        if success:
            # Update status
            db_manager.mark_notification_sent(email_id)
            db_manager.log_processing_action(
                email_id, 'notification_resent', 'success', 'Notification resent via API'
            )
            
            return {"status": "success", "message": "Notification sent successfully"}
        else:
            db_manager.log_processing_action(
                email_id, 'notification_resent', 'error', 'Failed to resend notification'
            )
            raise HTTPException(status_code=500, detail="Failed to send notification")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resending notification: {e}")
        raise HTTPException(status_code=500, detail="Failed to resend notification")


@app.delete("/emails/{email_id}")
async def delete_email(email_id: int, db: Session = Depends(get_db)):
    """Delete an email (for maintenance)"""
    try:
        email = db.query(Email).filter(Email.id == email_id).first()
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        
        db.delete(email)
        db.commit()
        
        logger.info(f"Email {email_id} deleted")
        return {"status": "success", "message": "Email deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting email: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete email")


@app.post("/maintenance/cleanup")
async def cleanup_old_emails(
    days: int = Query(30, ge=1, le=365, description="Delete emails older than N days")
):
    """Clean up old emails"""
    try:
        count = db_manager.cleanup_old_emails(days)
        return {
            "status": "success",
            "message": f"Cleaned up {count} old emails",
            "deleted_count": count
        }
        
    except Exception as e:
        logger.error(f"Error cleaning up emails: {e}")
        raise HTTPException(status_code=500, detail="Failed to cleanup emails")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
