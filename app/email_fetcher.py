"""
Email fetching module for SmartMailer
Supports Gmail and Outlook via IMAP
"""

import email
import ssl
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from imapclient import IMAPClient
from loguru import logger
from app.config import settings


class EmailFetcher:
    """Email fetcher for Gmail and Outlook"""
    
    def __init__(self):
        self.client: Optional[IMAPClient] = None
        self.connected = False
    
    def connect(self) -> bool:
        """Connect to email server"""
        try:
            # Create SSL context
            ssl_context = ssl.create_default_context()
            
            # Connect to IMAP server
            self.client = IMAPClient(
                settings.email_imap_server,
                port=settings.email_imap_port,
                ssl=True,
                ssl_context=ssl_context
            )
            
            # Login
            self.client.login(settings.email_address, settings.email_password)
            self.client.select_folder('INBOX')
            
            self.connected = True
            logger.info(f"Connected to {settings.email_provider} email server")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to email server: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from email server"""
        if self.client and self.connected:
            try:
                self.client.logout()
                self.connected = False
                logger.info("Disconnected from email server")
            except Exception as e:
                logger.error(f"Error disconnecting: {e}")
    
    def fetch_new_emails(self, since_days: int = 1) -> List[Dict]:
        """Fetch new emails from the last N days"""
        if not self.connected:
            if not self.connect():
                return []
        
        try:
            # Calculate date threshold
            since_date = datetime.now() - timedelta(days=since_days)
            
            # Search for emails since the date
            search_criteria = ['SINCE', since_date.strftime('%d-%b-%Y')]
            messages = self.client.search(search_criteria)
            
            if not messages:
                logger.info("No new emails found")
                return []
            
            # Limit to max emails per batch
            messages = messages[-settings.max_emails_per_batch:]
            
            # Fetch email data
            emails = []
            for msg_id in messages:
                try:
                    email_data = self._parse_email(msg_id)
                    if email_data:
                        emails.append(email_data)
                except Exception as e:
                    logger.error(f"Error parsing email {msg_id}: {e}")
                    continue
            
            logger.info(f"Fetched {len(emails)} new emails")
            return emails
            
        except Exception as e:
            logger.error(f"Error fetching emails: {e}")
            return []
    
    def _parse_email(self, msg_id: int) -> Optional[Dict]:
        """Parse email message"""
        try:
            # Fetch email data
            response = self.client.fetch([msg_id], ['RFC822', 'ENVELOPE', 'FLAGS'])
            
            if not response:
                return None
            
            msg_data = response[msg_id]
            raw_email = msg_data[b'RFC822']
            
            # Parse email
            email_message = email.message_from_bytes(raw_email)
            
            # Extract basic information
            subject = email_message.get('Subject', '')
            sender = email_message.get('From', '')
            recipient = email_message.get('To', settings.email_address)
            date_str = email_message.get('Date', '')
            
            # Parse date
            try:
                date_received = email.utils.parsedate_to_datetime(date_str)
            except:
                date_received = datetime.now()
            
            # Extract content
            content = self._extract_content(email_message)
            
            # Create email data
            email_data = {
                'uid': str(msg_id),
                'subject': subject,
                'sender': sender,
                'recipient': recipient,
                'date_received': date_received,
                'content': content,
                'raw_message': email_message
            }
            
            return email_data
            
        except Exception as e:
            logger.error(f"Error parsing email {msg_id}: {e}")
            return None
    
    def _extract_content(self, email_message) -> str:
        """Extract text content from email"""
        content = ""
        
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        content += payload.decode('utf-8', errors='ignore')
        else:
            payload = email_message.get_payload(decode=True)
            if payload:
                content = payload.decode('utf-8', errors='ignore')
        
        return content.strip()
    
    def mark_as_read(self, msg_id: int) -> bool:
        """Mark email as read"""
        try:
            if self.client and self.connected:
                self.client.add_flags([msg_id], [b'\\Seen'])
                return True
        except Exception as e:
            logger.error(f"Error marking email {msg_id} as read: {e}")
        return False
    
    def get_unread_count(self) -> int:
        """Get count of unread emails"""
        try:
            if self.client and self.connected:
                messages = self.client.search(['UNSEEN'])
                return len(messages)
        except Exception as e:
            logger.error(f"Error getting unread count: {e}")
        return 0
