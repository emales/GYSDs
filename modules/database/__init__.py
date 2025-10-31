"""
Database Module

Handles all database-related functionality including:
- Database connection management
- Connection pooling
- User queries and operations
"""

from .connection import DatabaseConnection

__all__ = ["DatabaseConnection"]