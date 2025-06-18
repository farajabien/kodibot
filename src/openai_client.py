"""
Centralized OpenAI Client Configuration
Eliminates duplication and ensures consistent error handling
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_openai_client() -> OpenAI:
    """
    Get a configured OpenAI client instance
    Centralized configuration with proper error handling
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found in environment variables. "
            "Please add it to your .env file: OPENAI_API_KEY=sk-proj-..."
        )
    
    return OpenAI(api_key=api_key)

def validate_openai_config() -> tuple[bool, str]:
    """
    Validate OpenAI configuration
    Returns (is_valid, message)
    """
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return False, "❌ OPENAI_API_KEY manquante dans le fichier .env"
        
        if len(api_key) < 20:
            return False, "❌ OPENAI_API_KEY semble invalide (trop courte)"
        
        return True, f"✅ Clé API trouvée: {api_key[:20]}..."
    
    except Exception as e:
        return False, f"❌ Erreur validation OpenAI: {e}"

# Global client instance (lazy loading)
_client = None

def get_client() -> OpenAI:
    """Get the global OpenAI client instance (singleton pattern)"""
    global _client
    if _client is None:
        _client = get_openai_client()
    return _client 