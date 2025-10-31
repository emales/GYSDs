"""
Database Connection Module

Handles PostgreSQL database connections, connection pooling, and user-related queries.
Provides a clean interface for database operations with proper error handling.
"""

import os
import psycopg2
from psycopg2 import pool
import streamlit as st
from contextlib import contextmanager
from typing import Optional, Dict, Any


class DatabaseConnection:
    """
    Manages PostgreSQL database connections and user operations.
    
    Features:
    - Connection pooling for efficiency
    - Context manager for safe connection handling
    - Environment-based configuration
    - User CRUD operations
    """
    
    def __init__(self):
        """Initialize database configuration from environment variables."""
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('POSTGRES_DB', 'gysd_app'),
            'user': os.getenv('POSTGRES_USER', 'postgres'),
            'password': os.getenv('POSTGRES_PASSWORD', 'password'),
            'port': os.getenv('DB_PORT', '5432')
        }
        self._connection_pool = None
    
    def get_connection_pool(self):
        """
        Get or create connection pool.
        
        Returns:
            SimpleConnectionPool: PostgreSQL connection pool or None if failed
        """
        if self._connection_pool is None:
            try:
                self._connection_pool = pool.SimpleConnectionPool(
                    1, 10,  # min=1, max=10 connections
                    **self.config
                )
            except Exception as e:
                st.error(f"Failed to create connection pool: {e}")
                return None
        return self._connection_pool
    
    @contextmanager
    def get_db_connection(self):
        """
        Context manager for safe database connections.
        
        Yields:
            psycopg2.connection: Database connection or None if failed
        """
        conn_pool = self.get_connection_pool()
        if conn_pool is None:
            yield None
            return
            
        conn = None
        try:
            conn = conn_pool.getconn()
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            st.error(f"Database error: {e}")
            yield None
        finally:
            if conn:
                conn_pool.putconn(conn)
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user by username from database.
        
        Args:
            username (str): Username to search for
            
        Returns:
            Dict[str, Any]: User data or None if not found
        """
        with self.get_db_connection() as conn:
            if conn is None:
                return None
                
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, username, password_hash, name, email FROM users WHERE username = %s AND is_active = TRUE",
                    (username,)
                )
                result = cursor.fetchone()
                cursor.close()
                
                if result:
                    return {
                        'id': result[0],
                        'username': result[1],
                        'password_hash': result[2],
                        'name': result[3],
                        'email': result[4]
                    }
                return None
            except Exception as e:
                st.error(f"Error fetching user: {e}")
                return None
    
    def create_user(self, username: str, password_hash: str, name: str, email: str) -> bool:
        """
        Create a new user in database.
        
        Args:
            username (str): Unique username
            password_hash (str): Bcrypt hashed password
            name (str): User's full name
            email (str): User's email address
            
        Returns:
            bool: True if user created successfully, False otherwise
        """
        with self.get_db_connection() as conn:
            if conn is None:
                return False
                
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO users (username, password_hash, name, email) 
                       VALUES (%s, %s, %s, %s)""",
                    (username, password_hash, name, email)
                )
                conn.commit()
                cursor.close()
                return True
            except Exception as e:
                st.error(f"Error creating user: {e}")
                return False
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve user by ID from database.
        
        Args:
            user_id (int): User ID to search for
            
        Returns:
            Dict[str, Any]: User data or None if not found
        """
        with self.get_db_connection() as conn:
            if conn is None:
                return None
                
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, username, password_hash, name, email FROM users WHERE id = %s AND is_active = TRUE",
                    (user_id,)
                )
                result = cursor.fetchone()
                cursor.close()
                
                if result:
                    return {
                        'id': result[0],
                        'username': result[1],
                        'password_hash': result[2],
                        'name': result[3],
                        'email': result[4]
                    }
                return None
            except Exception as e:
                st.error(f"Error fetching user by ID: {e}")
                return None
    
    def update_user_last_login(self, user_id: int) -> bool:
        """
        Update user's last login timestamp.
        
        Args:
            user_id (int): User ID to update
            
        Returns:
            bool: True if updated successfully, False otherwise
        """
        with self.get_db_connection() as conn:
            if conn is None:
                return False
                
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                    (user_id,)
                )
                conn.commit()
                cursor.close()
                return True
            except Exception as e:
                st.error(f"Error updating user last login: {e}")
                return False