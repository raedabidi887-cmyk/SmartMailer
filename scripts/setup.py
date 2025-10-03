"""
Setup script for SmartMailer
Initializes the application and creates necessary files
"""

import os
import sys
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        "logs",
        "templates", 
        "scripts",
        "tests"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")

def create_env_file():
    """Create .env file from template"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists() and env_example.exists():
        env_file.write_text(env_example.read_text())
        print("✓ Created .env file from template")
    elif env_file.exists():
        print("✓ .env file already exists")
    else:
        print("⚠ env.example not found, please create .env manually")

def create_database():
    """Initialize database"""
    try:
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from app.models import create_tables
        create_tables()
        print("✓ Database initialized")
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")

def create_templates():
    """Create default templates"""
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    # Auto-reply template
    auto_reply_template = templates_dir / "auto_reply.html"
    if not auto_reply_template.exists():
        auto_reply_content = """<!DOCTYPE html>
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
        
        auto_reply_template.write_text(auto_reply_content, encoding='utf-8')
        print("✓ Created auto-reply template")
    
    # Notification template
    notification_template = templates_dir / "notification.html"
    if not notification_template.exists():
        notification_content = """<!DOCTYPE html>
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
        
        notification_template.write_text(notification_content, encoding='utf-8')
        print("✓ Created notification template")

def main():
    """Main setup function"""
    print("🚀 Setting up SmartMailer...")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Create templates
    create_templates()
    
    # Initialize database
    create_database()
    
    print("=" * 50)
    print("✅ Setup completed!")
    print("\n📝 Next steps:")
    print("1. Edit .env file with your configuration")
    print("2. Test connections: python -c \"from app.worker import SmartMailerWorker; SmartMailerWorker()._test_connections()\"")
    print("3. Start the application: python main.py both")
    print("\n📚 Documentation: README.md")

if __name__ == "__main__":
    main()
