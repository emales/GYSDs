# GYSD Streamlit Authentication App

A secure Streamlit web application with PostgreSQL authentication using Object-Oriented Programming principles.

## ✨ Features

- 🔐 **PostgreSQL Authentication**: Secure database-backed user authentication
- 📝 **User Registration**: Complete user registration with validation
- 🏗️ **OOP Architecture**: Clean, maintainable object-oriented design
- 🐳 **Docker Containerized**: Complete Docker setup with PostgreSQL
- 🔒 **Password Security**: bcrypt hashing with salt
- 👤 **Session Management**: Secure session state handling
- 📊 **Dashboard**: Interactive dashboard with metrics and charts
- 🔄 **Hot Reload**: Code changes reflect immediately during development

## 🚀 Quick Start

1. **Clone and setup**:
   ```bash
   git clone <your-repo>
   cd GYSDs
   cp .env.example .env
   # Edit .env with your database credentials
   ```

2. **Run with Docker**:
   ```bash
   docker compose up --build
   ```

3. **Access the app**:
   - **Streamlit App**: http://localhost:8501
   - **PostgreSQL**: localhost:5431 (for DBeaver/database tools)

4. **Login credentials**:
   - Username: `admin` | Password: `admin123`
   - Username: `user1` | Password: `user123`
   
5. **Register new users**:
   - Click "Register here" on the login page
   - Fill out the registration form
   - New users can immediately login

## 🏗️ Architecture

### **OOP Classes** (`utils.py`):
- **`DBConn`**: Handles PostgreSQL connections and queries with connection pooling
- **`AuthenticationManager`**: Manages user authentication, registration, and password hashing
- **`SessionManager`**: Handles Streamlit session state management

### **Main Application** (`app.py`):
- Login and registration forms with validation
- Interactive dashboard with metrics and charts
- Clean separation of authentication and main app views
- Uses OOP classes for all authentication logic

## 📁 Project Structure

```
GYSDs/
├── app.py                 # Main Streamlit application
├── utils.py               # OOP classes for auth and database
├── docker-compose.yml     # Docker services configuration
├── Dockerfile             # Streamlit app container
├── init.sql               # PostgreSQL database initialization
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from .env.example)
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🔧 Development

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
- Tables are automatically created via `init.sql`

### **Hot Reload Development**:
- Volume mounts enable live code editing
- Changes to `app.py` and `utils.py` auto-reload
- No container rebuild needed during development

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

### **Add New Pages**:
1. Create new functions in `app.py`
2. Add tabs or navigation in `show_main_app()`

### **Add Database Tables**:
1. Add SQL to `init.sql`
2. Create methods in `DatabaseManager` class

### **Add Authentication Features**:
1. Extend `AuthenticationManager` class
2. Update `SessionManager` for new session data

## 📊 Example Usage

```python
# Authentication and Registration
from utils import AuthenticationManager, SessionManager

auth_manager = AuthenticationManager()

# Register new user
success, message = auth_manager.register_user(username, password, name, email)

# Authenticate existing user
success, user_data = auth_manager.authenticate_user(username, password)

if success:
    SessionManager.login_user(user_data)
    
# Check if user is logged in
if SessionManager.is_authenticated():
    current_user = SessionManager.get_current_user()
    print(f"Welcome {current_user['name']}")
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