"""
Authentication Screen

Handles user login and registration functionality.
Provides a clean UI for authentication with form validation.
"""

import streamlit as st
import time
from typing import Optional
from .base_screen import BaseScreen
from modules.auth import AuthenticationManager, SessionManager


class AuthScreen(BaseScreen):
    """
    Authentication screen for login and registration.
    
    Features:
    - Login form with validation
    - Registration form with password confirmation
    - Toggle between login and registration modes
    - Demo credentials display
    - Automatic redirect after successful authentication
    """
    
    def __init__(self):
        super().__init__("auth", "🔐 Welcome to GYSD App")
        self.auth_manager = self._get_auth_manager()
    
    @st.cache_resource
    def _get_auth_manager(_self):
        """Get cached authentication manager instance."""
        return AuthenticationManager()
    
    def validate_access(self) -> bool:
        """Auth screen is accessible to everyone."""
        return True
    
    def get_navigation_info(self) -> dict:
        """Auth screen navigation info."""
        return {
            "name": self.screen_name,
            "title": self.title,
            "requires_auth": False,
            "sidebar_visible": False  # Hide sidebar on auth screen
        }
    
    def on_enter(self) -> None:
        """Initialize auth screen state."""
        if "show_register" not in st.session_state:
            st.session_state.show_register = False
    
    def render(self) -> Optional[str]:
        """Render the authentication screen."""
        # Check if already authenticated
        if SessionManager.is_authenticated():
            return "dashboard"
        
        # Create centered layout
        col1, col2, col3 = self.create_columns([1, 2, 1])
        
        with col2:
            if not st.session_state.get("show_register", False):
                return self._render_login_form()
            else:
                return self._render_registration_form()
    
    def _render_login_form(self) -> Optional[str]:
        """Render the login form."""
        st.markdown("### Login to Your Account")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            login_button = st.form_submit_button("Login", use_container_width=True)
            
            if login_button:
                return self._handle_login(username, password)
        
        st.markdown("---")
        
        # Register button
        st.markdown("Don't have an account?")
        if st.button("Register here", use_container_width=True, type="secondary"):
            st.session_state.show_register = True
            st.rerun()
        
        self._render_demo_credentials()
        return None
    
    def _render_registration_form(self) -> Optional[str]:
        """Render the registration form."""
        st.markdown("### Create New Account")
        
        with st.form("register_form"):
            reg_username = st.text_input("Username", placeholder="Choose a username", key="reg_username")
            reg_name = st.text_input("Full Name", placeholder="Enter your full name", key="reg_name")
            reg_email = st.text_input("Email", placeholder="Enter your email address", key="reg_email")
            reg_password = st.text_input("Password", type="password", placeholder="Choose a password", key="reg_password")
            reg_password_confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="reg_password_confirm")
            
            register_button = st.form_submit_button("Create Account", use_container_width=True)
            
            if register_button:
                return self._handle_registration(reg_username, reg_name, reg_email, reg_password, reg_password_confirm)
        
        st.markdown("---")
        
        # Back to login button
        st.markdown("Already have an account?")
        if st.button("Back to Login", use_container_width=True, type="secondary"):
            st.session_state.show_register = False
            st.rerun()
        
        self._render_demo_credentials()
        return None
    
    def _handle_login(self, username: str, password: str) -> Optional[str]:
        """Handle login form submission."""
        if not username or not password:
            self.show_error("Please enter both username and password")
            return None
        
        # Authenticate user
        success, user_data = self.auth_manager.authenticate_user(username, password)
        
        if success and user_data:
            # Use SessionManager to handle login
            SessionManager.login_user(user_data)
            self.show_success("Login successful! Redirecting...")
            time.sleep(1)
            return "dashboard"
        else:
            self.show_error("Invalid username or password")
            return None
    
    def _handle_registration(self, username: str, name: str, email: str, password: str, password_confirm: str) -> Optional[str]:
        """Handle registration form submission."""
        # Validate all fields are filled
        if not all([username, name, email, password, password_confirm]):
            self.show_error("Please fill in all fields")
            return None
        
        # Validate passwords match
        if password != password_confirm:
            self.show_error("Passwords do not match")
            return None
        
        # Validate password length
        if len(password) < 6:
            self.show_error("Password must be at least 6 characters long")
            return None
        
        # Register user
        success, message = self.auth_manager.register_user(username, password, name, email)
        
        if success:
            self.show_success(f"{message}! You can now login with your credentials.")
            st.session_state.show_register = False
            time.sleep(2)
            st.rerun()
            return None
        else:
            self.show_error(message)
            return None
    
    def _render_demo_credentials(self) -> None:
        """Render demo credentials expander."""
        with st.expander("Demo Credentials"):
            st.info("""
            **For testing purposes:**
            - Username: `admin` | Password: `admin123`
            - Username: `user1` | Password: `user123`
            """)
    
    def on_exit(self) -> None:
        """Clean up auth screen state when leaving."""
        # Reset registration toggle
        if "show_register" in st.session_state:
            st.session_state.show_register = False