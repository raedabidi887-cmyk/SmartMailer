"""
Email classification module for SmartMailer
Classifies emails as 'normal' or 'important' based on rules
"""

import re
from typing import Dict, List
from loguru import logger
from app.config import settings


class EmailClassifier:
    """Email classifier based on rules and keywords"""
    
    def __init__(self):
        self.important_keywords = settings.important_keywords_list
        self.important_senders = settings.important_senders_list
        self.normal_keywords = settings.normal_keywords_list
    
    def classify_email(self, email_data: Dict) -> str:
        """
        Classify email as 'normal' or 'important'
        
        Args:
            email_data: Dictionary containing email information
            
        Returns:
            str: 'normal' or 'important'
        """
        try:
            subject = email_data.get('subject', '').lower()
            sender = email_data.get('sender', '').lower()
            content = email_data.get('content', '').lower()
            
            # Check if email is important
            if self._is_important_email(subject, sender, content):
                logger.info(f"Email classified as IMPORTANT: {subject[:50]}...")
                return 'important'
            
            # Check if email is normal
            elif self._is_normal_email(subject, sender, content):
                logger.info(f"Email classified as NORMAL: {subject[:50]}...")
                return 'normal'
            
            # Default classification based on sender domain
            else:
                classification = self._classify_by_sender_domain(sender)
                logger.info(f"Email classified as {classification.upper()} (by domain): {subject[:50]}...")
                return classification
                
        except Exception as e:
            logger.error(f"Error classifying email: {e}")
            return 'normal'  # Default to normal on error
    
    def _is_important_email(self, subject: str, sender: str, content: str) -> bool:
        """Check if email should be classified as important"""
        
        # Check important senders
        for important_sender in self.important_senders:
            if important_sender in sender:
                logger.debug(f"Important sender match: {important_sender}")
                return True
        
        # Check important keywords in subject
        for keyword in self.important_keywords:
            if keyword in subject:
                logger.debug(f"Important keyword in subject: {keyword}")
                return True
        
        # Check important keywords in content (first 500 chars)
        content_preview = content[:500]
        for keyword in self.important_keywords:
            if keyword in content_preview:
                logger.debug(f"Important keyword in content: {keyword}")
                return True
        
        # Check for urgent patterns
        urgent_patterns = [
            r'\b(urgent|asap|as soon as possible)\b',
            r'\b(deadline|due date)\b',
            r'\b(entretien|interview)\b',
            r'\b(recrutement|recruitment|hiring)\b',
            r'\b(rh|hr|human resources)\b'
        ]
        
        for pattern in urgent_patterns:
            if re.search(pattern, subject + ' ' + content_preview, re.IGNORECASE):
                logger.debug(f"Urgent pattern match: {pattern}")
                return True
        
        return False
    
    def _is_normal_email(self, subject: str, sender: str, content: str) -> bool:
        """Check if email should be classified as normal"""
        
        # Check normal keywords
        for keyword in self.normal_keywords:
            if keyword in subject or keyword in content[:200]:
                logger.debug(f"Normal keyword match: {keyword}")
                return True
        
        # Check for newsletter/marketing patterns
        normal_patterns = [
            r'\b(newsletter|news letter)\b',
            r'\b(marketing|promotion|promo)\b',
            r'\b(publicité|advertisement|ads)\b',
            r'\b(unsubscribe|désabonnement)\b',
            r'\b(offre|offer|deal)\b'
        ]
        
        for pattern in normal_patterns:
            if re.search(pattern, subject + ' ' + content[:200], re.IGNORECASE):
                logger.debug(f"Normal pattern match: {pattern}")
                return True
        
        return False
    
    def _classify_by_sender_domain(self, sender: str) -> str:
        """Classify email based on sender domain"""
        try:
            # Extract domain from sender
            if '@' in sender:
                domain = sender.split('@')[1].lower()
                
                # Known important domains
                important_domains = [
                    'company.com',
                    'entreprise.fr',
                    'hr.com',
                    'recruitment.com'
                ]
                
                # Known normal domains
                normal_domains = [
                    'newsletter.com',
                    'marketing.com',
                    'promo.com',
                    'ads.com',
                    'noreply.com',
                    'no-reply.com'
                ]
                
                for imp_domain in important_domains:
                    if imp_domain in domain:
                        return 'important'
                
                for norm_domain in normal_domains:
                    if norm_domain in domain:
                        return 'normal'
            
            # Default classification
            return 'normal'
            
        except Exception as e:
            logger.error(f"Error classifying by domain: {e}")
            return 'normal'
    
    def get_classification_rules(self) -> Dict:
        """Get current classification rules"""
        return {
            'important_keywords': self.important_keywords,
            'important_senders': self.important_senders,
            'normal_keywords': self.normal_keywords
        }
    
    def update_classification_rules(self, rules: Dict):
        """Update classification rules"""
        try:
            if 'important_keywords' in rules:
                self.important_keywords = rules['important_keywords']
            if 'important_senders' in rules:
                self.important_senders = rules['important_senders']
            if 'normal_keywords' in rules:
                self.normal_keywords = rules['normal_keywords']
            
            logger.info("Classification rules updated")
            
        except Exception as e:
            logger.error(f"Error updating classification rules: {e}")
