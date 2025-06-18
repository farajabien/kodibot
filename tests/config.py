"""
Centralized Test Configuration
Eliminates hardcoded URLs and provides consistent test settings
"""

import os

# Base URLs for testing
DEFAULT_API_BASE = "http://localhost:8000"
DEFAULT_FRONTEND_BASE = "http://localhost:3000"

class TestConfig:
    """Centralized configuration for all tests"""
    
    # API Configuration
    API_BASE = os.getenv("TEST_API_BASE", DEFAULT_API_BASE)
    FRONTEND_BASE = os.getenv("TEST_FRONTEND_BASE", DEFAULT_FRONTEND_BASE)
    
    # Test Data
    TEST_PHONE_LINKED = "+243123456789"      # Pre-linked user (Jean Kabila)
    TEST_PHONE_UNLINKED = "+243987654321"    # Unlinked user (Marie Tshisekedi)
    TEST_CITIZEN_ID = "CIT123456789"          # Valid citizen ID
    TEST_OTP_CODE = "123456"                  # Standard test OTP
    
    # Test Timeouts
    API_TIMEOUT = 30  # seconds
    FRONTEND_TIMEOUT = 10  # seconds
    
    # Test Messages
    TEST_MESSAGES = {
        "greeting": "Bonjour",
        "tax_info": "Quel est mon solde fiscal?",
        "parcels": "Mes parcelles",
        "procedures": "Comment renouveler mon permis?",
        "profile": "Quel est mon nom?",
        "goodbye": "Au revoir"
    }
    
    # Expected Responses (for validation)
    EXPECTED_RESPONSES = {
        "linking_required": "Bienvenue sur KodiBOT! 📋 Pour accéder",
        "quota_exceeded": "temporairement indisponible",
        "otp_generated": "Code OTP généré",
        "linking_success": "Liaison réussie"
    }
    
    @classmethod
    def get_api_url(cls, endpoint: str) -> str:
        """Get full API URL for endpoint"""
        return f"{cls.API_BASE}{endpoint}"
    
    @classmethod
    def get_frontend_url(cls, path: str = "") -> str:
        """Get full frontend URL for path"""
        return f"{cls.FRONTEND_BASE}{path}"
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development mode"""
        return cls.API_BASE == DEFAULT_API_BASE 