import os
import bcrypt
import psycopg2
from psycopg2 import pool
import streamlit as st
from contextlib import contextmanager
from typing import Optional, Tuple, Dict, Any

class DBConn:
    """Handles all database operations"""
    
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST', 'cannot read host from env'),
            'database': os.getenv('POSTGRES_DB', 'cannot read database from env'),
            'user': os.getenv('POSTGRES_USER', 'cannot read user from env'),
            'password': os.getenv('POSTGRES_PASSWORD', 'cannot read password from env'),
            'port': os.getenv('DB_PORT', 'cannot read port from env')
        }
        self._connection_pool = None
    
    def get_connection_pool(self):
        """Get or create connection pool"""
        if self._connection_pool is None:
            try:
                self._connection_pool = pool.SimpleConnectionPool(
                    1, 20,  # min and max connections
                    **self.config
                )
            except Exception as e:
                st.error(f"Failed to create connection pool: {e}")
                return None
        return self._connection_pool
    
    @contextmanager
    def get_db_connection(self):
        """Context manager for database connections"""
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
        """Get user by username from database"""
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
        """Create a new user in database"""
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

class AuthenticationManager:
    """Handles user authentication and password management"""
    
    def __init__(self):
        self.db = DBConn()
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password for storing in the database"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify a stored password against one provided by user"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Authenticate a user
        Returns: (success: bool, user_data: dict or None)
        """
        user = self.db.get_user_by_username(username)
        if user is None:
            return False, None
        
        if self.verify_password(password, user['password_hash']):
            return True, user
        
        return False, None
    
    def register_user(self, username: str, password: str, name: str, email: str) -> Tuple[bool, str]:
        """
        Register a new user
        Returns: (success: bool, message: str)
        """
        # Check if user already exists
        existing_user = self.db.get_user_by_username(username)
        if existing_user:
            return False, "Username already exists"
        
        # Hash password and create user
        password_hash = self.hash_password(password)
        success = self.db.create_user(username, password_hash, name, email)
        
        if success:
            return True, "User registered successfully"
        else:
            return False, "Failed to register user"

class SessionManager:
    """Handles Streamlit session state management"""
    
    @staticmethod
    def login_user(user_data: Dict[str, Any]):
        """Set session state for logged in user"""
        st.session_state["authenticated"] = True
        st.session_state["user_id"] = user_data['id']
        st.session_state["username"] = user_data['username']
        st.session_state["user_name"] = user_data['name']
        st.session_state["user_email"] = user_data['email']
    
    @staticmethod
    def logout_user():
        """Clear session state"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    
    @staticmethod
    def is_authenticated() -> bool:
        """Check if user is authenticated"""
        return st.session_state.get("authenticated", False)
    
    @staticmethod
    def get_current_user() -> Optional[Dict[str, Any]]:
        """Get current user data from session"""
        if not SessionManager.is_authenticated():
            return None
            
        return {
            'id': st.session_state.get("user_id"),
            'username': st.session_state.get("username"),
            'name': st.session_state.get("user_name"),
            'email': st.session_state.get("user_email")
        }
   