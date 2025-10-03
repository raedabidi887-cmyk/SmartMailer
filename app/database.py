"""
Database operations for SmartMailer
Handles email storage and retrieval
"""

from datetime import datetime
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from loguru import logger
from app.models import Email, ProcessingLog, get_db


class DatabaseManager:
    """Database manager for email operations"""
    
    def __init__(self):
        self.db = next(get_db())
    
    def save_email(self, email_data: Dict, classification: str) -> Optional[Email]:
        """
        Save email to database
        
        Args:
            email_data: Email data dictionary
            classification: 'normal' or 'important'
            
        Returns:
            Email object if saved successfully, None otherwise
        """
        try:
            # Check if email already exists
            existing_email = self.get_email_by_uid(email_data.get('uid'))
            if existing_email:
                logger.warning(f"Email {email_data.get('uid')} already exists in database")
                return existing_email
            
            # Create new email record
            email_record = Email(
                uid=email_data.get('uid'),
                subject=email_data.get('subject', ''),
                sender=email_data.get('sender', ''),
                recipient=email_data.get('recipient', ''),
                date_received=email_data.get('date_received', datetime.now()),
                content=email_data.get('content', ''),
                classification=classification,
                auto_reply_sent=False,
                notification_sent=False
            )
            
            self.db.add(email_record)
            self.db.commit()
            self.db.refresh(email_record)
            
            logger.info(f"Email saved to database: {email_record.id}")
            return email_record
            
        except Exception as e:
            logger.error(f"Error saving email to database: {e}")
            self.db.rollback()
            return None
    
    def get_email_by_uid(self, uid: str) -> Optional[Email]:
        """Get email by UID"""
        try:
            return self.db.query(Email).filter(Email.uid == uid).first()
        except Exception as e:
            logger.error(f"Error getting email by UID: {e}")
            return None
    
    def get_emails_by_classification(self, classification: str, limit: int = 100) -> List[Email]:
        """Get emails by classification"""
        try:
            return self.db.query(Email).filter(
                Email.classification == classification
            ).order_by(desc(Email.date_received)).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting emails by classification: {e}")
            return []
    
    def get_recent_emails(self, limit: int = 50) -> List[Email]:
        """Get recent emails"""
        try:
            return self.db.query(Email).order_by(
                desc(Email.date_received)
            ).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting recent emails: {e}")
            return []
    
    def update_email_status(self, email_id: int, **kwargs) -> bool:
        """Update email status"""
        try:
            email = self.db.query(Email).filter(Email.id == email_id).first()
            if not email:
                logger.error(f"Email with ID {email_id} not found")
                return False
            
            # Update fields
            for key, value in kwargs.items():
                if hasattr(email, key):
                    setattr(email, key, value)
            
            email.updated_at = datetime.utcnow()
            self.db.commit()
            
            logger.info(f"Email {email_id} status updated")
            return True
            
        except Exception as e:
            logger.error(f"Error updating email status: {e}")
            self.db.rollback()
            return False
    
    def mark_auto_reply_sent(self, email_id: int) -> bool:
        """Mark email as having auto-reply sent"""
        return self.update_email_status(email_id, auto_reply_sent=True)
    
    def mark_notification_sent(self, email_id: int) -> bool:
        """Mark email as having notification sent"""
        return self.update_email_status(email_id, notification_sent=True)
    
    def get_processing_stats(self) -> Dict:
        """Get processing statistics"""
        try:
            total_emails = self.db.query(Email).count()
            normal_emails = self.db.query(Email).filter(Email.classification == 'normal').count()
            important_emails = self.db.query(Email).filter(Email.classification == 'important').count()
            auto_replies_sent = self.db.query(Email).filter(Email.auto_reply_sent == True).count()
            notifications_sent = self.db.query(Email).filter(Email.notification_sent == True).count()
            
            return {
                'total_emails': total_emails,
                'normal_emails': normal_emails,
                'important_emails': important_emails,
                'auto_replies_sent': auto_replies_sent,
                'notifications_sent': notifications_sent,
                'processing_rate': (auto_replies_sent + notifications_sent) / max(total_emails, 1) * 100
            }
            
        except Exception as e:
            logger.error(f"Error getting processing stats: {e}")
            return {}
    
    def log_processing_action(self, email_id: int, action: str, status: str, message: str = "") -> bool:
        """Log processing action"""
        try:
            log_entry = ProcessingLog(
                email_id=email_id,
                action=action,
                status=status,
                message=message
            )
            
            self.db.add(log_entry)
            self.db.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Error logging processing action: {e}")
            self.db.rollback()
            return False
    
    def get_processing_logs(self, email_id: Optional[int] = None, limit: int = 100) -> List[ProcessingLog]:
        """Get processing logs"""
        try:
            query = self.db.query(ProcessingLog)
            
            if email_id:
                query = query.filter(ProcessingLog.email_id == email_id)
            
            return query.order_by(desc(ProcessingLog.timestamp)).limit(limit).all()
            
        except Exception as e:
            logger.error(f"Error getting processing logs: {e}")
            return []
    
    def cleanup_old_emails(self, days: int = 30) -> int:
        """Clean up old emails (for maintenance)"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Count emails to be deleted
            count = self.db.query(Email).filter(
                Email.date_received < cutoff_date
            ).count()
            
            # Delete old emails
            self.db.query(Email).filter(
                Email.date_received < cutoff_date
            ).delete()
            
            self.db.commit()
            
            logger.info(f"Cleaned up {count} old emails")
            return count
            
        except Exception as e:
            logger.error(f"Error cleaning up old emails: {e}")
            self.db.rollback()
            return 0
    
    def close(self):
        """Close database connection"""
        if self.db:
            self.db.close()
