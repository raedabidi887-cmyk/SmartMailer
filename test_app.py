"""
Test simple de l'application SmartMailer
"""

import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test que tous les modules s'importent correctement"""
    print("🧪 Testing imports...")
    
    try:
        from app.config import settings
        print("✓ Config imported")
        
        from app.models import Email, ProcessingLog, create_tables
        print("✓ Models imported")
        
        from app.email_classifier import EmailClassifier
        print("✓ Email classifier imported")
        
        from app.templates import TemplateManager
        print("✓ Templates imported")
        
        from app.notifications import NotificationManager
        print("✓ Notifications imported")
        
        from app.database import DatabaseManager
        print("✓ Database imported")
        
        return True
        
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_classification():
    """Test de classification"""
    print("\n🤖 Testing classification...")
    
    try:
        from app.email_classifier import EmailClassifier
        
        classifier = EmailClassifier()
        
        # Test email important
        important_email = {
            'subject': 'URGENT: Entretien demain matin',
            'sender': 'hr@company.com',
            'content': 'Nous avons un entretien urgent demain matin à 9h.'
        }
        
        result = classifier.classify_email(important_email)
        print(f"✓ Important email classified as: {result}")
        
        # Test email normal
        normal_email = {
            'subject': 'Newsletter hebdomadaire',
            'sender': 'newsletter@example.com',
            'content': 'Découvrez nos dernières offres promotionnelles.'
        }
        
        result = classifier.classify_email(normal_email)
        print(f"✓ Normal email classified as: {result}")
        
        return True
        
    except Exception as e:
        print(f"✗ Classification error: {e}")
        return False

def test_templates():
    """Test des templates"""
    print("\n📝 Testing templates...")
    
    try:
        from app.templates import TemplateManager
        
        template_manager = TemplateManager()
        
        # Test auto-reply
        test_email = {
            'subject': 'Test email',
            'date_received': '2024-01-01 10:00:00'
        }
        
        auto_reply = template_manager.render_auto_reply(test_email)
        if 'Merci pour votre message' in auto_reply:
            print("✓ Auto-reply template works")
        else:
            print("✗ Auto-reply template failed")
            return False
        
        # Test notification
        notification = template_manager.render_notification(test_email)
        if 'Email Important Reçu' in notification:
            print("✓ Notification template works")
        else:
            print("✗ Notification template failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Template error: {e}")
        return False

def test_database():
    """Test de la base de données"""
    print("\n🗄️ Testing database...")
    
    try:
        from app.database import DatabaseManager
        
        db = DatabaseManager()
        stats = db.get_processing_stats()
        print(f"✓ Database connection works - Total emails: {stats.get('total_emails', 0)}")
        db.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 SmartMailer Application Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Classification", test_classification),
        ("Templates", test_templates),
        ("Database", test_database)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! SmartMailer is ready to use.")
        print("\n📝 Next steps:")
        print("1. Configure your .env file (see CONFIGURATION.md)")
        print("2. Run: python scripts/test_connections.py")
        print("3. Start: python main.py both")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
