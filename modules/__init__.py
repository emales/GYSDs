"""
GYSD Application Modules

This package contains the core business logic modules for the GYSD Streamlit application.
Organized into logical components for better maintainability and scalability.
"""

__version__ = "1.0.0"
__author__ = "GYSD Team"

# Import main classes for easy access
from .auth.login import AuthenticationManager
from .auth.session import SessionManager
from .database.connection import DatabaseConnection

__all__ = [
    "AuthenticationManager",
    "SessionManager", 
    "DatabaseConnection"
]