"""
Centralized Test Configuration
Eliminates hardcoded URLs and provides consistent test settings
"""

import os
from src.test_data import (
    get_primary_phone, get_secondary_phone, get_primary_citizen_id, 
    get_test_otp, TEST_MESSAGES, EXPECTED_RESPONSES
)

# Base URLs for testing
DEFAULT_API_BASE = "http://localhost:8000"
DEFAULT_FRONTEND_BASE = "http://localhost:3000"

class TestConfig:
    """Centralized configuration for all tests"""
    
    # API Configuration
    API_BASE = os.getenv("TEST_API_BASE", DEFAULT_API_BASE)
    FRONTEND_BASE = os.getenv("TEST_FRONTEND_BASE", DEFAULT_FRONTEND_BASE)
    
    # Test Data (imported from centralized test_data module)
    TEST_PHONE_LINKED = get_primary_phone()         # Pre-linked user (Jean Kabila)
    TEST_PHONE_UNLINKED = get_secondary_phone()     # Unlinked user (Marie Tshisekedi)
    TEST_CITIZEN_ID = get_primary_citizen_id()       # Valid citizen ID
    TEST_OTP_CODE = get_test_otp()                   # Standard test OTP
    
    # Test Timeouts
    API_TIMEOUT = 30  # seconds
    FRONTEND_TIMEOUT = 10  # seconds
    
    # Test Messages (imported from centralized module)
    TEST_MESSAGES = TEST_MESSAGES
    
    # Expected Responses (imported from centralized module)
    EXPECTED_RESPONSES = EXPECTED_RESPONSES
    
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