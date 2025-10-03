# 🚀 SmartMailer - Guide de Démarrage Rapide

## ✅ Installation Terminée !

Votre application SmartMailer est maintenant **installée et fonctionnelle** ! 

## 🎯 Ce qui fonctionne déjà

- ✅ **Classification intelligente** des emails (normal/important)
- ✅ **Templates de réponse** automatique
- ✅ **Base de données** SQLite opérationnelle
- ✅ **API REST** FastAPI complète
- ✅ **Architecture modulaire** et extensible

## 🔧 Configuration Requise

Pour utiliser SmartMailer avec vos emails, configurez le fichier `.env` :

### 1. Configuration Email (Gmail)
```bash
EMAIL_ADDRESS=votre-email@gmail.com
EMAIL_PASSWORD=votre-mot-de-passe-application
```

### 2. Configuration Telegram
```bash
TELEGRAM_BOT_TOKEN=votre-bot-token
TELEGRAM_CHAT_ID=votre-chat-id
```

> 📖 **Guide détaillé** : Voir `CONFIGURATION.md`

## 🚀 Commandes Rapides

```bash
# Tester l'application
python test_app.py

# Voir la démonstration
python demo.py

# Tester les connexions
python scripts/test_connections.py

# Lancer l'application
python main.py both
```

## 📊 Accès à l'API

Une fois lancée, l'application est accessible sur :
- **Documentation API** : http://localhost:8000/docs
- **Health Check** : http://localhost:8000/health
- **Statistiques** : http://localhost:8000/stats

## 🎬 Démonstration

La démonstration montre :
- 🤖 **Classification** : 4 emails testés (2 normaux, 2 importants)
- 📝 **Templates** : Réponses automatiques et notifications
- 💾 **Base de données** : Sauvegarde et statistiques
- 🌐 **API** : Endpoints disponibles

## 📁 Structure du Projet

```
smartmailer/
├── app/                    # Code principal
│   ├── config.py          # Configuration
│   ├── models.py          # Modèles BDD
│   ├── email_fetcher.py   # Récupération emails
│   ├── email_classifier.py # Classification
│   ├── email_sender.py    # Envoi réponses
│   ├── templates.py       # Templates
│   ├── notifications.py   # Notifications
│   ├── database.py        # Base de données
│   ├── worker.py          # Orchestrateur
│   └── api.py            # API REST
├── scripts/               # Scripts utilitaires
├── templates/             # Templates HTML
├── logs/                  # Fichiers de logs
├── main.py               # Point d'entrée
├── demo.py               # Démonstration
├── test_app.py           # Tests
└── CONFIGURATION.md      # Guide configuration
```

## 🔄 Workflow Complet

1. **📧 Récupération** : IMAP Gmail/Outlook
2. **🤖 Classification** : Règles intelligentes
3. **📤 Traitement** : Réponses auto + Notifications
4. **💾 Stockage** : Base SQLite
5. **📊 Monitoring** : API REST

## 🎯 Cas d'Usage

### Email Normal (Newsletter)
- Classification : `normal`
- Action : Réponse automatique
- Template : "Merci pour votre message"

### Email Important (RH)
- Classification : `important`  
- Action : Notification Telegram
- Message : "🚨 Email Important Reçu"

## 🐳 Déploiement Docker

```bash
# Avec Docker Compose
docker-compose up -d

# Vérifier les logs
docker-compose logs -f smartmailer
```

## 📈 Métriques Cibles

- **Latence notification** : < 1 minute
- **Temps traitement** : < 5 secondes
- **Classification correcte** : > 90%
- **Taux d'erreur** : < 5%

## 🔧 Personnalisation

### Règles de Classification
Modifiez dans `.env` :
```bash
IMPORTANT_KEYWORDS=urgent,important,entretien,rh,recrutement,deadline,asap
NORMAL_KEYWORDS=newsletter,marketing,promotion,publicité
```

### Templates
Modifiez les fichiers dans `templates/` :
- `auto_reply.html` - Réponse automatique
- `notification.html` - Notification

### Fréquence
```bash
CHECK_INTERVAL_MINUTES=5  # Vérifier toutes les 5 minutes
```

## 🆘 Support

- **Documentation** : `README.md`
- **Architecture** : `architecture.md`
- **Configuration** : `CONFIGURATION.md`
- **Logs** : `logs/smartmailer.log`

## 🎉 Félicitations !

SmartMailer est prêt à automatiser votre gestion d'emails ! 

**Prochaine étape** : Configurez votre fichier `.env` et lancez l'application.

---

*SmartMailer v1.0.0 - Application intelligente de gestion d'emails* 📧✨
