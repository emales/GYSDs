# GYSD Streamlit Authentication App

A secure Streamlit web application with PostgreSQL authentication using Object-Oriented Programming principles.

## ✨ Features

- 🔐 **PostgreSQL Authentication**: Secure database-backed user authentication
- 🏗️ **OOP Architecture**: Clean, maintainable object-oriented design
- 🐳 **Docker Containerized**: Complete Docker setup with PostgreSQL
- 🔒 **Password Security**: bcrypt hashing with salt
- 👤 **Session Management**: Secure session state handling
- 📊 **Dashboard**: Sample interactive dashboard with metrics

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
   docker-compose up --build
   ```

3. **Access the app**:
   - **Streamlit App**: http://localhost:8501
   - **PostgreSQL**: localhost:5432 (for DBeaver/database tools)

4. **Login credentials**:
   - Username: `admin` | Password: `admin123`
   - Username: `user1` | Password: `user123`

## 🏗️ Architecture

### **OOP Classes** (`utils.py`):
- **`DatabaseManager`**: Handles PostgreSQL connections and queries
- **`AuthenticationManager`**: Manages user authentication and password hashing
- **`SessionManager`**: Handles Streamlit session state

### **Main Application** (`app.py`):
- Clean separation of login and dashboard views
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
- Connect to `localhost:5432` with credentials from `.env`
- Tables are automatically created via `init.sql`

## 🐳 Docker Services

- **`postgres`**: PostgreSQL 15 with automatic schema initialization
- **`streamlit`**: Python app with all dependencies

## 🔒 Security Features

- Environment variables for database credentials
- bcrypt password hashing with salt
- SQL injection protection with parameterized queries
- Session state management
- Connection pooling for database efficiency

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
# In your app code
from utils import AuthenticationManager, SessionManager

# Authenticate user
auth_manager = AuthenticationManager()
success, user_data = auth_manager.authenticate_user(username, password)

if success:
    SessionManager.login_user(user_data)
    
# Check if user is logged in
if SessionManager.is_authenticated():
    current_user = SessionManager.get_current_user()
```

## 🐛 Troubleshooting

### **Database Connection Issues**:
```bash
# Check if containers are running
docker-compose ps

# View logs
docker-compose logs postgres
docker-compose logs streamlit
```

### **Environment Variables**:
- Ensure `.env` file exists and has correct values
- Restart containers after changing `.env`: `docker-compose restart`

## 📝 License

MIT License - feel free to use for your projects!

---

Built with ❤️ using Streamlit, PostgreSQL, and Docker