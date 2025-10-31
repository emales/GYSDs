"""
Dashboard Screen

Main application dashboard with user info, metrics, and various tabs.
Displays after successful authentication.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Optional
from .base_screen import BaseScreen
from modules.auth import SessionManager


class DashboardScreen(BaseScreen):
    """
    Main dashboard screen for authenticated users.
    
    Features:
    - User information sidebar
    - Metrics overview
    - Data visualization
    - User profile management
    - Application settings
    - Logout functionality
    """
    
    def __init__(self):
        super().__init__("dashboard", "🎉 Welcome to Your Dashboard")
    
    def validate_access(self) -> bool:
        """Dashboard requires authentication."""
        return SessionManager.is_authenticated()
    
    def get_navigation_info(self) -> dict:
        """Dashboard navigation info."""
        return {
            "name": self.screen_name,
            "title": self.title,
            "requires_auth": True,
            "sidebar_visible": True
        }
    
    def render(self) -> Optional[str]:
        """Render the dashboard screen."""
        # Check if user is still authenticated
        if not SessionManager.is_authenticated():
            return "auth"
        
        # Render sidebar
        logout_requested = self._render_sidebar()
        if logout_requested:
            return "auth"
        
        # Main content area with tabs
        return self._render_main_content()
    
    def _render_sidebar(self) -> bool:
        """
        Render the sidebar with user info and logout.
        
        Returns:
            bool: True if logout was requested, False otherwise
        """
        current_user = SessionManager.get_current_user()
        
        with st.sidebar:
            if current_user:
                st.success(f"Welcome, {current_user['name']}!")
                st.write(f"**Username:** {current_user['username']}")
                st.write(f"**Email:** {current_user['email']}")
                
                # Show session info
                session_duration = SessionManager.get_session_duration()
                if session_duration:
                    hours = int(session_duration // 3600)
                    minutes = int((session_duration % 3600) // 60)
                    st.write(f"**Session:** {hours}h {minutes}m")
            
            if st.button("Logout", type="primary"):
                SessionManager.logout_user()
                st.rerun()
                return True
        
        return False
    
    def _render_main_content(self) -> Optional[str]:
        """Render the main dashboard content with tabs."""
        # Tabs for different sections
        tab1, tab2, tab3 = st.tabs(["Dashboard", "Profile", "Settings"])
        
        with tab1:
            self._render_dashboard_tab()
        
        with tab2:
            self._render_profile_tab()
        
        with tab3:
            self._render_settings_tab()
        
        return None
    
    def _render_dashboard_tab(self) -> None:
        """Render the main dashboard overview tab."""
        st.header("Dashboard Overview")
        
        # Sample metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Users", "1,234", "12%")
        
        with col2:
            st.metric("Revenue", "$45,678", "8%")
        
        with col3:
            st.metric("Orders", "567", "-2%")
        
        with col4:
            st.metric("Growth", "23%", "5%")
        
        # Sample chart
        st.subheader("Sample Data Visualization")
        
        # Generate sample data
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['Sales', 'Marketing', 'Development']
        )
        st.line_chart(chart_data)
        
        # Additional dashboard widgets
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Recent Activity")
            st.info("📊 Dashboard accessed")
            st.info("👤 Profile updated")
            st.info("⚙️ Settings changed")
        
        with col2:
            st.subheader("Quick Actions")
            if st.button("Generate Report", use_container_width=True):
                st.success("Report generated successfully!")
            
            if st.button("Export Data", use_container_width=True):
                st.info("Data export functionality would go here!")
            
            if st.button("Refresh Data", use_container_width=True):
                st.rerun()
    
    def _render_profile_tab(self) -> None:
        """Render the user profile tab."""
        st.header("User Profile")
        
        current_user = SessionManager.get_current_user()
        if current_user:
            # User information display
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Personal Information")
                st.write(f"**Name:** {current_user['name']}")
                st.write(f"**Username:** {current_user['username']}")
                st.write(f"**Email:** {current_user['email']}")
                st.write(f"**User ID:** {current_user['id']}")
                
                # Session information
                login_time = current_user.get('login_time')
                if login_time:
                    import datetime
                    login_dt = datetime.datetime.fromtimestamp(login_time)
                    st.write(f"**Last Login:** {login_dt.strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    st.write("**Last Login:** Current session")
            
            with col2:
                st.subheader("Profile Actions")
                
                if st.button("Edit Profile", use_container_width=True):
                    st.info("Profile editing functionality would go here!")
                
                if st.button("Change Password", use_container_width=True):
                    st.info("Password change functionality would go here!")
                
                if st.button("Download Profile Data", use_container_width=True):
                    st.info("Profile data download would go here!")
        
        # Profile statistics
        st.subheader("Profile Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Logins", "47", "3")
        
        with col2:
            st.metric("Sessions", "12", "1")
        
        with col3:
            st.metric("Active Days", "23", "2")
    
    def _render_settings_tab(self) -> None:
        """Render the application settings tab."""
        st.header("Application Settings")
        
        # Settings form
        with st.form("settings_form"):
            st.subheader("Preferences")
            
            # UI preferences
            dark_mode = st.checkbox("Dark Mode", value=self.get_state("dark_mode", False))
            notifications = st.checkbox("Enable Notifications", value=self.get_state("notifications", True))
            auto_refresh = st.checkbox("Auto-refresh Dashboard", value=self.get_state("auto_refresh", False))
            
            # Language selection
            language = st.selectbox(
                "Language", 
                ["English", "Spanish", "French", "German"],
                index=["English", "Spanish", "French", "German"].index(self.get_state("language", "English"))
            )
            
            # Dashboard settings
            st.subheader("Dashboard Settings")
            refresh_interval = st.slider("Refresh Interval (minutes)", 1, 60, self.get_state("refresh_interval", 5))
            items_per_page = st.number_input("Items per page", 10, 100, self.get_state("items_per_page", 20))
            
            # Save button
            save_settings = st.form_submit_button("Save Settings", use_container_width=True)
            
            if save_settings:
                # Save settings to state
                self.set_state("dark_mode", dark_mode)
                self.set_state("notifications", notifications)
                self.set_state("auto_refresh", auto_refresh)
                self.set_state("language", language)
                self.set_state("refresh_interval", refresh_interval)
                self.set_state("items_per_page", items_per_page)
                
                st.success("Settings saved successfully!")
        
        # Security settings
        st.subheader("Security Settings")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Change Password", use_container_width=True):
                st.info("Password change functionality would go here!")
        
        with col2:
            if st.button("Enable 2FA", use_container_width=True):
                st.info("Two-factor authentication setup would go here!")
        
        # Danger zone
        st.subheader("⚠️ Danger Zone")
        st.warning("These actions cannot be undone!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clear All Data", use_container_width=True, type="secondary"):
                st.error("Data clearing functionality would go here!")
        
        with col2:
            if st.button("Delete Account", use_container_width=True, type="secondary"):
                st.error("Account deletion functionality would go here!")
    
    def on_enter(self) -> None:
        """Called when entering dashboard screen."""
        # Refresh session timestamp
        SessionManager.refresh_session()
        
        # Check for session expiration
        if SessionManager.is_session_expired():
            st.warning("Your session has expired. Please log in again.")
            SessionManager.logout_user()
    
    def on_exit(self) -> None:
        """Called when leaving dashboard screen."""
        # Could log user activity, save state, etc.
        pass