"""
Email sending module for SmartMailer
Handles automatic replies via SMTP
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from typing import Dict, Optional
from loguru import logger
from app.config import settings


class EmailSender:
    """Email sender for automatic replies"""
    
    def __init__(self):
        self.smtp_server = settings.email_smtp_server
        self.smtp_port = settings.email_smtp_port
        self.email_address = settings.email_address
        self.email_password = settings.email_password
    
    def send_auto_reply(self, original_email: Dict, reply_content: str) -> bool:
        """
        Send automatic reply to an email
        
        Args:
            original_email: Original email data
            reply_content: Content of the reply
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = formataddr(("SmartMailer", self.email_address))
            msg['To'] = original_email.get('sender', '')
            msg['Subject'] = self._format_reply_subject(original_email.get('subject', ''))
            
            # Add reply content
            msg.attach(MIMEText(reply_content, 'html', 'utf-8'))
            
            # Send email
            success = self._send_email(msg)
            
            if success:
                logger.info(f"Auto-reply sent to {original_email.get('sender', '')}")
            else:
                logger.error(f"Failed to send auto-reply to {original_email.get('sender', '')}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending auto-reply: {e}")
            return False
    
    def _format_reply_subject(self, original_subject: str) -> str:
        """Format reply subject"""
        if original_subject.startswith('Re: '):
            return original_subject
        else:
            return f"Re: {original_subject}"
    
    def _send_email(self, msg: MIMEMultipart) -> bool:
        """Send email via SMTP"""
        try:
            # Create SSL context
            context = ssl.create_default_context()
            
            # Connect to SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_address, self.email_password)
                
                # Send email
                text = msg.as_string()
                server.sendmail(self.email_address, msg['To'], text)
                
            return True
            
        except Exception as e:
            logger.error(f"SMTP error: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test SMTP connection"""
        try:
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_address, self.email_password)
                
            logger.info("SMTP connection test successful")
            return True
            
        except Exception as e:
            logger.error(f"SMTP connection test failed: {e}")
            return False
