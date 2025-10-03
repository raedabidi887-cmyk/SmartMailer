# Guide de Configuration SmartMailer

## 🚀 Configuration Rapide

L'application SmartMailer est maintenant installée et fonctionnelle ! Il ne reste plus qu'à configurer vos credentials.

## 📧 Configuration Email

### Pour Gmail

1. **Activer l'authentification à 2 facteurs**
   - Aller dans [Compte Google](https://myaccount.google.com/)
   - Sécurité → Authentification à 2 étapes
   - Activer si ce n'est pas déjà fait

2. **Générer un mot de passe d'application**
   - Aller dans [Compte Google](https://myaccount.google.com/)
   - Sécurité → Mots de passe des applications
   - Sélectionner "Mail" et votre appareil
   - Copier le mot de passe généré (16 caractères)

3. **Configurer le fichier .env**
```bash
EMAIL_PROVIDER=gmail
EMAIL_ADDRESS=votre-email@gmail.com
EMAIL_PASSWORD=votre-mot-de-passe-application-16-caracteres
EMAIL_IMAP_SERVER=imap.gmail.com
EMAIL_IMAP_PORT=993
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
```

### Pour Outlook

1. **Activer l'authentification à 2 facteurs**
   - Aller dans [Compte Microsoft](https://account.microsoft.com/)
   - Sécurité → Options de sécurité avancées
   - Activer l'authentification à 2 facteurs

2. **Générer un mot de passe d'application**
   - Aller dans [Compte Microsoft](https://account.microsoft.com/)
   - Sécurité → Mots de passe des applications
   - Créer un nouveau mot de passe pour "Mail"
   - Copier le mot de passe généré

3. **Configurer le fichier .env**
```bash
EMAIL_PROVIDER=outlook
EMAIL_ADDRESS=votre-email@outlook.com
EMAIL_PASSWORD=votre-mot-de-passe-application
EMAIL_IMAP_SERVER=outlook.office365.com
EMAIL_IMAP_PORT=993
EMAIL_SMTP_SERVER=smtp-mail.outlook.com
EMAIL_SMTP_PORT=587
```

## 📱 Configuration Telegram

### 1. Créer un Bot Telegram

1. **Ouvrir Telegram** et chercher `@BotFather`
2. **Envoyer** `/newbot`
3. **Donner un nom** à votre bot (ex: "SmartMailer Bot")
4. **Donner un username** (ex: "smartmailer_bot")
5. **Copier le token** fourni (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Obtenir votre Chat ID

1. **Envoyer un message** à votre bot
2. **Ouvrir** `https://api.telegram.org/bot<VOTRE_TOKEN>/getUpdates`
3. **Chercher** `"chat":{"id":123456789}` dans la réponse
4. **Copier** le numéro (ex: `123456789`)

### 3. Configurer le fichier .env
```bash
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
```

## ⚙️ Configuration Complète

Voici un exemple de fichier `.env` complet :

```bash
# Email Configuration
EMAIL_PROVIDER=gmail
EMAIL_ADDRESS=votre-email@gmail.com
EMAIL_PASSWORD=votre-mot-de-passe-application
EMAIL_IMAP_SERVER=imap.gmail.com
EMAIL_IMAP_PORT=993
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587

# Telegram Configuration
TELEGRAM_BOT_TOKEN=votre-bot-token
TELEGRAM_CHAT_ID=votre-chat-id

# Database Configuration
DATABASE_URL=sqlite:///./smartmailer.db

# Application Configuration
APP_NAME=SmartMailer
APP_VERSION=1.0.0
DEBUG=True
LOG_LEVEL=INFO

# Processing Configuration
CHECK_INTERVAL_MINUTES=5
MAX_EMAILS_PER_BATCH=50
PROCESSING_TIMEOUT_SECONDS=300

# Classification Rules
IMPORTANT_KEYWORDS=urgent,important,entretien,rh,recrutement,deadline,asap
IMPORTANT_SENDERS=hr@company.com,recruitment@company.com
NORMAL_KEYWORDS=newsletter,marketing,promotion,publicité

# Response Templates
AUTO_REPLY_ENABLED=True
AUTO_REPLY_SUBJECT=Re: {original_subject}
AUTO_REPLY_TEMPLATE=auto_reply_template.html
```

## 🧪 Tester la Configuration

Une fois votre fichier `.env` configuré :

```bash
# Tester toutes les connexions
python scripts/test_connections.py

# Si tout est OK, lancer l'application
python main.py both
```

## 🚀 Lancer l'Application

### Mode Complet (Recommandé)
```bash
python main.py both
```
- Lance le worker (traitement emails) + API (monitoring)
- Accessible sur http://localhost:8000

### Mode Worker Seul
```bash
python main.py worker
```
- Traitement des emails uniquement

### Mode API Seul
```bash
python main.py api
```
- API de monitoring uniquement

## 📊 Monitoring

Une fois lancée, l'application est accessible via :

- **API Documentation** : http://localhost:8000/docs
- **Health Check** : http://localhost:8000/health
- **Statistiques** : http://localhost:8000/stats
- **Liste des emails** : http://localhost:8000/emails

## 🔧 Personnalisation

### Règles de Classification

Modifiez les mots-clés dans `.env` :

```bash
# Emails importants
IMPORTANT_KEYWORDS=urgent,important,entretien,rh,recrutement,deadline,asap,client,projet

# Emails normaux  
NORMAL_KEYWORDS=newsletter,marketing,promotion,publicité,spam,unsubscribe
```

### Templates de Réponse

Modifiez les fichiers dans `templates/` :
- `auto_reply.html` - Réponse automatique
- `notification.html` - Template de notification

### Fréquence de Vérification

```bash
# Vérifier les emails toutes les 2 minutes
CHECK_INTERVAL_MINUTES=2
```

## 🐳 Déploiement Docker

```bash
# Avec Docker Compose
docker-compose up -d

# Vérifier les logs
docker-compose logs -f smartmailer
```

## ❓ Problèmes Courants

### Erreur d'authentification Gmail
- Vérifier que l'authentification à 2 facteurs est activée
- Utiliser un mot de passe d'application, pas votre mot de passe normal
- Vérifier que l'accès "Moins sécurisé" n'est pas activé

### Erreur Telegram
- Vérifier que le bot token est correct
- Vérifier que le chat ID est correct
- Envoyer un message au bot avant de lancer l'application

### Erreur de connexion
- Vérifier votre connexion internet
- Vérifier que les ports 993 (IMAP) et 587 (SMTP) ne sont pas bloqués
- Vérifier les paramètres de votre pare-feu

## 📞 Support

- **Documentation** : README.md
- **Architecture** : architecture.md
- **Logs** : `logs/smartmailer.log`

---

**SmartMailer est maintenant prêt à automatiser votre gestion d'emails !** 🎉
