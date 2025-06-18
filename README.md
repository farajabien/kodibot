# KodiBOT - Assistant WhatsApp Gouvernemental RDC 🇨🇩

KodiBOT est un assistant conversationnel intelligent conçu spécifiquement pour les services gouvernementaux de la République Démocratique du Congo. Il permet aux citoyens d'accéder facilement à leurs informations fiscales, cadastrales et procédurales via WhatsApp.

## 🚀 Architecture Modernisée

### **Systèmes Centralisés** ✅
- **`src/prompts.py`** - Gestion unifiée des prompts système
- **`src/openai_client.py`** - Client OpenAI centralisé avec gestion d'erreurs
- **`src/logger.py`** - Système de logging structuré
- **`src/test_data.py`** - 🆕 Données de test centralisées (zéro duplication)
- **`tests/config.py`** - Configuration centralisée des tests

### **Fonctionnalités Principales**
- 📊 **Fiscalité**: Consultation soldes, impôts, taxes DGI/DGRAD
- 🏠 **Parcelles**: Informations cadastrales et biens fonciers  
- 📋 **Procédures**: Démarches administratives (permis, documents)
- 👤 **Profil Citoyen**: Informations personnelles sécurisées
- 🔐 **Liaison Sécurisée**: Authentification via OTP

## 🛠️ Technologies

- **Backend**: FastAPI (Python 3.8+)
- **Base de Données**: SQLite avec SQLAlchemy ORM
- **IA**: OpenAI GPT-4 avec prompts optimisés DRC
- **Tests**: Pytest avec couverture complète
- **Logging**: Système structuré multi-niveaux

## 📦 Installation

```bash
# Cloner le repository
git clone <repository-url>
cd kodibot

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
export OPENAI_API_KEY="votre-clé-openai"
export LOG_LEVEL="INFO"  # Optional: DEBUG, INFO, WARNING, ERROR

# Initialiser la base de données
python scripts/seed_data.py

# Lancer le serveur
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 Configuration

### Variables d'Environnement
```bash
OPENAI_API_KEY=sk-...          # Obligatoire: Clé API OpenAI
LOG_LEVEL=INFO                 # Optionnel: Niveau de logging  
LOG_TO_FILE=false              # Optionnel: Activer logs fichier
DB_PATH=kodibot.db             # Optionnel: Chemin base de données
```

### Structure Base de Données
```sql
Citizens         # Informations citoyens
LinkedUsers      # Comptes liés WhatsApp  
TaxRecords       # Soldes fiscaux DGI/DGRAD
Properties       # Parcelles cadastrales
MessageLogs      # Historique conversations
```

## 🧪 Tests

```bash
# Lancer tous les tests
pytest tests/ -v

# Tests spécifiques
pytest tests/test_chat.py -v              # Tests chat flow
pytest tests/test_openai.py -v            # Tests OpenAI integration  
pytest tests/test_integration.py -v       # Tests end-to-end

# Tests avec couverture
pytest tests/ --cov=src --cov-report=html
```

### 📋 Données de Test Centralisées
- **`src/test_data.py`** - Source unique pour tous les données de test
- **Citoyens Test**: Jean Kabila (lié), Marie Tshisekedi (non-lié)
- **Données DRC**: Taxes, parcelles, procédures authentiques
- **Zéro Duplication**: Élimine hardcoding dans tests et seed scripts

## 📚 API Endpoints

### Chat Principal
```http
POST /chat
Content-Type: application/json

{
  "phone_number": "+243901234567",
  "message": "Quel est mon solde fiscal?"
}
```

### Liaison de Compte
```http
POST /link-account
{
  "phone_number": "+243901234567", 
  "citizen_id": "CIT123456789"
}
```

### Vérification OTP
```http
POST /verify-otp
{
  "phone_number": "+243901234567",
  "otp": "123456"
}
```

### Monitoring
```http
GET /                          # Health check
GET /test-users               # Utilisateurs de test
GET /analytics/popular-intents # Statistiques usage
```

## 🏗️ Structure du Projet (Optimisée)

```
kodibot/                     # 🎯 17 fichiers Python total
├── src/                     # 📁 10 fichiers - Code source optimisé
│   ├── __init__.py         # Package initialization (v2.0.0)
│   ├── database.py         # Modèles SQLAlchemy + ORM
│   ├── kodibot.py         # Logic conversationnelle DRC
│   ├── logger.py          # 🆕 Logging centralisé structuré
│   ├── model.py           # Interface OpenAI + intent extraction
│   ├── models.py          # ✅ Modèles Pydantic (maintenu)
│   ├── openai_client.py   # 🆕 Client OpenAI centralisé
│   ├── prompts.py         # 🆕 Prompts système DRC centralisés
│   ├── services.py        # Services métier + handlers
│   └── test_data.py       # 🆕 Données test centralisées (zéro duplication)
├── tests/                  # 📋 4 fichiers - Tests complets
│   ├── config.py          # 🆕 Configuration centralisée tests
│   ├── test_chat.py       # Tests chat flow principal
│   ├── test_integration.py # Tests end-to-end complets
│   └── test_openai.py     # Tests OpenAI + intent (consolidé)
├── scripts/               # 🔧 1 fichier - Utilitaires
│   └── seed_data.py       # Initialisation données DRC
├── main.py                # 🚀 Point d'entrée FastAPI (principal)
├── requirements.txt       # 📦 Dépendances Python optimisées
└── README.md             # 📖 Documentation complète
```

### 📊 Métriques Codebase
- **📁 Total fichiers Python**: 17 (optimisé)
- **🔄 Duplications**: 0 (éliminées complètement)
- **🎯 Fichiers core**: 10 (src/)
- **🧪 Fichiers tests**: 4 (consolidés)
- **📋 Couverture**: Tests complets E2E
- **🔧 Configuration**: Centralisée + données test unifiées

## 🔍 Exemples d'Utilisation

### Consultation Solde Fiscal
```
👤 Utilisateur: "Bonjour, quel est mon solde fiscal?"
🤖 KodiBOT: "Bonjour Jean Kabila, votre solde fiscal actuel est de 100 000 FC. Si vous avez d'autres questions, n'hésitez pas ! 😊"
```

### Informations Parcelles
```
👤 Utilisateur: "Mes parcelles"
🤖 KodiBOT: "Voici vos parcelles:
1. Parcelle 123, Gombe - 500m² - 85M FC
2. Parcelle 456, Limete - 800m² - 45M FC"
```

### Procédures Administratives
```
👤 Utilisateur: "Comment renouveler mon permis?"
🤖 KodiBOT: "Procédure de renouvellement:
1. Documents requis: ancien permis, certificat médical...
2. Coût: 25 000 FC
3. Durée: 2-3 semaines"
```

## 🛡️ Sécurité

- ✅ **Authentification OTP** pour liaison comptes
- ✅ **Validation stricte** numéros citoyens  
- ✅ **Logging sécurisé** sans données sensibles
- ✅ **Rate limiting** automatique OpenAI
- ✅ **Gestion d'erreurs** robuste

## 🔄 Améliorations Récentes

### Version 2.0.0 - Architecture Optimisée ✨
- ✅ **Centralisation Complete** prompts, OpenAI client, logging
- ✅ **Codebase Nettoyé** - Élimination doublons et fichiers obsolètes
- ✅ **Tests Streamlinés** - Configuration centralisée, suppression redondances
- ✅ **Architecture Moderne** - Séparation claire des responsabilités
- ✅ **Performance Optimisée** - 16 fichiers Python focalisés

### Corrections Architecturales ✅
- 🔧 **Imports Corrigés** - `test_openai.py`, `seed_data.py`
- 🔧 **Configuration Centralisée** - URLs tests, clients OpenAI
- 🔧 **Suppression Redondances** - `test_intent.py`, fichiers système
- 🔧 **Gestion d'Erreurs Unifiée** - Patterns cohérents
- 🔧 **Logging Structuré** - Système centralisé avec contexte

### Optimisations Finales 🎯
- 🧹 **Cleanup Système** - Suppression `.DS_Store`, fichiers cache
- 📁 **Structure Rationalisée** - 10 fichiers src/, 4 fichiers tests/
- 🔄 **Maintenabilité** - Zero duplication, dépendances claires
- 📊 **Métriques** - 17 fichiers Python total (optimisé)
- 🆕 **Données Centralisées** - `src/test_data.py` élimine toute duplication

## 📞 Support

Pour questions techniques ou suggestions:
- 📧 Email: support@kodinet.cd
- 🐛 Issues: GitHub Issues
- 📖 Docs: Wiki du projet

## 📄 Licence

Ce projet est développé pour les services gouvernementaux de la République Démocratique du Congo.

---

## 🎉 Status Final

**KodiBOT v2.0.0 - Architecture Optimisée** ✨

✅ **Codebase Clean**: 17 fichiers Python focalisés  
✅ **Zero Duplications**: Données test centralisées, architecture moderne  
✅ **Tests Complets**: Couverture E2E avec 4 fichiers consolidés  
✅ **Systèmes Centralisés**: Prompts, OpenAI, logging, config, test data  
✅ **Performance**: Structure optimisée, maintenabilité maximale  

**Votre assistant numérique pour les services citoyens RDC** 🇨🇩 