"""
Session Management Module

Handles Streamlit session state management for user authentication.
Provides secure session handling with user data storage and cleanup.
"""

import streamlit as st
from typing import Optional, Dict, Any


class SessionManager:
    """
    Manages Streamlit session state for user authentication.
    
    Features:
    - Secure session state management
    - User data storage in session
    - Session cleanup and logout
    - Authentication status checking
    """
    
    # Session keys used for storing user data
    SESSION_AUTHENTICATED = "authenticated"
    SESSION_USER_ID = "user_id"
    SESSION_USERNAME = "username"
    SESSION_USER_NAME = "user_name"
    SESSION_USER_EMAIL = "user_email"
    SESSION_LOGIN_TIME = "login_time"
    
    @staticmethod
    def login_user(user_data: Dict[str, Any]) -> None:
        """
        Set session state for a logged-in user.
        
        Args:
            user_data (Dict[str, Any]): User information from database
                Expected keys: id, username, name, email
        """
        import time
        
        # Store authentication status
        st.session_state[SessionManager.SESSION_AUTHENTICATED] = True
        
        # Store user data
        st.session_state[SessionManager.SESSION_USER_ID] = user_data.get('id')
        st.session_state[SessionManager.SESSION_USERNAME] = user_data.get('username')
        st.session_state[SessionManager.SESSION_USER_NAME] = user_data.get('name')
        st.session_state[SessionManager.SESSION_USER_EMAIL] = user_data.get('email')
        
        # Store login timestamp
        st.session_state[SessionManager.SESSION_LOGIN_TIME] = time.time()
    
    @staticmethod
    def logout_user() -> None:
        """
        Clear all session state data and log out the user.
        """
        # Clear all session state keys
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    
    @staticmethod
    def is_authenticated() -> bool:
        """
        Check if a user is currently authenticated.
        
        Returns:
            bool: True if user is authenticated, False otherwise
        """
        return st.session_state.get(SessionManager.SESSION_AUTHENTICATED, False)
    
    @staticmethod
    def get_current_user() -> Optional[Dict[str, Any]]:
        """
        Get current user data from session state.
        
        Returns:
            Optional[Dict[str, Any]]: User data dict or None if not authenticated
        """
        if not SessionManager.is_authenticated():
            return None
            
        return {
            'id': st.session_state.get(SessionManager.SESSION_USER_ID),
            'username': st.session_state.get(SessionManager.SESSION_USERNAME),
            'name': st.session_state.get(SessionManager.SESSION_USER_NAME),
            'email': st.session_state.get(SessionManager.SESSION_USER_EMAIL),
            'login_time': st.session_state.get(SessionManager.SESSION_LOGIN_TIME)
        }
    
    @staticmethod
    def get_user_id() -> Optional[int]:
        """
        Get the current user's ID from session.
        
        Returns:
            Optional[int]: User ID or None if not authenticated
        """
        if not SessionManager.is_authenticated():
            return None
        return st.session_state.get(SessionManager.SESSION_USER_ID)
    
    @staticmethod
    def get_username() -> Optional[str]:
        """
        Get the current user's username from session.
        
        Returns:
            Optional[str]: Username or None if not authenticated
        """
        if not SessionManager.is_authenticated():
            return None
        return st.session_state.get(SessionManager.SESSION_USERNAME)
    
    @staticmethod
    def get_user_display_name() -> Optional[str]:
        """
        Get the current user's display name from session.
        
        Returns:
            Optional[str]: User's full name or None if not authenticated
        """
        if not SessionManager.is_authenticated():
            return None
        return st.session_state.get(SessionManager.SESSION_USER_NAME)
    
    @staticmethod
    def update_session_data(key: str, value: Any) -> None:
        """
        Update specific session data while maintaining authentication.
        
        Args:
            key (str): Session key to update
            value (Any): New value to store
        """
        if SessionManager.is_authenticated():
            st.session_state[key] = value
    
    @staticmethod
    def get_session_duration() -> Optional[float]:
        """
        Get the duration of the current session in seconds.
        
        Returns:
            Optional[float]: Session duration in seconds or None if not authenticated
        """
        if not SessionManager.is_authenticated():
            return None
        
        import time
        login_time = st.session_state.get(SessionManager.SESSION_LOGIN_TIME)
        if login_time:
            return time.time() - login_time
        return None
    
    @staticmethod
    def is_session_expired(max_duration_hours: float = 24.0) -> bool:
        """
        Check if the current session has expired.
        
        Args:
            max_duration_hours (float): Maximum session duration in hours
            
        Returns:
            bool: True if session is expired, False otherwise
        """
        if not SessionManager.is_authenticated():
            return True
        
        duration = SessionManager.get_session_duration()
        if duration is None:
            return True
        
        max_duration_seconds = max_duration_hours * 3600
        return duration > max_duration_seconds
    
    @staticmethod
    def refresh_session() -> None:
        """
        Refresh the session timestamp to extend the session.
        """
        if SessionManager.is_authenticated():
            import time
            st.session_state[SessionManager.SESSION_LOGIN_TIME] = time.time()
    
    @staticmethod
    def clear_session_except_auth() -> None:
        """
        Clear session data except authentication information.
        Useful for clearing temporary UI state while keeping user logged in.
        """
        if not SessionManager.is_authenticated():
            return
        
        # Preserve authentication data
        auth_data = SessionManager.get_current_user()
        
        # Clear all session state
        for key in list(st.session_state.keys()):
            if isinstance(key, str) and not key.startswith(('authenticated', 'user_', 'login_')):
                del st.session_state[key]