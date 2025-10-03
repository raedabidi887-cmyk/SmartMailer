"""
Configuration management for SmartMailer
"""

import os
from typing import List, Optional
from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Email Configuration
    email_provider: str = "gmail"
    email_address: str
    email_password: str
    email_imap_server: str = "imap.gmail.com"
    email_imap_port: int = 993
    email_smtp_server: str = "smtp.gmail.com"
    email_smtp_port: int = 587
    
    # Telegram Configuration
    telegram_bot_token: str
    telegram_chat_id: str
    
    # Database Configuration
    database_url: str = "sqlite:///./smartmailer.db"
    
    # Application Configuration
    app_name: str = "SmartMailer"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"
    
    # Processing Configuration
    check_interval_minutes: int = 5
    max_emails_per_batch: int = 50
    processing_timeout_seconds: int = 300
    
    # Classification Rules
    important_keywords: str = "urgent,important,entretien,rh,recrutement,deadline,asap"
    important_senders: str = ""
    normal_keywords: str = "newsletter,marketing,promotion,publicité"
    
    # Response Templates
    auto_reply_enabled: bool = True
    auto_reply_subject: str = "Re: {original_subject}"
    auto_reply_template: str = "auto_reply_template.html"
    
    @validator('important_keywords', 'important_senders', 'normal_keywords')
    def parse_comma_separated(cls, v):
        """Parse comma-separated strings into lists"""
        if isinstance(v, str):
            return [item.strip().lower() for item in v.split(',') if item.strip()]
        return v
    
    @property
    def important_keywords_list(self) -> List[str]:
        """Get important keywords as list"""
        return self.important_keywords if isinstance(self.important_keywords, list) else []
    
    @property
    def important_senders_list(self) -> List[str]:
        """Get important senders as list"""
        return self.important_senders if isinstance(self.important_senders, list) else []
    
    @property
    def normal_keywords_list(self) -> List[str]:
        """Get normal keywords as list"""
        return self.normal_keywords if isinstance(self.normal_keywords, list) else []
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
