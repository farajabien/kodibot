"""
Centralized Logging System for KodiBOT
Replaces scattered print statements with structured logging
"""

import logging
import os
from datetime import datetime
from typing import Optional

class KodiBOTLogger:
    """
    Centralized logger for KodiBOT application
    Provides structured logging with different levels and contexts
    """
    
    def __init__(self, name: str = "kodibot", level: str = "INFO"):
        self.logger = logging.getLogger(name)
        
        # Set level from environment or default
        log_level = os.getenv("LOG_LEVEL", level).upper()
        self.logger.setLevel(getattr(logging, log_level, logging.INFO))
        
        # Avoid duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup console and file handlers"""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (optional, for production)
        if os.getenv("LOG_TO_FILE", "false").lower() == "true":
            file_handler = logging.FileHandler("kodibot.log")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, message: str, context: Optional[dict] = None):
        """Log info message with optional context"""
        if context:
            message = f"{message} | Context: {context}"
        self.logger.info(message)
    
    def error(self, message: str, error: Optional[Exception] = None, context: Optional[dict] = None):
        """Log error message with optional exception and context"""
        if error:
            message = f"{message} | Error: {str(error)}"
        if context:
            message = f"{message} | Context: {context}"
        self.logger.error(message)
    
    def warning(self, message: str, context: Optional[dict] = None):
        """Log warning message with optional context"""
        if context:
            message = f"{message} | Context: {context}"
        self.logger.warning(message)
    
    def debug(self, message: str, context: Optional[dict] = None):
        """Log debug message with optional context"""
        if context:
            message = f"{message} | Context: {context}"
        self.logger.debug(message)
    
    def chat_log(self, phone_number: str, message: str, direction: str, intent: str = None):
        """Specialized logging for chat interactions"""
        context = {
            "phone": phone_number,
            "direction": direction,
            "intent": intent,
            "message_length": len(message)
        }
        self.info(f"Chat {direction}: {message[:100]}...", context)
    
    def openai_log(self, action: str, model: str = None, tokens: int = None, error: Exception = None):
        """Specialized logging for OpenAI API calls"""
        context = {
            "action": action,
            "model": model,
            "tokens": tokens
        }
        
        if error:
            self.error(f"OpenAI {action} failed", error, context)
        else:
            self.info(f"OpenAI {action} successful", context)
    
    def quota_exceeded(self, service: str = "OpenAI"):
        """Log quota exceeded events"""
        self.warning(f"{service} quota exceeded, using fallback", {
            "service": service,
            "timestamp": datetime.now().isoformat()
        })

# Global logger instances
logger = KodiBOTLogger()
chat_logger = KodiBOTLogger("kodibot.chat")
openai_logger = KodiBOTLogger("kodibot.openai")

# Convenience functions for backward compatibility
def log_info(message: str, context: dict = None):
    """Backward compatible info logging"""
    logger.info(message, context)

def log_error(message: str, error: Exception = None, context: dict = None):
    """Backward compatible error logging"""
    logger.error(message, error, context)

def log_warning(message: str, context: dict = None):
    """Backward compatible warning logging"""
    logger.warning(message, context)

def log_chat(phone_number: str, message: str, direction: str, intent: str = None):
    """Backward compatible chat logging"""
    chat_logger.chat_log(phone_number, message, direction, intent)

def log_openai(action: str, model: str = None, tokens: int = None, error: Exception = None):
    """Backward compatible OpenAI logging"""
    openai_logger.openai_log(action, model, tokens, error) 