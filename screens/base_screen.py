"""
Base Screen Class

Abstract base class that defines the interface for all screens in the application.
Provides common functionality and ensures consistent screen behavior.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import streamlit as st


class BaseScreen(ABC):
    """
    Abstract base class for all application screens.
    
    Provides:
    - Common screen interface
    - Screen lifecycle management
    - State management helpers
    - Navigation hooks
    """
    
    def __init__(self, screen_name: str, title: Optional[str] = None):
        """
        Initialize screen with basic properties.
        
        Args:
            screen_name (str): Unique identifier for this screen
            title (str): Display title for the screen
        """
        self.screen_name = screen_name
        self.title = title or screen_name.replace('_', ' ').title()
        self.state_key = f"screen_{screen_name}_state"
    
    @abstractmethod
    def render(self) -> Optional[str]:
        """
        Render the screen content.
        
        This method must be implemented by all screen subclasses.
        It should render the screen's UI and handle user interactions.
        
        Returns:
            Optional[str]: Next screen to navigate to, or None to stay on current screen
        """
        pass
    
    def on_enter(self) -> None:
        """
        Called when the screen is first displayed.
        Override this method to perform initialization tasks.
        """
        pass
    
    def on_exit(self) -> None:
        """
        Called when leaving this screen.
        Override this method to perform cleanup tasks.
        """
        pass
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """
        Get screen-specific state value.
        
        Args:
            key (str): State key
            default (Any): Default value if key doesn't exist
            
        Returns:
            Any: State value
        """
        screen_state = st.session_state.get(self.state_key, {})
        return screen_state.get(key, default)
    
    def set_state(self, key: str, value: Any) -> None:
        """
        Set screen-specific state value.
        
        Args:
            key (str): State key
            value (Any): Value to store
        """
        if self.state_key not in st.session_state:
            st.session_state[self.state_key] = {}
        st.session_state[self.state_key][key] = value
    
    def clear_state(self) -> None:
        """Clear all screen-specific state."""
        if self.state_key in st.session_state:
            del st.session_state[self.state_key]
    
    def show_error(self, message: str) -> None:
        """
        Display an error message.
        
        Args:
            message (str): Error message to display
        """
        st.error(message)
    
    def show_success(self, message: str) -> None:
        """
        Display a success message.
        
        Args:
            message (str): Success message to display
        """
        st.success(message)
    
    def show_info(self, message: str) -> None:
        """
        Display an info message.
        
        Args:
            message (str): Info message to display
        """
        st.info(message)
    
    def show_warning(self, message: str) -> None:
        """
        Display a warning message.
        
        Args:
            message (str): Warning message to display
        """
        st.warning(message)
    
    def create_columns(self, ratios: Optional[list] = None) -> list:
        """
        Create columns with specified ratios.
        
        Args:
            ratios (list): Column width ratios
            
        Returns:
            tuple: Column objects
        """
        if ratios is None:
            ratios = [1, 2, 1]  # Default: centered layout
        return st.columns(ratios)
    
    def render_header(self) -> None:
        """Render the screen header with title."""
        if self.title:
            st.title(self.title)
    
    def render_footer(self) -> None:
        """Render the screen footer. Override to add custom footer content."""
        pass
    
    def validate_access(self) -> bool:
        """
        Validate if user has access to this screen.
        Override this method to implement access control.
        
        Returns:
            bool: True if user has access, False otherwise
        """
        return True
    
    def get_navigation_info(self) -> Dict[str, Any]:
        """
        Get navigation information for this screen.
        
        Returns:
            Dict[str, Any]: Navigation metadata
        """
        return {
            "name": self.screen_name,
            "title": self.title,
            "requires_auth": False,
            "sidebar_visible": True
        }
    
    def render_with_lifecycle(self) -> Optional[str]:
        """
        Render screen with full lifecycle management.
        
        This method handles the complete screen lifecycle:
        1. Access validation
        2. on_enter hook
        3. Header rendering
        4. Main content rendering
        5. Footer rendering
        6. on_exit hook (if navigating away)
        
        Returns:
            Optional[str]: Next screen to navigate to
        """
        # Validate access
        if not self.validate_access():
            st.error("Access denied to this screen")
            return "auth"
        
        # Call enter hook
        self.on_enter()
        
        # Render header
        self.render_header()
        
        # Render main content
        next_screen = self.render()
        
        # Render footer
        self.render_footer()
        
        # If navigating away, call exit hook
        if next_screen and next_screen != self.screen_name:
            self.on_exit()
        
        return next_screen