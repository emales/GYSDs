# GYSD Streamlit Authentication App

A secure Streamlit web application with PostgreSQL authentication using modern screen-based architecture.

## ✨ Features

- 🔐 **PostgreSQL Authentication**: Secure database-backed user authentication
- 📝 **User Registration**: Complete user registration with validation
- 🏗️ **Modular Architecture**: Clean separation between backend modules and frontend screens
- 🐳 **Docker Containerized**: Complete Docker setup with PostgreSQL
- 🔒 **Password Security**: bcrypt hashing with salt
- 👤 **Session Management**: Secure session state handling
- 📊 **Dashboard**: Interactive dashboard with metrics and charts
- 🔄 **Hot Reload**: Code changes reflect immediately during development
- 🎯 **Screen-based Navigation**: Each screen manages its own UI logic

## 🚀 Quick Start

### Option 1: Run with Docker (Recommended)
```bash
# Start the application
docker compose up --build -d

# View logs
docker compose logs streamlit

# Stop the application
docker compose down
```

The app will be available at: http://localhost:8501

### Option 2: Debug with VS Code
1. Press `F5` or go to Run & Debug in VS Code
2. Select "Debug Streamlit in Docker"
3. Set breakpoints in your code
4. The debugger will attach automatically

### Option 3: Local Development (requires local Python setup)
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DB_HOST=localhost
export POSTGRES_DB=GYSD_streamlit
export POSTGRES_USER=admin
export POSTGRES_PASSWORD=admin123
export DB_PORT=5431

# Run the app
streamlit run app.py
```

## 🏗️ Architecture

### **Backend Modules** (`modules/`):
- **`auth/login.py`**: `AuthenticationManager` class for password hashing and user authentication
- **`auth/session.py`**: `SessionManager` class for Streamlit session state management  
- **`database/connection.py`**: `DatabaseConnection` class with connection pooling and queries

### **Frontend Screens** (`screens/`):
- **`base_screen.py`**: Abstract `BaseScreen` class with lifecycle management
- **`auth_screen.py`**: `AuthScreen` class for login/registration UI
- **`dashboard_screen.py`**: `DashboardScreen` class for main app UI
- **`screen_manager.py`**: `ScreenManager` class for navigation control

### **Main Application** (`app.py`):
- Minimal entry point using screen manager
- All UI logic delegated to screen classes
- Clean navigation between authentication and dashboard

## 📁 Project Structure

```
GYSDs/
├── app.py                     # Main entry point (minimal, uses screen manager)
├── modules/                   # Backend logic
│   ├── auth/                  # Authentication modules
│   │   ├── login.py          # AuthenticationManager class
│   │   └── session.py        # SessionManager class
│   └── database/              # Database modules
│       └── connection.py     # DatabaseConnection class
├── screens/                   # Frontend UI screens
│   ├── base_screen.py        # Abstract BaseScreen class
│   ├── auth_screen.py        # Login/registration UI
│   ├── dashboard_screen.py   # Main dashboard UI
│   ├── screen_manager.py     # Navigation controller
│   └── components/           # Reusable UI components (optional)
├── docker-compose.yml        # Production Docker setup
├── docker-compose.debug.yml  # Debug Docker setup
├── Dockerfile                # Production container
├── Dockerfile.debug          # Debug container with debugpy
├── .vscode/                  # VS Code debug configuration
├── sql/init.sql              # PostgreSQL database initialization
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create from .env.example)
└── README.md                 # This file
```

## 🎯 Key Features

- **Clean Architecture**: Backend modules separated from frontend screens
- **Screen-based Navigation**: Each screen manages its own logic
- **Authentication**: Secure login with bcrypt password hashing
- **Database Integration**: PostgreSQL with connection pooling
- **Docker Support**: Full containerization with debug capabilities
- **Hot Reload**: File changes trigger automatic updates
- **Modular Design**: Easy to extend with new screens and features

## 🔧 Development

### **Adding New Screens**:
```python
from screens.base_screen import BaseScreen

class MyNewScreen(BaseScreen):
    def __init__(self):
        super().__init__("my_screen", "My Screen")
    
    def render_content(self):
        st.title("My New Screen")
        # Your screen logic here
        
    def get_navigation_info(self):
        return {
            "title": "My Screen",
            "icon": "🎯",
            "requires_auth": True,
            "sidebar_visible": True
        }

# Register in screen_manager.py
self.screens["my_screen"] = MyNewScreen()
```

### **Local Development**:
```bash
# Install dependencies
pip install -r requirements.txt

# Set up PostgreSQL locally or use Docker for just the database:
docker-compose up postgres -d

# Run Streamlit
streamlit run app.py
```

### **Database Management**:
- Use DBeaver or any PostgreSQL client
- Connect to `localhost:5431` with credentials from `.env`
- Database: `GYSD_streamlit`
- Tables are automatically created via `sql/init.sql`

## 🐳 Docker Services

- **`postgres`**: PostgreSQL 15-alpine running on port 5431 (both internal and external)
- **`streamlit`**: Python app with hot reload capability and health checks

## 🔒 Security Features

- Environment variables for database credentials
- bcrypt password hashing with salt for all passwords
- SQL injection protection with parameterized queries
- Session state management with user data isolation
- Connection pooling for database efficiency
- User registration with password confirmation and validation

## 🛠️ Extending the App

### **Add New Screens**:
1. Create new class inheriting from `BaseScreen`
2. Implement `render_content()` and `get_navigation_info()`
3. Register in `ScreenManager._register_screens()`

### **Add Database Features**:
1. Add methods to `DatabaseConnection` class
2. Update SQL in `sql/init.sql` if needed
3. Use in screen classes via dependency injection

### **Add Authentication Features**:
1. Extend `AuthenticationManager` class
2. Update `SessionManager` for new session data
3. Modify screen access requirements

## 📊 Example Usage

```python
# Using the modular architecture
from modules.auth import AuthenticationManager, SessionManager
from modules.database import DatabaseConnection

# Authentication
auth_manager = AuthenticationManager()
success, user_data = auth_manager.authenticate_user(username, password)

if success:
    SessionManager.login_user(user_data)

# Database operations
with DatabaseConnection().get_db_connection() as conn:
    # Your database queries here
    pass

# Screen navigation
from screens import ScreenManager
screen_manager = ScreenManager()
screen_manager.navigate_to("dashboard")
```

## 🐛 Troubleshooting

### **Database Connection Issues**:
```bash
# Check if containers are running
docker compose ps

# View logs
docker compose logs postgres
docker compose logs streamlit

# Restart containers
docker compose restart
```

### **Environment Variables**:
- Ensure `.env` file exists and has correct values
- Default ports: PostgreSQL=5431, Streamlit=8501
- Restart containers after changing `.env`: `docker compose restart`

### **Hot Reload Issues**:
- If changes don't appear, press `R` in browser to reload
- Check volume mounts in `docker-compose.yml`
- Rebuild if Dockerfile changes: `docker compose up --build`

## 📝 License

MIT License - feel free to use for your projects!

---

Built with ❤️ using Streamlit, PostgreSQL, and Docker