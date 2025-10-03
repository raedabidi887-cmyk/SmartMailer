"""
Template management for SmartMailer
Handles email templates using Jinja2
"""

import os
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, Template
from loguru import logger
from app.config import settings


class TemplateManager:
    """Template manager for email responses"""
    
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = templates_dir
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=True
        )
        
        # Create templates directory if it doesn't exist
        os.makedirs(templates_dir, exist_ok=True)
        
        # Create default templates if they don't exist
        self._create_default_templates()
    
    def _create_default_templates(self):
        """Create default templates if they don't exist"""
        
        # Auto-reply template
        auto_reply_path = os.path.join(self.templates_dir, "auto_reply.html")
        if not os.path.exists(auto_reply_path):
            self._create_auto_reply_template(auto_reply_path)
        
        # Notification template
        notification_path = os.path.join(self.templates_dir, "notification.html")
        if not os.path.exists(notification_path):
            self._create_notification_template(notification_path)
    
    def _create_auto_reply_template(self, file_path: str):
        """Create default auto-reply template"""
        template_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Réponse automatique</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #2c3e50;">Merci pour votre message</h2>
        
        <p>Bonjour,</p>
        
        <p>J'ai bien reçu votre email concernant <strong>"{{ original_subject }}"</strong>.</p>
        
        <p>Je vous remercie de m'avoir contacté. Je traiterai votre demande dans les plus brefs délais.</p>
        
        <p>Si votre demande est urgente, n'hésitez pas à me contacter par téléphone.</p>
        
        <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
        
        <p style="font-size: 12px; color: #666;">
            <em>Ce message a été envoyé automatiquement par SmartMailer.</em><br>
            <em>Date de réception: {{ received_date }}</em>
        </p>
        
        <p>Cordialement,<br>
        {{ sender_name }}</p>
    </div>
</body>
</html>"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        logger.info(f"Created default auto-reply template: {file_path}")
    
    def _create_notification_template(self, file_path: str):
        """Create default notification template"""
        template_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Notification Email Important</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #e74c3c;">📧 Email Important Reçu</h2>
        
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>Expéditeur:</strong> {{ sender }}</p>
            <p><strong>Sujet:</strong> {{ subject }}</p>
            <p><strong>Date:</strong> {{ received_date }}</p>
        </div>
        
        <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #856404; margin-top: 0;">Aperçu du contenu:</h3>
            <p style="font-style: italic;">{{ content_preview }}</p>
        </div>
        
        <p style="color: #666; font-size: 12px;">
            <em>Notification envoyée par SmartMailer</em>
        </p>
    </div>
</body>
</html>"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        logger.info(f"Created default notification template: {file_path}")
    
    def render_auto_reply(self, original_email: Dict, sender_name: str = "SmartMailer") -> str:
        """Render auto-reply template"""
        try:
            template = self.env.get_template("auto_reply.html")
            
            context = {
                'original_subject': original_email.get('subject', ''),
                'received_date': original_email.get('date_received', '').strftime('%d/%m/%Y à %H:%M') if original_email.get('date_received') else '',
                'sender_name': sender_name
            }
            
            return template.render(**context)
            
        except Exception as e:
            logger.error(f"Error rendering auto-reply template: {e}")
            return self._get_fallback_auto_reply(original_email)
    
    def render_notification(self, email_data: Dict) -> str:
        """Render notification template"""
        try:
            template = self.env.get_template("notification.html")
            
            content = email_data.get('content', '')
            content_preview = content[:200] + "..." if len(content) > 200 else content
            
            context = {
                'sender': email_data.get('sender', ''),
                'subject': email_data.get('subject', ''),
                'received_date': email_data.get('date_received', '').strftime('%d/%m/%Y à %H:%M') if email_data.get('date_received') else '',
                'content_preview': content_preview
            }
            
            return template.render(**context)
            
        except Exception as e:
            logger.error(f"Error rendering notification template: {e}")
            return self._get_fallback_notification(email_data)
    
    def _get_fallback_auto_reply(self, original_email: Dict) -> str:
        """Fallback auto-reply if template fails"""
        return f"""
        <html>
        <body>
            <h2>Merci pour votre message</h2>
            <p>J'ai bien reçu votre email concernant "{original_email.get('subject', '')}".</p>
            <p>Je vous remercie de m'avoir contacté. Je traiterai votre demande dans les plus brefs délais.</p>
            <p>Cordialement,<br>SmartMailer</p>
        </body>
        </html>
        """
    
    def _get_fallback_notification(self, email_data: Dict) -> str:
        """Fallback notification if template fails"""
        return f"""
        <html>
        <body>
            <h2>📧 Email Important Reçu</h2>
            <p><strong>Expéditeur:</strong> {email_data.get('sender', '')}</p>
            <p><strong>Sujet:</strong> {email_data.get('subject', '')}</p>
            <p><strong>Date:</strong> {email_data.get('date_received', '')}</p>
        </body>
        </html>
        """
    
    def get_template_list(self) -> list:
        """Get list of available templates"""
        try:
            return [f for f in os.listdir(self.templates_dir) if f.endswith('.html')]
        except Exception as e:
            logger.error(f"Error getting template list: {e}")
            return []
    
    def create_custom_template(self, template_name: str, content: str) -> bool:
        """Create a custom template"""
        try:
            file_path = os.path.join(self.templates_dir, f"{template_name}.html")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Created custom template: {template_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating custom template: {e}")
            return False
