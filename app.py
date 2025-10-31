import streamlit as st
import time
from modules.auth import AuthenticationManager, SessionManager

# Configure the Streamlit page
st.set_page_config(
    page_title="GYSD Streamlit App",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize authentication manager
@st.cache_resource
def get_auth_manager():
    """Get authentication manager instance"""
    return AuthenticationManager()

def show_login_page():
    """Display the login page with registration option using OOP structure"""
    auth_manager = get_auth_manager()
    
    # Initialize session state for showing registration form
    if "show_register" not in st.session_state:
        st.session_state.show_register = False
    
    st.title("🔐 Welcome to GYSD App")
    
    # Create a centered column for the forms
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if not st.session_state.show_register:
            # LOGIN FORM
            st.markdown("### Login to Your Account")
            
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                login_button = st.form_submit_button("Login", use_container_width=True)
                
                if login_button:
                    if username and password:
                        # Authenticate user using OOP approach
                        success, user_data = auth_manager.authenticate_user(username, password)
                        
                        if success and user_data:
                            # Use SessionManager to handle login
                            SessionManager.login_user(user_data)
                            st.success("Login successful! Redirecting...")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Invalid username or password")
                    else:
                        st.error("Please enter both username and password")
            
            st.markdown("---")
            
            # Register button
            st.markdown("Don't have an account?")
            if st.button("Register here", use_container_width=True, type="secondary"):
                st.session_state.show_register = True
                st.rerun()
        
        else:
            # REGISTRATION FORM
            st.markdown("### Create New Account")
            
            with st.form("register_form"):
                reg_username = st.text_input("Username", placeholder="Choose a username", key="reg_username")
                reg_name = st.text_input("Full Name", placeholder="Enter your full name", key="reg_name")
                reg_email = st.text_input("Email", placeholder="Enter your email address", key="reg_email")
                reg_password = st.text_input("Password", type="password", placeholder="Choose a password", key="reg_password")
                reg_password_confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="reg_password_confirm")
                
                register_button = st.form_submit_button("Create Account", use_container_width=True)
                
                if register_button:
                    if not all([reg_username, reg_name, reg_email, reg_password, reg_password_confirm]):
                        st.error("Please fill in all fields")
                    elif reg_password != reg_password_confirm:
                        st.error("Passwords do not match")
                    elif len(reg_password) < 6:
                        st.error("Password must be at least 6 characters long")
                    else:
                        # Register user using OOP approach
                        success, message = auth_manager.register_user(reg_username, reg_password, reg_name, reg_email)
                        
                        if success:
                            st.success(f"{message}! You can now login with your credentials.")
                            st.session_state.show_register = False
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(message)
            
            st.markdown("---")
            
            # Back to login button
            st.markdown("Already have an account?")
            if st.button("Back to Login", use_container_width=True, type="secondary"):
                st.session_state.show_register = False
                st.rerun()
        
        st.markdown("---")

def show_main_app():
    """Display the main application after successful login"""
    current_user = SessionManager.get_current_user()
    
    # Sidebar with user info and logout
    with st.sidebar:
        if current_user:
            st.success(f"Welcome, {current_user['name']}!")
            st.write(f"**Username:** {current_user['username']}")
            st.write(f"**Email:** {current_user['email']}")
        
        if st.button("Logout", type="primary"):
            SessionManager.logout_user()
            st.rerun()
    
    # Main content area
    st.title("🎉 Welcome to Your Dashboard")
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Profile", "Settings"])
    
    with tab1:
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
        import pandas as pd
        import numpy as np
        
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['Sales', 'Marketing', 'Development']
        )
        st.line_chart(chart_data)
    
    with tab2:
        st.header("User Profile")
        if current_user:
            st.write(f"**Name:** {current_user['name']}")
            st.write(f"**Username:** {current_user['username']}")
            st.write(f"**Email:** {current_user['email']}")
            st.write(f"**User ID:** {current_user['id']}")
        
        st.write("**Last Login:** Today")
        
        if st.button("Edit Profile"):
            st.info("Profile editing functionality would go here!")
    
    with tab3:
        st.header("Application Settings")
        
        # Sample settings
        dark_mode = st.checkbox("Dark Mode", value=False)
        notifications = st.checkbox("Enable Notifications", value=True)
        language = st.selectbox("Language", ["English", "Spanish", "French", "German"])
        
        if st.button("Save Settings"):
            st.success("Settings saved successfully!")

def main():
    """Main application function"""
    # Check authentication status using SessionManager
    if SessionManager.is_authenticated():
        show_main_app()
    else:
        show_login_page()

if __name__ == "__main__":
    main()