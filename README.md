# KodiBOT API 🤖

Assistant WhatsApp intelligent pour les services gouvernementaux de la République Démocratique du Congo.

## 🌟 Aperçu

KodiBOT est un assistant conversationnel intelligent conçu pour faciliter l'accès aux services gouvernementaux de la RDC via WhatsApp. Cette API gère les conversations, les requêtes utilisateurs et l'intégration avec les systèmes gouvernementaux.

## 🚀 Fonctionnalités

- **Chat Intelligent**: Conversations naturelles avec les citoyens
- **Intégration WhatsApp**: Interface native WhatsApp
- **Services Gouvernementaux**: Accès aux informations fiscales, foncières, etc.
- **Base de Données**: Stockage des conversations et données utilisateurs
- **API RESTful**: Endpoints pour intégration avec d'autres systèmes

## 🛠️ Technologies

- **Framework**: FastAPI / Flask (Python)
- **Base de Données**: SQLite
- **IA**: OpenAI GPT / Modèles de langage
- **API**: RESTful API
- **Logging**: Système de logs personnalisé

## 📦 Installation & Développement

### Prérequis
- Python 3.8+
- pip ou pipenv

### Installation
```bash
# Cloner le repository
cd kodibot

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Démarrer l'application
python main.py
```

### Configuration
Créer un fichier `.env` avec les variables nécessaires :
```env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=sqlite:///kodibot.db
DEBUG=True
```

## 🏗️ Structure du Projet

```
kodibot/
├── main.py                 # Point d'entrée de l'application
├── requirements.txt        # Dépendances Python
├── kodibot.db             # Base de données SQLite
├── src/                   # Code source principal
│   ├── __init__.py
│   ├── kodibot.py         # Logique principale du bot
│   ├── database.py        # Gestion de la base de données
│   ├── models.py          # Modèles de données
│   ├── services.py        # Services métier
│   ├── openai_client.py   # Client OpenAI
│   ├── prompts.py         # Templates de prompts
│   ├── logger.py          # Système de logging
│   └── test_data.py       # Données de test
├── scripts/               # Scripts utilitaires
│   └── seed_data.py       # Initialisation des données
└── tests/                 # Tests unitaires
    ├── config.py
    ├── test_chat.py
    ├── test_integration.py
    └── test_openai.py
```

## 🔧 API Endpoints

### Chat
- `POST /chat`: Envoyer un message au bot
- `GET /chat/history`: Historique des conversations

### Services Gouvernementaux
- `GET /services/tax`: Informations fiscales
- `GET /services/land`: Informations foncières
- `GET /services/procedures`: Procédures administratives

### Gestion
- `GET /health`: Vérification de l'état de l'API
- `GET /logs`: Logs de l'application

## 📊 Base de Données

### Modèles Principaux
- **Conversations**: Historique des échanges
- **Users**: Informations des utilisateurs
- **Services**: Catalogue des services disponibles
- **Logs**: Journal des activités

## 🧪 Tests

```bash
# Exécuter tous les tests
python -m pytest tests/

# Test spécifique
python -m pytest tests/test_chat.py

# Tests avec couverture
python -m pytest --cov=src tests/
```

## 🚀 Déploiement

### Production
```bash
# Configuration production
export ENVIRONMENT=production
export DEBUG=False

# Démarrer l'application
python main.py
```

### Docker (optionnel)
```bash
# Build de l'image
docker build -t kodibot-api .

# Lancer le conteneur
docker run -p 8000:8000 kodibot-api
```

## 🔍 Monitoring & Logs

### Logs Disponibles
- **Chat Logs**: Conversations utilisateurs
- **Error Logs**: Erreurs système
- **Performance Logs**: Métriques de performance

### Monitoring
- Vérification de santé via `/health`
- Logs centralisés dans `src/logger.py`

## 🤝 Contribution

### Guidelines de Développement
1. **Code Style**: Suivre PEP 8
2. **Tests**: Ajouter des tests pour nouvelles fonctionnalités
3. **Documentation**: Documenter les nouvelles API
4. **Commits**: Messages descriptifs en français

## 📞 Support & Contact

### Équipe de Développement
- **Backend**: Équipe Kodinet
- **IA/ML**: Spécialistes en traitement du langage naturel

### Liens Utiles
- 🌐 **Kodinet**: [kodinet.cd](https://kodinet.cd)
- 📧 **Support**: support@kodinet.cd
- 🐛 **Issues**: GitHub Issues

## 📄 Licence

Ce projet est développé pour les services gouvernementaux de la République Démocratique du Congo sous licence propriétaire Kodinet.

---

**KodiBOT API - Assistant numérique pour les services citoyens RDC** 🇨🇩