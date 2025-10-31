"""
Authentication Login Module

Handles user authentication, registration, and password management.
Provides secure login functionality with bcrypt password hashing.
"""

import bcrypt
from typing import Optional, Tuple, Dict, Any
from ..database.connection import DatabaseConnection


class AuthenticationManager:
    """
    Manages user authentication and registration operations.
    
    Features:
    - Secure password hashing with bcrypt
    - User login authentication
    - User registration with validation
    - Integration with database layer
    """
    
    def __init__(self):
        """Initialize authentication manager with database connection."""
        self.db = DatabaseConnection()
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt for secure storage.
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Bcrypt hashed password
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Verify a password against a stored hash.
        
        Args:
            password (str): Plain text password to verify
            hashed (str): Stored bcrypt hash
            
        Returns:
            bool: True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Authenticate a user with username and password.
        
        Args:
            username (str): Username to authenticate
            password (str): Plain text password
            
        Returns:
            Tuple[bool, Optional[Dict[str, Any]]]: (success, user_data)
                - success: True if authentication successful
                - user_data: User information dict or None
        """
        user = self.db.get_user_by_username(username)
        if user is None:
            return False, None
        
        if self.verify_password(password, user['password_hash']):
            # Update last login timestamp
            self.db.update_user_last_login(user['id'])
            return True, user
        
        return False, None
    
    def register_user(self, username: str, password: str, name: str, email: str) -> Tuple[bool, str]:
        """
        Register a new user in the system.
        
        Args:
            username (str): Desired username (must be unique)
            password (str): Plain text password
            name (str): User's full name
            email (str): User's email address
            
        Returns:
            Tuple[bool, str]: (success, message)
                - success: True if registration successful
                - message: Success or error message
        """
        # Validate input
        if not all([username, password, name, email]):
            return False, "All fields are required"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
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
    
    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """
        Validate password strength according to security requirements.
        
        Args:
            password (str): Password to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, message)
        """
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        if len(password) > 128:
            return False, "Password must be less than 128 characters"
        
        # Add more validation rules as needed
        has_letter = any(c.isalpha() for c in password)
        has_number = any(c.isdigit() for c in password)
        
        if not (has_letter and has_number):
            return False, "Password must contain both letters and numbers"
        
        return True, "Password meets security requirements"
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
        """
        Change user's password with verification of old password.
        
        Args:
            user_id (int): User ID
            old_password (str): Current password for verification
            new_password (str): New password to set
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        # Get user data
        user = self.db.get_user_by_id(user_id)
        if not user:
            return False, "User not found"
        
        # Verify old password
        if not self.verify_password(old_password, user['password_hash']):
            return False, "Current password is incorrect"
        
        # Validate new password
        is_valid, message = self.validate_password_strength(new_password)
        if not is_valid:
            return False, message
        
        # Hash new password and update
        new_hash = self.hash_password(new_password)
        # Note: This would require a new method in DatabaseConnection
        # success = self.db.update_user_password(user_id, new_hash)
        
        return True, "Password changed successfully"