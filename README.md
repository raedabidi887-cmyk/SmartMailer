# SmartMailer - Application intelligente de gestion d'emails

## 📧 Description

SmartMailer est une application intelligente qui automatise la gestion des emails en :
- **Classifiant automatiquement** les emails reçus (normaux vs importants)
- **Répondant automatiquement** aux emails normaux avec des templates personnalisés
- **Notifiant en temps réel** sur Telegram pour les emails importants
- **Stockant l'historique** de tous les emails traités

## 🚀 Fonctionnalités

### MVP (Version 1.0)
- ✅ Connexion Gmail/Outlook via IMAP/SMTP
- ✅ Classification automatique basée sur des règles
- ✅ Réponses automatiques avec templates Jinja2
- ✅ Notifications Telegram en temps réel
- ✅ Stockage SQLite avec historique complet
- ✅ API REST FastAPI pour monitoring
- ✅ Déploiement Docker

### V2 (Futur)
- 🔄 Interface Web React/Vue
- 🤖 Classification ML avec NLP
- 📊 Statistiques et analytics
- 🔐 OAuth2 pour Gmail/Outlook
- 🐘 PostgreSQL pour production
- ⚡ Celery/Redis pour traitement asynchrone

## 🛠️ Installation

### Prérequis
- Python 3.11+
- Docker & Docker Compose (optionnel)
- Compte Gmail/Outlook avec mot de passe d'application
- Bot Telegram (pour les notifications)

### Installation locale

1. **Cloner le projet**
```bash
git clone <repository-url>
cd smartmailer
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configuration**
```bash
cp env.example .env
# Éditer .env avec vos paramètres
```

4. **Créer la base de données**
```bash
python -c "from app.models import create_tables; create_tables()"
```

5. **Lancer l'application**
```bash
# Mode worker (traitement emails)
python main.py worker

# Mode API (monitoring)
python main.py api

# Mode complet (worker + API)
python main.py both
```

### Installation Docker

1. **Configuration**
```bash
cp env.example .env
# Éditer .env avec vos paramètres
```

2. **Lancer avec Docker Compose**
```bash
docker-compose up -d
```

## ⚙️ Configuration

### Variables d'environnement (.env)

```bash
# Configuration Email
EMAIL_PROVIDER=gmail  # ou outlook
EMAIL_ADDRESS=votre-email@gmail.com
EMAIL_PASSWORD=votre-mot-de-passe-application

# Configuration Telegram
TELEGRAM_BOT_TOKEN=votre-bot-token
TELEGRAM_CHAT_ID=votre-chat-id

# Configuration Application
CHECK_INTERVAL_MINUTES=5
AUTO_REPLY_ENABLED=True
```

### Configuration Gmail
1. Activer l'authentification à 2 facteurs
2. Générer un mot de passe d'application
3. Utiliser ce mot de passe dans `EMAIL_PASSWORD`

### Configuration Telegram
1. Créer un bot via @BotFather
2. Obtenir le token du bot
3. Obtenir votre chat ID via @userinfobot

## 📊 API Endpoints

### Monitoring
- `GET /` - Informations générales
- `GET /health` - État de santé de l'application
- `GET /stats` - Statistiques de traitement

### Emails
- `GET /emails` - Liste des emails traités
- `GET /emails/{id}` - Détails d'un email
- `POST /emails/{id}/resend-notification` - Renvoyer notification

### Maintenance
- `POST /test/telegram` - Tester Telegram
- `POST /maintenance/cleanup` - Nettoyer anciens emails

## 🔧 Architecture

```
[Gmail/Outlook] → [EmailFetcher] → [EmailClassifier] → [EmailSender/Notifier]
                                                      ↓
[Database] ← [API] ← [Worker] ← [Templates]
```

### Modules principaux
- **`email_fetcher.py`** - Récupération emails via IMAP
- **`email_classifier.py`** - Classification basée sur règles
- **`email_sender.py`** - Envoi réponses automatiques
- **`notifications.py`** - Notifications Telegram
- **`templates.py`** - Gestion templates Jinja2
- **`database.py`** - Opérations base de données
- **`worker.py`** - Orchestrateur principal
- **`api.py`** - API REST FastAPI

## 📝 Cas d'utilisation

### UC1: Email normal
1. Réception email newsletter
2. Classification: "normal"
3. Envoi réponse automatique
4. Stockage en base

### UC2: Email important
1. Réception email RH urgent
2. Classification: "important"
3. Notification Telegram
4. Stockage en base

### UC3: Monitoring
1. Consultation API `/emails`
2. Visualisation historique
3. Statistiques de traitement

## 🎯 Règles de classification

### Emails importants
- **Mots-clés**: urgent, important, entretien, rh, recrutement, deadline, asap
- **Expéditeurs**: hr@company.com, recruitment@company.com
- **Patterns**: emails contenant "urgent" ou "asap"

### Emails normaux
- **Mots-clés**: newsletter, marketing, promotion, publicité
- **Patterns**: emails de désabonnement, offres commerciales

## 📈 Monitoring

### Logs
- Fichiers dans `logs/smartmailer.log`
- Rotation quotidienne
- Rétention 30 jours

### Métriques
- Nombre d'emails traités
- Taux de classification correcte
- Latence des notifications
- Taux d'erreur SMTP/IMAP

## 🐳 Déploiement

### Docker
```bash
# Build
docker build -t smartmailer .

# Run
docker run -d --name smartmailer \
  -p 8000:8000 \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/logs:/app/logs \
  smartmailer
```

### Docker Compose
```bash
docker-compose up -d
```

## 🔒 Sécurité

- Mots de passe d'application pour Gmail/Outlook
- Variables d'environnement pour secrets
- Connexions SSL/TLS
- Validation des entrées API

## 🧪 Tests

```bash
# Tests unitaires
pytest tests/

# Test connexions
python -c "from app.worker import SmartMailerWorker; SmartMailerWorker()._test_connections()"

# Test API
curl http://localhost:8000/health
```

## 📋 Roadmap

### V1.1
- [ ] Interface Web basique
- [ ] Gestion multi-comptes
- [ ] Templates personnalisés

### V2.0
- [ ] Classification ML
- [ ] PostgreSQL
- [ ] OAuth2
- [ ] Celery/Redis

### V3.0
- [ ] Analytics avancées
- [ ] Intégrations tierces
- [ ] Mobile app

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature
3. Commit les changements
4. Push vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

MIT License - voir fichier LICENSE

## 🆘 Support

- Issues GitHub pour bugs
- Discussions pour questions
- Documentation complète dans `/docs`

---

**SmartMailer** - Automatisez votre gestion d'emails intelligemment ! 📧✨
