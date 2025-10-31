"""
GYSD Streamlit Application

Main application entry point using screen-based architecture.
All UI logic is organized into screens managed by ScreenManager.
"""

import streamlit as st
from screens import ScreenManager


def configure_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="GYSD Streamlit App",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="expanded"
    )


@st.cache_resource
def get_screen_manager():
    """
    Get screen manager instance.
    
    Returns:
        ScreenManager: Cached screen manager instance
    """
    return ScreenManager()


def main():
    """Main application function with screen-based navigation."""
    # Configure page
    configure_page()
    
    # Get screen manager
    screen_manager = get_screen_manager()
    
    # Add debug info in development
    # if st.secrets.get("environment", "production") == "development":
    screen_manager.debug_info()
    
    # Render current screen
    screen_manager.render_current_screen()


if __name__ == "__main__":
    main()