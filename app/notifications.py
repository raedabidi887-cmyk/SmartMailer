"""
Notification module for SmartMailer
Handles Telegram notifications for important emails
"""

import requests
from typing import Dict, Optional
from loguru import logger
from app.config import settings


class TelegramNotifier:
    """Telegram notification handler"""
    
    def __init__(self):
        self.bot_token = settings.telegram_bot_token
        self.chat_id = settings.telegram_chat_id
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_notification(self, email_data: Dict) -> bool:
        """
        Send Telegram notification for important email
        
        Args:
            email_data: Email data dictionary
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            message = self._format_notification_message(email_data)
            return self._send_telegram_message(message)
            
        except Exception as e:
            logger.error(f"Error sending Telegram notification: {e}")
            return False
    
    def _format_notification_message(self, email_data: Dict) -> str:
        """Format notification message for Telegram"""
        
        sender = email_data.get('sender', 'Unknown')
        subject = email_data.get('subject', 'No Subject')
        date_received = email_data.get('date_received', '')
        
        # Format date
        if date_received:
            try:
                date_str = date_received.strftime('%d/%m/%Y à %H:%M')
            except:
                date_str = str(date_received)
        else:
            date_str = 'Date inconnue'
        
        # Get content preview
        content = email_data.get('content', '')
        content_preview = content[:150] + "..." if len(content) > 150 else content
        
        # Create message
        message = f"""🚨 <b>Email Important Reçu</b>

📧 <b>Expéditeur:</b> {sender}
📝 <b>Sujet:</b> {subject}
📅 <b>Date:</b> {date_str}

📄 <b>Aperçu:</b>
{content_preview}

<i>Notification SmartMailer</i>"""
        
        return message
    
    def _send_telegram_message(self, message: str) -> bool:
        """Send message to Telegram"""
        try:
            url = f"{self.base_url}/sendMessage"
            
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info("Telegram notification sent successfully")
                return True
            else:
                logger.error(f"Telegram API error: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Telegram request error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending Telegram message: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test Telegram bot connection"""
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                bot_info = response.json()
                if bot_info.get('ok'):
                    logger.info(f"Telegram bot connection successful: @{bot_info['result']['username']}")
                    return True
            
            logger.error(f"Telegram bot connection failed: {response.text}")
            return False
            
        except Exception as e:
            logger.error(f"Telegram connection test error: {e}")
            return False
    
    def send_test_message(self) -> bool:
        """Send a test message to verify configuration"""
        try:
            test_message = """🧪 <b>Test SmartMailer</b>

Ce message confirme que votre configuration Telegram fonctionne correctement.

<i>SmartMailer est prêt à vous notifier des emails importants !</i>"""
            
            return self._send_telegram_message(test_message)
            
        except Exception as e:
            logger.error(f"Error sending test message: {e}")
            return False


class NotificationManager:
    """Main notification manager"""
    
    def __init__(self):
        self.telegram = TelegramNotifier()
    
    def notify_important_email(self, email_data: Dict) -> bool:
        """Send notification for important email"""
        try:
            logger.info(f"Sending notification for important email: {email_data.get('subject', '')[:50]}...")
            return self.telegram.send_notification(email_data)
            
        except Exception as e:
            logger.error(f"Error in notification manager: {e}")
            return False
    
    def test_all_notifications(self) -> Dict[str, bool]:
        """Test all notification channels"""
        results = {}
        
        # Test Telegram
        try:
            results['telegram_connection'] = self.telegram.test_connection()
            if results['telegram_connection']:
                results['telegram_message'] = self.telegram.send_test_message()
            else:
                results['telegram_message'] = False
        except Exception as e:
            logger.error(f"Telegram test error: {e}")
            results['telegram_connection'] = False
            results['telegram_message'] = False
        
        return results
