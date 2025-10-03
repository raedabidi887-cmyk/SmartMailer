# Architecture SmartMailer

## Vue d'ensemble

SmartMailer est une application intelligente de gestion d'emails qui automatise la classification, le traitement et les réponses aux emails entrants.

## Architecture générale

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Gmail/Outlook │    │   Telegram Bot  │    │   Base SQLite   │
│   (IMAP/SMTP)   │    │   (Notifications)│    │   (Stockage)    │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          │                      │                      │
          ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SmartMailer Core                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Fetcher   │  │ Classifier  │  │   Sender    │            │
│  │  (IMAP)     │  │ (Règles)    │  │  (SMTP)     │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ Templates   │  │ Notifier    │  │  Database   │            │
│  │ (Jinja2)    │  │(Telegram)   │  │ (SQLite)    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestration Layer                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Worker    │  │     API     │  │  Scheduler  │            │
│  │ (Principal) │  │ (FastAPI)   │  │ (Schedule)  │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

## Flux de données

### 1. Récupération des emails
```
Gmail/Outlook → EmailFetcher → Email Data
```

### 2. Classification
```
Email Data → EmailClassifier → Classification (normal/important)
```

### 3. Traitement selon classification

#### Email Normal
```
Email Data → TemplateManager → EmailSender → SMTP → Réponse auto
```

#### Email Important
```
Email Data → NotificationManager → Telegram API → Notification
```

### 4. Stockage
```
Email Data + Classification → DatabaseManager → SQLite
```

## Modules détaillés

### 1. EmailFetcher (`app/email_fetcher.py`)
- **Responsabilité**: Récupération des emails via IMAP
- **Technologies**: IMAPClient, SSL
- **Fonctionnalités**:
  - Connexion sécurisée IMAP
  - Récupération emails récents
  - Parsing des emails
  - Extraction contenu texte

### 2. EmailClassifier (`app/email_classifier.py`)
- **Responsabilité**: Classification des emails
- **Algorithme**: Règles basées sur mots-clés et patterns
- **Classifications**:
  - **Important**: urgent, entretien, rh, deadline
  - **Normal**: newsletter, marketing, promotion

### 3. EmailSender (`app/email_sender.py`)
- **Responsabilité**: Envoi réponses automatiques
- **Technologies**: SMTP, SSL
- **Fonctionnalités**:
  - Connexion SMTP sécurisée
  - Envoi réponses HTML
  - Gestion erreurs SMTP

### 4. TemplateManager (`app/templates.py`)
- **Responsabilité**: Gestion templates de réponse
- **Technologies**: Jinja2
- **Templates**:
  - Auto-reply (emails normaux)
  - Notification (emails importants)

### 5. NotificationManager (`app/notifications.py`)
- **Responsabilité**: Notifications Telegram
- **Technologies**: Telegram Bot API
- **Fonctionnalités**:
  - Envoi notifications temps réel
  - Formatage messages HTML
  - Gestion erreurs API

### 6. DatabaseManager (`app/database.py`)
- **Responsabilité**: Persistance des données
- **Technologies**: SQLAlchemy, SQLite
- **Entités**:
  - Email (données emails)
  - ProcessingLog (logs traitement)

### 7. Worker (`app/worker.py`)
- **Responsabilité**: Orchestration principale
- **Technologies**: Schedule, Loguru
- **Fonctionnalités**:
  - Boucle de traitement périodique
  - Gestion des erreurs
  - Monitoring des performances

### 8. API (`app/api.py`)
- **Responsabilité**: Interface REST
- **Technologies**: FastAPI, Pydantic
- **Endpoints**:
  - `/health` - État de santé
  - `/emails` - Liste emails
  - `/stats` - Statistiques
  - `/test/telegram` - Test notifications

## Configuration

### Variables d'environnement
```bash
# Email
EMAIL_PROVIDER=gmail
EMAIL_ADDRESS=user@gmail.com
EMAIL_PASSWORD=app-password

# Telegram
TELEGRAM_BOT_TOKEN=bot-token
TELEGRAM_CHAT_ID=chat-id

# Application
CHECK_INTERVAL_MINUTES=5
AUTO_REPLY_ENABLED=True
```

### Règles de classification
```python
IMPORTANT_KEYWORDS = [
    'urgent', 'important', 'entretien', 
    'rh', 'recrutement', 'deadline', 'asap'
]

NORMAL_KEYWORDS = [
    'newsletter', 'marketing', 
    'promotion', 'publicité'
]
```

## Sécurité

### Authentification
- **Gmail**: Mot de passe d'application (2FA requis)
- **Outlook**: Mot de passe d'application
- **Telegram**: Bot token

### Connexions
- **IMAP/SMTP**: SSL/TLS obligatoire
- **API**: HTTPS en production
- **Base de données**: Fichier local SQLite

### Secrets
- Variables d'environnement pour tous les secrets
- Fichier `.env` exclu du versioning
- Pas de hardcoding de credentials

## Performance

### Métriques cibles
- **Latence notification**: < 1 minute
- **Temps traitement email**: < 5 secondes
- **Taux erreur**: < 5%
- **Classification correcte**: > 90%

### Optimisations
- Traitement par batch (50 emails max)
- Connexions réutilisées
- Logs structurés
- Monitoring intégré

## Monitoring

### Logs
- **Format**: JSON structuré
- **Rotation**: Quotidienne
- **Rétention**: 30 jours
- **Niveaux**: DEBUG, INFO, WARNING, ERROR

### Métriques
- Emails traités par heure
- Taux de classification
- Latence des notifications
- Erreurs par type

### Alertes
- Échec connexion email
- Échec notifications Telegram
- Taux d'erreur élevé
- Performance dégradée

## Déploiement

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py", "both"]
```

### Docker Compose
```yaml
services:
  smartmailer:
    build: .
    ports:
      - "8000:8000"
    environment:
      - EMAIL_ADDRESS=${EMAIL_ADDRESS}
      - EMAIL_PASSWORD=${EMAIL_PASSWORD}
    volumes:
      - ./logs:/app/logs
      - ./smartmailer.db:/app/smartmailer.db
```

## Évolutivité (V2)

### Base de données
- **PostgreSQL** pour production
- **Migrations** avec Alembic
- **Indexation** optimisée

### Traitement
- **Celery** pour tâches asynchrones
- **Redis** pour cache et queue
- **Workers** multiples

### Interface
- **React/Vue** frontend
- **WebSocket** pour temps réel
- **Dashboard** analytics

### IA/ML
- **scikit-learn** pour classification
- **HuggingFace** pour NLP
- **Apprentissage** continu

## Maintenance

### Nettoyage
- Suppression emails anciens (> 30 jours)
- Rotation logs
- Optimisation base de données

### Sauvegarde
- Base de données SQLite
- Configuration .env
- Templates personnalisés

### Mise à jour
- Tests automatisés
- Déploiement sans interruption
- Rollback automatique
