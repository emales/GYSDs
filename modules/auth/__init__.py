"""
Authentication Module

Handles all authentication-related functionality including:
- User login and registration
- Password hashing and verification  
- Session state management
"""

from .login import AuthenticationManager
from .session import SessionManager

__all__ = ["AuthenticationManager", "SessionManager"]