"""
Centralized Test Data Constants
Eliminates duplication between seed scripts and test configuration
"""

from datetime import datetime
from typing import Dict, List, Any

# 📋 PRIMARY TEST CITIZEN (Jean Kabila - Linked User)
PRIMARY_CITIZEN = {
    "phone_number": "+243123456789",
    "citizen_id": "CIT123456789", 
    "first_name": "Jean",
    "last_name": "Kabila",
    "email": "jean.kabila@example.com",
    "address": "Avenue de la Liberté, Kinshasa, RDC",
    "date_of_birth": datetime(1980, 5, 15),
    "is_verified": True
}

# 📋 SECONDARY TEST CITIZEN (Marie Tshisekedi - Unlinked User)
SECONDARY_CITIZEN = {
    "phone_number": "+243987654321",
    "citizen_id": "CIT987654321",
    "first_name": "Marie", 
    "last_name": "Tshisekedi",
    "email": "marie.tshisekedi@example.com",
    "address": "Avenue du Commerce, Lubumbashi, RDC",
    "date_of_birth": datetime(1985, 8, 22),
    "is_verified": True
}

# 💰 TEST TAX RECORDS
TEST_TAXES = [
    {
        "tax_type": "Taxe foncière",
        "amount_due": 250000.0,
        "amount_paid": 150000.0,
        "due_date": datetime(2024, 12, 31),
        "status": "pending",
        "tax_year": 2024
    },
    {
        "tax_type": "Taxe professionnelle", 
        "amount_due": 180000.0,
        "amount_paid": 180000.0,
        "due_date": datetime(2024, 6, 30),
        "status": "paid",
        "tax_year": 2024
    }
]

# 🏠 TEST PARCELS
TEST_PARCELS = [
    {
        "parcel_number": "P001-KIN-2024",
        "property_type": "Maison",
        "address": "Parcelle 123, Commune de Gombe, Kinshasa",
        "area_sqm": 500.0,
        "estimated_value": 85_000_000.0,
        "status": "active"
    },
    {
        "parcel_number": "P002-KIN-2024", 
        "property_type": "Terrain",
        "address": "Parcelle 456, Commune de Limete, Kinshasa",
        "area_sqm": 800.0,
        "estimated_value": 45_000_000.0,
        "status": "active"
    }
]

# 📋 TEST PROCEDURES
TEST_PROCEDURES = [
    {
        "name": "Renouvellement de permis de conduire",
        "description": "Procédure pour renouveler votre permis de conduire",
        "steps": [
            "1. Rassembler les documents requis",
            "2. Se rendre au bureau des transports", 
            "3. Payer les frais de renouvellement",
            "4. Passer l'examen médical",
            "5. Récupérer le nouveau permis"
        ],
        "required_documents": [
            "Ancien permis de conduire",
            "Certificat médical",
            "2 photos passeport", 
            "Reçu de paiement"
        ],
        "estimated_duration": "2-3 semaines",
        "cost": 25000.0,
        "department": "Ministère des Transports"
    },
    {
        "name": "Demande de passeport",
        "description": "Procédure pour obtenir un nouveau passeport",
        "steps": [
            "1. Remplir le formulaire de demande",
            "2. Fournir les documents requis",
            "3. Payer les frais consulaires",
            "4. Attendre la production",
            "5. Récupérer le passeport"
        ],
        "required_documents": [
            "Acte de naissance",
            "Carte d'identité", 
            "4 photos biométriques",
            "Justificatif de domicile"
        ],
        "estimated_duration": "4-6 semaines",
        "cost": 150000.0,
        "department": "Ministère des Affaires Étrangères"
    }
]

# 🔐 TEST AUTHENTICATION
TEST_AUTH = {
    "otp_code": "123456",
    "session_timeout": 3600,  # 1 hour
    "max_attempts": 3
}

# 💬 TEST MESSAGES
TEST_MESSAGES = {
    "greeting": "Bonjour",
    "tax_info": "Quel est mon solde fiscal?",
    "parcels": "Mes parcelles", 
    "procedures": "Comment renouveler mon permis?",
    "profile": "Quel est mon nom?",
    "goodbye": "Au revoir"
}

# ✅ EXPECTED RESPONSES
EXPECTED_RESPONSES = {
    "linking_required": "Bienvenue sur KodiBOT! 📋 Pour accéder",
    "quota_exceeded": "temporairement indisponible",
    "otp_generated": "Code OTP généré", 
    "linking_success": "Liaison réussie"
}

# 🔧 CONVENIENCE FUNCTIONS
def get_primary_phone() -> str:
    """Get primary test user phone number"""
    return PRIMARY_CITIZEN["phone_number"]

def get_primary_citizen_id() -> str:
    """Get primary test user citizen ID"""
    return PRIMARY_CITIZEN["citizen_id"]

def get_secondary_phone() -> str:
    """Get secondary test user phone number (unlinked)"""
    return SECONDARY_CITIZEN["phone_number"]

def get_test_otp() -> str:
    """Get standard test OTP code"""
    return TEST_AUTH["otp_code"] 