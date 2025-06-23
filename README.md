# 🤖 KodiBOT API

**Assistant WhatsApp intelligent pour les services gouvernementaux de la République Démocratique du Congo**

KodiBOT facilite l'accès aux services gouvernementaux RDC via une interface conversationnelle moderne, permettant aux citoyens de consulter leurs informations fiscales, foncières et administratives.

---

## 🚀 Quick Start

```bash
# 1. Clone and setup
git clone <repository>
cd kodibot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Seed database with real user data
python scripts/seed_data.py

# 4. Start the API
python main.py
```

**API running at:** `http://localhost:8000`  
**Interactive docs:** `http://localhost:8000/docs`

### Alternative Start Methods
```bash
# Direct Python (current method)
python main.py

# With uvicorn (for production)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# With Docker (recommended)
docker-compose up --build
```

---

## 🎯 Features

### 🔗 **Account Linking**
- Secure OTP-based phone number verification
- Link citizen ID to WhatsApp numbers
- Persistent user sessions

### 💬 **Intelligent Chat**
- Natural language understanding
- Intent classification with confidence scoring
- Contextual responses with user data

### 🏛️ **Government Services**
- **📊 Tax Information**: Balance, payment history, due dates
- **💳 E-Tax Status**: Digital portal access, compliance scores, account verification
- **🏠 Property Data**: Parcels, cadastral information, valuations
- **📋 K-CAF Records**: Property assessment and compliance data
- **👤 Profile Management**: Personal information, addresses
- **📋 Procedures**: Permit renewals, document requests

### 🔍 **Analytics & Monitoring**
- Chat logs with intent tracking
- Popular queries analytics
- Health monitoring endpoints

---

## 👥 Test Users (Pre-linked)

The database comes with real team members for testing:

| Name | Phone | Citizen ID | Role | Properties | Tax Status | E-Tax Status |
|------|--------|------------|------|------------|------------|--------------|
| **Patrick Daudi** | `+243842616809` | `CIT842616809` | 👑 **Founder** | 3 properties | All paid (2.5M FC) | ✅ Active |
| **Bienvenu Faraja** | `+254793643308` | `CIT793643308` | Developer | 1 apartment | Partial payment | ⚠️ Pending |
| **Ombeni Faraja** | `+254729054607` | `CIT729054607` | Developer | 1 house | Paid | ✅ Active |
| **Prince Makeo** | `+243971127650` | `CIT971127650` | Developer | 1 villa | Partial payment | ⚠️ Pending |
| **Nickson Maliva** | `+243993710507` | `CIT993710507` | Developer | 1 duplex | Paid | ✅ Active |
| **Heri Mujyambere** | `+243070624910` | `CIT070624910` | Developer | 1 family home | Partial payment | ⚠️ Pending |
| **Jean-Pierre Mukendi** | `+25411820424` | `CIT011820424` | Developer | 1 studio | Paid | ✅ Active |

### 🧪 **Testing E-Tax Status**

Test the E-Tax endpoint with any of these citizen IDs:

```bash
# Test Patrick Daudi's E-Tax status (Premium account)
curl http://localhost:8000/etax-status/CIT842616809

# Test Bienvenu Faraja's E-Tax status (Pending verification)
curl http://localhost:8000/etax-status/CIT793643308

# Test Ombeni Faraja's E-Tax status (Standard account)
curl http://localhost:8000/etax-status/CIT729054607
```

### 💬 **Testing E-Tax via Chat**

You can also test E-Tax status through the chat interface:

```bash
# Test with Patrick Daudi (Premium account)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+243842616809",
    "message": "Quel est mon statut E-Tax?"
  }'

# Test with Bienvenu Faraja (Pending verification)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+254793643308", 
    "message": "Mon statut E-Tax"
  }'
```

**Expected Chat Responses:**
- **Patrick Daudi**: Premium account with excellent compliance (95/100)
- **Bienvenu Faraja**: Pending verification with good compliance (75/100)
- **Others**: Various statuses from active to pending

---

## 🔧 API Endpoints

### 💬 **Chat**
```http
POST /chat
{
  "phone_number": "+243842616809",
  "message": "Quel est mon solde fiscal?"
}
```

### 🔐 **Account Linking**
```http
POST /link-account
{
  "phone_number": "+243842616809", 
  "citizen_id": "CIT842616809"
}

POST /verify-otp
{
  "phone_number": "+243842616809",
  "otp_code": "123456"
}
```

### 📋 **K-CAF Records**
```http
POST /kcaf-records
{
  "parcel_number": "P001-GOMBE-2024",
  "nature_propriete": "Bâtie",
  "usage_principal": "Résidentiel",
  "nom_proprietaire": "Patrick Daudi",
  "nationalite_proprietaire": "National",
  "type_possession": "Titre Foncier",
  "adresse_commune": "Gombe",
  "adresse_quartier": "Centre",
  "adresse_avenue": "Boulevard du 30 Juin",
  "adresse_numero": "100",
  "type_personne": "Physique",
  "type_batiment": "Maison principale",
  "nombre_etages": "R+2",
  "nombre_appartements": 1,
  "nombre_appartements_vides": 0,
  "plaque_identification": true,
  "raccordements": {"eau": true, "electricite": true, "telecom": true, "assainissement": true},
  "distance_sante": "<1KM",
  "distance_education": "<1KM",
  "acces_eau_potable": {"reseau": true, "puit": false},
  "gestion_dechets": {"collecte_municipale": true},
  "montant_a_payer": 1500.0,
  "etat": "Complet",
  "numero_collecteur": "COLLECTOR-001"
}

GET /kcaf-records/{parcel_number}
```

### 💳 **E-Tax Status**
```http
GET /etax-status/{citizen_id}
```

**Example Response:**
```json
{
  "status": "active",
  "status_display": "✅ Active",
  "account_type": "premium",
  "verification_level": "✅ Verified",
  "registration_date": "15/01/2023",
  "last_login": "20/06/2024",
  "payment_methods": ["mobile_money", "bank_transfer", "card"],
  "notifications_enabled": true,
  "auto_payment_setup": true,
  "tax_returns_filed": 3,
  "last_filing_date": "31/03/2024",
  "compliance_score": 95,
  "compliance_level": "Excellent"
}
```

**E-Tax Status Types:**
- **✅ Active**: Account fully functional with verified status
- **⚠️ Pending**: Account created but verification in progress
- **❌ Suspended**: Account temporarily suspended (not in test data)

**Account Types:**
- **Premium**: Full access with multiple payment methods
- **Standard**: Basic access with limited payment options

**Compliance Levels:**
- **Excellent** (90-100): Outstanding compliance record
- **Bon** (80-89): Good compliance with minor issues
- **Moyen** (70-79): Average compliance, needs attention
- **À améliorer** (<70): Below average, requires action

### 📊 **Data Endpoints**
```http
GET /test-users          # Get all test users
GET /debug-db            # Database diagnostics
GET /analytics/popular-intents  # Usage analytics
GET /                    # Health check
```

---

## 🏗️ Project Structure

```
kodibot/
├── main.py              # 🚀 Main application & startup
├── requirements.txt     # 📦 Dependencies
├── kodibot.db          # 💾 SQLite database
├── src/
│   ├── kodibot.py      # 🤖 Bot logic & responses
│   ├── database.py     # 🗄️ Models & schema
│   ├── services.py     # 🔧 Business logic & handlers
│   ├── model.py        # 🧠 AI/ML intent classification
│   ├── prompts.py      # 💭 LLM system prompts
│   ├── models.py       # 📝 Request/response models
│   ├── openai_client.py # 🔌 OpenAI integration
│   ├── logger.py       # 📋 Logging system
│   └── test_data.py    # 👥 Real user test data
├── scripts/
│   └── seed_data.py    # 🌱 Database seeding
└── tests/
    ├── health_check.py # 🏥 Health diagnostics
    └── test_integration.py # 🧪 Integration tests
```

---

## 🛠️ Technology Stack

- **🐍 Backend**: FastAPI + Uvicorn
- **🗄️ Database**: SQLAlchemy + SQLite
- **🧠 AI**: OpenAI GPT-4o-mini
- **🔍 Intent Classification**: Hybrid LLM + rule-based
- **📦 Containerization**: Docker + Docker Compose
- **🧪 Testing**: Custom integration suite

---

## 🐳 Docker Deployment

### Development
```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f kodibot
```

### Production
```bash
# Set environment variables
export OPENAI_API_KEY=your_key_here
export ENVIRONMENT=production
export WORKERS=4

# Run
docker-compose up -d --build
```

### Environment Variables
```bash
HOST=0.0.0.0                    # Server host
PORT=8000                       # Server port  
WORKERS=1                       # Uvicorn workers
LOG_LEVEL=info                  # Logging level
ENVIRONMENT=development         # Environment mode
OPENAI_API_KEY=your_key_here   # OpenAI API key
DATABASE_URL=sqlite:///kodibot.db # Database URL
```

---

## 🧪 Testing

### Health Check
```bash
python tests/health_check.py
```

### Test K-CAF Endpoints
```bash
# Create K-CAF record
curl -X POST "http://localhost:8000/kcaf-records" \
  -H "Content-Type: application/json" \
  -d @test_kcaf_data.json

# Get K-CAF record
curl "http://localhost:8000/kcaf-records/P001-GOMBE-2024"
```

---

## 📋 K-CAF Data Structure

The K-CAF (Cadastre et Aménagement Foncier) module includes:

### 🏠 **Property Information**
- Nature of property (Built/Unbuilt)
- Main usage (Residential, Commercial, etc.)
- Building structure and floors
- Apartment details and occupancy

### 👤 **Owner Information**
- Full name and nationality
- Type of possession (Title deed, Customary right, etc.)
- Contact information and civil status

### 📍 **Location Details**
- Complete address (City, Commune, Quarter, Avenue, Number)
- Building type and classification

### 🏥 **Compliance & Environment**
- Physical identification plaque
- Utility connections (Water, Electricity, Telecom, Sanitation)
- Distance to health and educational institutions
- Water access and waste management
- Compliance status and payment amounts

---

## 🔄 Development Workflow

### 1. **Database Reset**
```bash
python scripts/seed_data.py
```

### 2. **Start Development**
```bash
# Option A: Direct Python (simple)
python main.py

# Option B: With uvicorn (better for development)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Option C: Docker (production-like)
docker-compose up --build
```

### 3. **Test Changes**
```bash
python tests/health_check.py
curl http://localhost:8000/test-users
```

### 4. **Deploy**
```bash
export ENVIRONMENT=production
docker-compose up -d --build
```

---

## 📈 Chat Flow

1. **📱 Message Received** → Log inbound
2. **🔗 Check Linking** → Prompt if unlinked  
3. **🧠 Intent Extraction** → Classify user intent
4. **📊 Fetch Data** → Get relevant user information
5. **💭 LLM Generation** → Create personalized response
6. **📝 Log Response** → Track outbound message

---

## 🌍 Environment Setup

### Local Development
```bash
# Clone repository
git clone <repository>
cd kodibot

# Install dependencies  
pip install -r requirements.txt

# Set up environment
export OPENAI_API_KEY=your_key_here

# Initialize database
python scripts/seed_data.py

# Start server (choose one)
python main.py                                    # Simple start
uvicorn main:app --host 0.0.0.0 --port 8000 --reload  # With auto-reload
```

### Production Deployment
```bash
# Set production environment
export ENVIRONMENT=production
export WORKERS=4
export PORT=8000

# Deploy with Docker
docker-compose up -d --build
```

---

## 🚨 Troubleshooting

### Warning: "You must pass the application as an import string"
If you see this warning when running `python main.py`, it's harmless but can be avoided:

```bash
# Instead of: python main.py
# Use: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Common Issues
- **Port 8000 in use**: Change port with `export PORT=8001`
- **Database errors**: Run `python scripts/seed_data.py`
- **OpenAI errors**: Check your `OPENAI_API_KEY` environment variable
- **Docker issues**: Run `docker-compose down && docker-compose up --build`

---

## 🔗 Integration

### WhatsApp Integration
```javascript
// Frontend integration example
const sendMessage = async (phone, message) => {
  const response = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ phone_number: phone, message })
  });
  return response.json();
};
```

---

## 🤝 Contributing

### Team Members
- **Patrick Daudi** - Founder & Product Owner
- **Bienvenu Faraja** - Lead Developer  
- **Development Team** - Backend & AI specialists

### Development Guidelines
- **Code Style**: Follow PEP 8
- **Testing**: Add tests for new features
- **Documentation**: Update README for API changes
- **Commits**: Descriptive messages in English/French

---

## 📞 Support

- **🌐 Website**: [kodinet.cd](https://kodinet.cd)
- **📧 Support**: support@kodinet.cd
- **🐛 Issues**: GitHub Issues
- **👥 Team**: Kodinet Development Team

---

**🇨🇩 Développé pour les services gouvernementaux de la République Démocratique du Congo**

*KodiBOT - Votre assistant numérique pour les services citoyens*