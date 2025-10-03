"""
Test script for SmartMailer connections
Tests all external services and configurations
"""

import sys
import os
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
from app.email_fetcher import EmailFetcher
from app.email_sender import EmailSender
from app.notifications import NotificationManager
from app.database import DatabaseManager
from loguru import logger


def test_configuration():
    """Test configuration loading"""
    print("🔧 Testing configuration...")
    
    try:
        print(f"✓ App name: {settings.app_name}")
        print(f"✓ App version: {settings.app_version}")
        print(f"✓ Email provider: {settings.email_provider}")
        print(f"✓ Check interval: {settings.check_interval_minutes} minutes")
        print(f"✓ Auto-reply enabled: {settings.auto_reply_enabled}")
        
        # Check required settings
        required_settings = [
            'email_address', 'email_password', 
            'telegram_bot_token', 'telegram_chat_id'
        ]
        
        missing_settings = []
        for setting in required_settings:
            if not getattr(settings, setting, None):
                missing_settings.append(setting)
        
        if missing_settings:
            print(f"⚠ Missing required settings: {', '.join(missing_settings)}")
            return False
        else:
            print("✓ All required settings present")
            return True
            
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False


def test_database():
    """Test database connection"""
    print("\n🗄️ Testing database...")
    
    try:
        db = DatabaseManager()
        stats = db.get_processing_stats()
        print("✓ Database connection successful")
        print(f"✓ Total emails: {stats.get('total_emails', 0)}")
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False


def test_email_connection():
    """Test email IMAP connection"""
    print("\n📧 Testing email connection...")
    
    try:
        fetcher = EmailFetcher()
        if fetcher.connect():
            unread_count = fetcher.get_unread_count()
            print("✓ Email IMAP connection successful")
            print(f"✓ Unread emails: {unread_count}")
            fetcher.disconnect()
            return True
        else:
            print("✗ Email IMAP connection failed")
            return False
            
    except Exception as e:
        print(f"✗ Email connection error: {e}")
        return False


def test_smtp_connection():
    """Test SMTP connection"""
    print("\n📤 Testing SMTP connection...")
    
    try:
        sender = EmailSender()
        if sender.test_connection():
            print("✓ SMTP connection successful")
            return True
        else:
            print("✗ SMTP connection failed")
            return False
            
    except Exception as e:
        print(f"✗ SMTP error: {e}")
        return False


def test_telegram():
    """Test Telegram connection"""
    print("\n📱 Testing Telegram...")
    
    try:
        notifier = NotificationManager()
        results = notifier.test_all_notifications()
        
        if results.get('telegram_connection'):
            print("✓ Telegram bot connection successful")
            if results.get('telegram_message'):
                print("✓ Test message sent successfully")
                return True
            else:
                print("⚠ Bot connected but test message failed")
                return False
        else:
            print("✗ Telegram bot connection failed")
            return False
            
    except Exception as e:
        print(f"✗ Telegram error: {e}")
        return False


def test_classification():
    """Test email classification"""
    print("\n🤖 Testing email classification...")
    
    try:
        from app.email_classifier import EmailClassifier
        
        classifier = EmailClassifier()
        
        # Test important email
        important_email = {
            'subject': 'URGENT: Entretien demain matin',
            'sender': 'hr@company.com',
            'content': 'Nous avons un entretien urgent demain matin à 9h.'
        }
        
        classification = classifier.classify_email(important_email)
        print(f"✓ Important email classified as: {classification}")
        
        # Test normal email
        normal_email = {
            'subject': 'Newsletter hebdomadaire',
            'sender': 'newsletter@example.com',
            'content': 'Découvrez nos dernières offres promotionnelles.'
        }
        
        classification = classifier.classify_email(normal_email)
        print(f"✓ Normal email classified as: {classification}")
        
        return True
        
    except Exception as e:
        print(f"✗ Classification error: {e}")
        return False


def test_templates():
    """Test template rendering"""
    print("\n📝 Testing templates...")
    
    try:
        from app.templates import TemplateManager
        
        template_manager = TemplateManager()
        
        # Test auto-reply template
        test_email = {
            'subject': 'Test email',
            'date_received': '2024-01-01 10:00:00'
        }
        
        auto_reply = template_manager.render_auto_reply(test_email)
        if auto_reply and 'Merci pour votre message' in auto_reply:
            print("✓ Auto-reply template rendering successful")
        else:
            print("✗ Auto-reply template rendering failed")
            return False
        
        # Test notification template
        notification = template_manager.render_notification(test_email)
        if notification and 'Email Important Reçu' in notification:
            print("✓ Notification template rendering successful")
        else:
            print("✗ Notification template rendering failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Template error: {e}")
        return False


def main():
    """Main test function"""
    print("🧪 SmartMailer Connection Tests")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Database", test_database),
        ("Email IMAP", test_email_connection),
        ("SMTP", test_smtp_connection),
        ("Telegram", test_telegram),
        ("Classification", test_classification),
        ("Templates", test_templates)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! SmartMailer is ready to use.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check your configuration.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
