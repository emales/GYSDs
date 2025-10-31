"""
Screen Manager

Manages screen navigation and lifecycle for the GYSD Streamlit application.
Provides centralized control over screen transitions and state management.
"""

import streamlit as st
from typing import Dict, Optional, Type
from .base_screen import BaseScreen
from .auth_screen import AuthScreen
from .dashboard_screen import DashboardScreen
from modules.auth import SessionManager


class ScreenManager:
    """
    Manages screen navigation and lifecycle.
    
    Features:
    - Screen registration and routing
    - Navigation between screens
    - Screen lifecycle management
    - Authentication-based routing
    - Session state management
    """
    
    def __init__(self):
        """Initialize screen manager with available screens."""
        self.screens: Dict[str, BaseScreen] = {}
        self.current_screen: Optional[str] = None
        self.default_screen = "auth"
        
        # Register available screens
        self._register_screens()
    
    def _register_screens(self) -> None:
        """Register all available screens."""
        self.screens = {
            "auth": AuthScreen(),
            "dashboard": DashboardScreen(),
        }
    
    def add_screen(self, screen: BaseScreen) -> None:
        """
        Add a new screen to the manager.
        
        Args:
            screen (BaseScreen): Screen instance to add
        """
        self.screens[screen.screen_name] = screen
    
    def get_current_screen_name(self) -> str:
        """
        Get the current screen name from session state.
        
        Returns:
            str: Current screen name or default screen
        """
        return st.session_state.get("current_screen", self.default_screen)
    
    def set_current_screen(self, screen_name: str) -> None:
        """
        Set the current screen in session state.
        
        Args:
            screen_name (str): Name of screen to set as current
        """
        if screen_name in self.screens:
            st.session_state["current_screen"] = screen_name
            self.current_screen = screen_name
    
    def navigate_to(self, screen_name: str) -> None:
        """
        Navigate to a specific screen.
        
        Args:
            screen_name (str): Name of screen to navigate to
        """
        if screen_name in self.screens:
            # Call exit hook for current screen
            current_screen_name = self.get_current_screen_name()
            if current_screen_name in self.screens:
                self.screens[current_screen_name].on_exit()
            
            # Set new screen
            self.set_current_screen(screen_name)
            
            # Trigger rerun to show new screen
            st.rerun()
        else:
            st.error(f"Screen '{screen_name}' not found")
    
    def get_screen(self, screen_name: str) -> Optional[BaseScreen]:
        """
        Get a screen instance by name.
        
        Args:
            screen_name (str): Name of screen to get
            
        Returns:
            Optional[BaseScreen]: Screen instance or None if not found
        """
        return self.screens.get(screen_name)
    
    def render_current_screen(self) -> None:
        """Render the current screen with full lifecycle management."""
        # Determine current screen
        current_screen_name = self.get_current_screen_name()
        
        # Validate authentication-based routing
        current_screen_name = self._validate_screen_access(current_screen_name)
        
        # Get screen instance
        screen = self.get_screen(current_screen_name)
        if not screen:
            st.error(f"Screen '{current_screen_name}' not found")
            return
        
        # Configure page based on screen settings
        self._configure_page_for_screen(screen)
        
        # Render screen with lifecycle
        next_screen = screen.render_with_lifecycle()
        
        # Handle navigation
        if next_screen and next_screen != current_screen_name:
            self.navigate_to(next_screen)
    
    def _validate_screen_access(self, requested_screen: str) -> str:
        """
        Validate access to requested screen based on authentication.
        
        Args:
            requested_screen (str): Requested screen name
            
        Returns:
            str: Validated screen name (may redirect to auth if access denied)
        """
        screen = self.get_screen(requested_screen)
        if not screen:
            return self.default_screen
        
        nav_info = screen.get_navigation_info()
        requires_auth = nav_info.get("requires_auth", False)
        
        # Check authentication requirement
        if requires_auth and not SessionManager.is_authenticated():
            return "auth"
        
        # Check if authenticated user is trying to access auth screen
        if requested_screen == "auth" and SessionManager.is_authenticated():
            return "dashboard"
        
        return requested_screen
    
    def _configure_page_for_screen(self, screen: BaseScreen) -> None:
        """
        Configure Streamlit page settings based on screen requirements.
        
        Args:
            screen (BaseScreen): Screen to configure for
        """
        nav_info = screen.get_navigation_info()
        
        # Configure sidebar visibility
        if not nav_info.get("sidebar_visible", True):
            # Hide sidebar for screens like auth
            st.markdown(
                """
                <style>
                .css-1d391kg {display: none !important;}
                .css-1lcbmhc {margin-left: 0 !important;}
                </style>
                """,
                unsafe_allow_html=True
            )
    
    def get_available_screens(self) -> Dict[str, dict]:
        """
        Get information about all available screens.
        
        Returns:
            Dict[str, dict]: Screen names mapped to their navigation info
        """
        return {
            name: screen.get_navigation_info() 
            for name, screen in self.screens.items()
        }
    
    def clear_screen_states(self) -> None:
        """Clear all screen-specific states."""
        for screen in self.screens.values():
            screen.clear_state()
    
    def get_navigation_history(self) -> list:
        """
        Get navigation history from session state.
        
        Returns:
            list: List of previously visited screens
        """
        return st.session_state.get("navigation_history", [])
    
    def add_to_navigation_history(self, screen_name: str) -> None:
        """
        Add screen to navigation history.
        
        Args:
            screen_name (str): Screen name to add to history
        """
        history = self.get_navigation_history()
        if not history or history[-1] != screen_name:
            history.append(screen_name)
            # Keep only last 10 screens in history
            st.session_state["navigation_history"] = history[-10:]
    
    def go_back(self) -> None:
        """Navigate to previous screen in history."""
        history = self.get_navigation_history()
        if len(history) > 1:
            # Remove current screen and go to previous
            history.pop()
            previous_screen = history[-1]
            self.navigate_to(previous_screen)
    
    def reset_navigation(self) -> None:
        """Reset navigation to default screen and clear history."""
        self.clear_screen_states()
        if "navigation_history" in st.session_state:
            del st.session_state["navigation_history"]
        if "current_screen" in st.session_state:
            del st.session_state["current_screen"]
        st.rerun()
    
    def debug_info(self) -> None:
        """Display debug information about current screen state."""
        if st.sidebar.checkbox("Show Debug Info"):
            with st.sidebar.expander("Screen Debug Info"):
                st.write(f"**Current Screen:** {self.get_current_screen_name()}")
                st.write(f"**Authenticated:** {SessionManager.is_authenticated()}")
                st.write(f"**Available Screens:** {list(self.screens.keys())}")
                st.write(f"**Navigation History:** {self.get_navigation_history()}")
                
                current_user = SessionManager.get_current_user()
                if current_user:
                    st.write(f"**Current User:** {current_user.get('username', 'Unknown')}")
                
                if st.button("Reset Navigation"):
                    self.reset_navigation()