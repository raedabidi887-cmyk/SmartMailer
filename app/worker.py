"""
Main worker for SmartMailer
Orchestrates email processing workflow
"""

import time
import schedule
from datetime import datetime, timedelta
from typing import List, Dict
from loguru import logger

from app.config import settings
from app.email_fetcher import EmailFetcher
from app.email_classifier import EmailClassifier
from app.email_sender import EmailSender
from app.templates import TemplateManager
from app.notifications import NotificationManager
from app.database import DatabaseManager


class SmartMailerWorker:
    """Main worker for email processing"""
    
    def __init__(self):
        self.fetcher = EmailFetcher()
        self.classifier = EmailClassifier()
        self.sender = EmailSender()
        self.templates = TemplateManager()
        self.notifications = NotificationManager()
        self.db = DatabaseManager()
        
        self.running = False
        self.last_check = None
        
        logger.info("SmartMailer Worker initialized")
    
    def start(self):
        """Start the worker"""
        try:
            logger.info("Starting SmartMailer Worker...")
            
            # Test all connections
            if not self._test_connections():
                logger.error("Connection tests failed. Please check your configuration.")
                return False
            
            # Schedule email checking
            schedule.every(settings.check_interval_minutes).minutes.do(self.process_emails)
            
            self.running = True
            logger.info(f"Worker started. Checking emails every {settings.check_interval_minutes} minutes.")
            
            # Run initial check
            self.process_emails()
            
            # Main loop
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logger.info("Worker stopped by user")
            self.stop()
        except Exception as e:
            logger.error(f"Worker error: {e}")
            self.stop()
    
    def stop(self):
        """Stop the worker"""
        self.running = False
        self.fetcher.disconnect()
        self.db.close()
        logger.info("SmartMailer Worker stopped")
    
    def _test_connections(self) -> bool:
        """Test all external connections"""
        logger.info("Testing connections...")
        
        # Test email connection
        try:
            if not self.fetcher.connect():
                logger.error("Email connection failed")
                return False
            self.fetcher.disconnect()
            logger.info("✓ Email connection: OK")
        except Exception as e:
            logger.error(f"✗ Email connection failed: {e}")
            return False
        
        # Test SMTP connection
        try:
            if not self.sender.test_connection():
                logger.error("SMTP connection failed")
                return False
            logger.info("✓ SMTP connection: OK")
        except Exception as e:
            logger.error(f"✗ SMTP connection failed: {e}")
            return False
        
        # Test Telegram connection
        try:
            telegram_test = self.notifications.test_all_notifications()
            if telegram_test.get('telegram_connection'):
                logger.info("✓ Telegram connection: OK")
            else:
                logger.warning("⚠ Telegram connection: FAILED")
        except Exception as e:
            logger.error(f"✗ Telegram connection failed: {e}")
            return False
        
        # Test database
        try:
            stats = self.db.get_processing_stats()
            logger.info("✓ Database connection: OK")
        except Exception as e:
            logger.error(f"✗ Database connection failed: {e}")
            return False
        
        return True
    
    def process_emails(self):
        """Main email processing function"""
        try:
            logger.info("Starting email processing cycle...")
            start_time = datetime.now()
            
            # Connect to email server
            if not self.fetcher.connect():
                logger.error("Failed to connect to email server")
                return
            
            try:
                # Fetch new emails
                emails = self.fetcher.fetch_new_emails(since_days=1)
                
                if not emails:
                    logger.info("No new emails to process")
                    return
                
                logger.info(f"Processing {len(emails)} emails...")
                
                # Process each email
                processed_count = 0
                for email_data in emails:
                    try:
                        if self._process_single_email(email_data):
                            processed_count += 1
                    except Exception as e:
                        logger.error(f"Error processing email {email_data.get('uid', 'unknown')}: {e}")
                        continue
                
                # Update last check time
                self.last_check = datetime.now()
                
                # Log processing summary
                duration = (datetime.now() - start_time).total_seconds()
                logger.info(f"Processing cycle completed: {processed_count}/{len(emails)} emails processed in {duration:.2f}s")
                
            finally:
                self.fetcher.disconnect()
                
        except Exception as e:
            logger.error(f"Error in email processing cycle: {e}")
    
    def _process_single_email(self, email_data: Dict) -> bool:
        """Process a single email"""
        try:
            email_uid = email_data.get('uid')
            logger.info(f"Processing email: {email_data.get('subject', 'No Subject')[:50]}...")
            
            # Check if email already processed
            existing_email = self.db.get_email_by_uid(email_uid)
            if existing_email:
                logger.debug(f"Email {email_uid} already processed, skipping")
                return True
            
            # Classify email
            classification = self.classifier.classify_email(email_data)
            
            # Save email to database
            email_record = self.db.save_email(email_data, classification)
            if not email_record:
                logger.error(f"Failed to save email {email_uid} to database")
                return False
            
            # Log classification
            self.db.log_processing_action(
                email_record.id, 'classified', 'success', 
                f"Classified as {classification}"
            )
            
            # Process based on classification
            if classification == 'normal':
                return self._process_normal_email(email_record, email_data)
            elif classification == 'important':
                return self._process_important_email(email_record, email_data)
            else:
                logger.warning(f"Unknown classification: {classification}")
                return False
                
        except Exception as e:
            logger.error(f"Error processing single email: {e}")
            return False
    
    def _process_normal_email(self, email_record, email_data: Dict) -> bool:
        """Process normal email (send auto-reply)"""
        try:
            if not settings.auto_reply_enabled:
                logger.info("Auto-reply disabled, skipping")
                return True
            
            # Generate auto-reply content
            reply_content = self.templates.render_auto_reply(email_data)
            
            # Send auto-reply
            if self.sender.send_auto_reply(email_data, reply_content):
                # Update database
                self.db.mark_auto_reply_sent(email_record.id)
                self.db.log_processing_action(
                    email_record.id, 'auto_reply_sent', 'success', 
                    'Auto-reply sent successfully'
                )
                
                logger.info(f"Auto-reply sent for email {email_record.id}")
                return True
            else:
                self.db.log_processing_action(
                    email_record.id, 'auto_reply_sent', 'error', 
                    'Failed to send auto-reply'
                )
                logger.error(f"Failed to send auto-reply for email {email_record.id}")
                return False
                
        except Exception as e:
            logger.error(f"Error processing normal email: {e}")
            self.db.log_processing_action(
                email_record.id, 'auto_reply_sent', 'error', str(e)
            )
            return False
    
    def _process_important_email(self, email_record, email_data: Dict) -> bool:
        """Process important email (send notification)"""
        try:
            # Send Telegram notification
            if self.notifications.notify_important_email(email_data):
                # Update database
                self.db.mark_notification_sent(email_record.id)
                self.db.log_processing_action(
                    email_record.id, 'notification_sent', 'success', 
                    'Telegram notification sent successfully'
                )
                
                logger.info(f"Notification sent for important email {email_record.id}")
                return True
            else:
                self.db.log_processing_action(
                    email_record.id, 'notification_sent', 'error', 
                    'Failed to send Telegram notification'
                )
                logger.error(f"Failed to send notification for email {email_record.id}")
                return False
                
        except Exception as e:
            logger.error(f"Error processing important email: {e}")
            self.db.log_processing_action(
                email_record.id, 'notification_sent', 'error', str(e)
            )
            return False
    
    def get_status(self) -> Dict:
        """Get worker status"""
        return {
            'running': self.running,
            'last_check': self.last_check.isoformat() if self.last_check else None,
            'check_interval_minutes': settings.check_interval_minutes,
            'stats': self.db.get_processing_stats()
        }
    
    def force_check(self):
        """Force an immediate email check"""
        logger.info("Forcing immediate email check...")
        self.process_emails()


def main():
    """Main entry point"""
    # Configure logging
    logger.add(
        "logs/smartmailer.log",
        rotation="1 day",
        retention="30 days",
        level=settings.log_level
    )
    
    # Create logs directory
    import os
    os.makedirs("logs", exist_ok=True)
    
    # Start worker
    worker = SmartMailerWorker()
    try:
        worker.start()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        worker.stop()


if __name__ == "__main__":
    main()
