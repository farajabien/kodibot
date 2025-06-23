"""
Centralized Test Configuration
Eliminates hardcoded URLs and provides consistent test settings
"""

import os
from src.test_data import (
    get_patrick_phone, get_patrick_citizen_id, TEST_MESSAGES,
    PATRICK_DAUDI, BIENVENU_FARAJA, TEST_AUTH
)

# Base URLs for testing
DEFAULT_API_BASE = "http://localhost:8000"
DEFAULT_FRONTEND_BASE = "http://localhost:3000"

class TestConfig:
    """Centralized configuration for all tests"""
    
    # API Configuration
    API_BASE = os.getenv("TEST_API_BASE", DEFAULT_API_BASE)
    FRONTEND_BASE = os.getenv("TEST_FRONTEND_BASE", DEFAULT_FRONTEND_BASE)
    
    # Test Data (using our real user data)
    TEST_PHONE_LINKED = get_patrick_phone()         # Pre-linked user (Patrick Daudi)
    TEST_PHONE_UNLINKED = BIENVENU_FARAJA["phone_number"]  # Unlinked user (Bienvenu Faraja)
    TEST_CITIZEN_ID = get_patrick_citizen_id()       # Valid citizen ID
    TEST_OTP_CODE = TEST_AUTH["otp_code"]            # Standard test OTP
    
    # Test Timeouts
    API_TIMEOUT = 30  # seconds
    FRONTEND_TIMEOUT = 10  # seconds
    
    # Test Messages (imported from centralized module)
    TEST_MESSAGES = TEST_MESSAGES
    
    # Expected Responses (simplified for our current setup)
    EXPECTED_RESPONSES = {
        "greeting": "Bonjour",
        "tax_info": "solde fiscal",
        "parcels": "parcelles",
        "procedures": "permis de conduire",
        "profile": "informations personnelles",
        "goodbye": "Au revoir"
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