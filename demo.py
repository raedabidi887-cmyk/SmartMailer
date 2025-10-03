"""
Démonstration des fonctionnalités SmartMailer
"""

import sys
from pathlib import Path
from datetime import datetime

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

def demo_classification():
    """Démonstration de la classification d'emails"""
    print("🤖 DÉMONSTRATION - Classification d'emails")
    print("=" * 50)
    
    from app.email_classifier import EmailClassifier
    
    classifier = EmailClassifier()
    
    # Exemples d'emails
    emails = [
        {
            'subject': 'URGENT: Entretien demain matin à 9h',
            'sender': 'hr@company.com',
            'content': 'Bonjour, nous avons un entretien urgent demain matin à 9h. Merci de confirmer votre présence.'
        },
        {
            'subject': 'Newsletter hebdomadaire - Offres spéciales',
            'sender': 'newsletter@shop.com',
            'content': 'Découvrez nos dernières offres promotionnelles cette semaine. Réductions jusqu\'à 50%!'
        },
        {
            'subject': 'Projet client - Deadline approche',
            'sender': 'manager@company.com',
            'content': 'Le projet client doit être terminé avant vendredi. C\'est urgent!'
        },
        {
            'subject': 'Publicité - Nouveaux produits',
            'sender': 'marketing@store.com',
            'content': 'Découvrez nos nouveaux produits en promotion. Offre limitée!'
        }
    ]
    
    for i, email in enumerate(emails, 1):
        classification = classifier.classify_email(email)
        emoji = "🚨" if classification == "important" else "📧"
        
        print(f"\n{emoji} Email {i}: {classification.upper()}")
        print(f"   Sujet: {email['subject']}")
        print(f"   Expéditeur: {email['sender']}")
        print(f"   Classification: {classification}")
    
    print("\n" + "=" * 50)

def demo_templates():
    """Démonstration des templates"""
    print("📝 DÉMONSTRATION - Templates de réponse")
    print("=" * 50)
    
    from app.templates import TemplateManager
    
    template_manager = TemplateManager()
    
    # Email exemple
    email_data = {
        'subject': 'Demande d\'information',
        'sender': 'client@example.com',
        'date_received': datetime.now(),
        'content': 'Bonjour, j\'aimerais avoir plus d\'informations sur vos services.'
    }
    
    # Template de réponse automatique
    print("\n📤 Template de réponse automatique:")
    print("-" * 30)
    auto_reply = template_manager.render_auto_reply(email_data)
    print(auto_reply[:200] + "..." if len(auto_reply) > 200 else auto_reply)
    
    # Template de notification
    print("\n📱 Template de notification:")
    print("-" * 30)
    notification = template_manager.render_notification(email_data)
    print(notification[:200] + "..." if len(notification) > 200 else notification)
    
    print("\n" + "=" * 50)

def demo_database():
    """Démonstration de la base de données"""
    print("🗄️ DÉMONSTRATION - Base de données")
    print("=" * 50)
    
    from app.database import DatabaseManager
    from app.email_classifier import EmailClassifier
    
    db = DatabaseManager()
    classifier = EmailClassifier()
    
    # Simuler quelques emails
    sample_emails = [
        {
            'uid': 'demo_001',
            'subject': 'URGENT: Réunion importante',
            'sender': 'boss@company.com',
            'recipient': 'user@company.com',
            'date_received': datetime.now(),
            'content': 'Réunion urgente demain matin à 8h.'
        },
        {
            'uid': 'demo_002',
            'subject': 'Newsletter mensuelle',
            'sender': 'newsletter@blog.com',
            'recipient': 'user@company.com',
            'date_received': datetime.now(),
            'content': 'Découvrez nos articles du mois.'
        }
    ]
    
    print("💾 Sauvegarde d'emails simulés...")
    
    for email_data in sample_emails:
        # Classifier l'email
        classification = classifier.classify_email(email_data)
        
        # Sauvegarder en base
        email_record = db.save_email(email_data, classification)
        
        if email_record:
            print(f"✓ Email sauvegardé: {email_data['subject'][:30]}... ({classification})")
        else:
            print(f"✗ Erreur sauvegarde: {email_data['subject'][:30]}...")
    
    # Afficher les statistiques
    print("\n📊 Statistiques de la base de données:")
    stats = db.get_processing_stats()
    print(f"   Total emails: {stats.get('total_emails', 0)}")
    print(f"   Emails normaux: {stats.get('normal_emails', 0)}")
    print(f"   Emails importants: {stats.get('important_emails', 0)}")
    
    # Afficher les emails récents
    print("\n📋 Emails récents:")
    recent_emails = db.get_recent_emails(5)
    for email in recent_emails:
        print(f"   - {email.subject[:40]}... ({email.classification})")
    
    db.close()
    print("\n" + "=" * 50)

def demo_api_endpoints():
    """Démonstration des endpoints API"""
    print("🌐 DÉMONSTRATION - API Endpoints")
    print("=" * 50)
    
    print("📡 Endpoints disponibles:")
    print("   GET  /                    - Informations générales")
    print("   GET  /health              - État de santé")
    print("   GET  /emails              - Liste des emails")
    print("   GET  /emails/{id}         - Détails d'un email")
    print("   GET  /stats               - Statistiques")
    print("   GET  /logs                - Logs de traitement")
    print("   POST /test/telegram       - Test Telegram")
    print("   POST /emails/{id}/resend-notification - Renvoyer notification")
    print("   POST /maintenance/cleanup - Nettoyer anciens emails")
    
    print("\n🔗 URLs d'accès:")
    print("   API Documentation: http://localhost:8000/docs")
    print("   Health Check:      http://localhost:8000/health")
    print("   Statistiques:      http://localhost:8000/stats")
    print("   Liste emails:      http://localhost:8000/emails")
    
    print("\n" + "=" * 50)

def demo_workflow():
    """Démonstration du workflow complet"""
    print("🔄 DÉMONSTRATION - Workflow complet")
    print("=" * 50)
    
    print("1️⃣  RÉCUPÉRATION")
    print("   📧 Connexion IMAP à Gmail/Outlook")
    print("   📥 Récupération des nouveaux emails")
    print("   🔍 Parsing et extraction du contenu")
    
    print("\n2️⃣  CLASSIFICATION")
    print("   🤖 Analyse du sujet, expéditeur, contenu")
    print("   📊 Application des règles de classification")
    print("   🏷️  Attribution du label (normal/important)")
    
    print("\n3️⃣  TRAITEMENT")
    print("   📤 Email NORMAL → Réponse automatique")
    print("   📱 Email IMPORTANT → Notification Telegram")
    print("   💾 Sauvegarde en base de données")
    
    print("\n4️⃣  MONITORING")
    print("   📈 Statistiques de traitement")
    print("   📝 Logs détaillés")
    print("   🌐 API REST pour consultation")
    
    print("\n" + "=" * 50)

def main():
    """Fonction principale de démonstration"""
    print("🎬 DÉMONSTRATION SMARTMAILER")
    print("=" * 60)
    print("Application intelligente de gestion d'emails")
    print("Version 1.0.0")
    print("=" * 60)
    
    try:
        # Démonstrations
        demo_classification()
        demo_templates()
        demo_database()
        demo_api_endpoints()
        demo_workflow()
        
        print("\n🎉 DÉMONSTRATION TERMINÉE")
        print("=" * 60)
        print("SmartMailer est prêt à automatiser votre gestion d'emails!")
        print("\n📚 Prochaines étapes:")
        print("1. Configurez votre fichier .env (voir CONFIGURATION.md)")
        print("2. Testez les connexions: python scripts/test_connections.py")
        print("3. Lancez l'application: python main.py both")
        print("4. Consultez l'API: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la démonstration: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
