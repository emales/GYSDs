-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create index on username for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Insert sample users with bcrypt hashed passwords
-- Password for 'admin': admin123
-- Password for 'user1': user123
INSERT INTO users (username, password_hash, name, email) VALUES 
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj38TUPwXgH6', 'Administrator', 'admin@example.com'),
('user1', '$2b$12$EHwdkMiNfTHjFwYwSNW9Bu5dJLqn.zCgK7/1lZ8lJ5sMNxF8vLFvC', 'Test User', 'user1@example.com')
ON CONFLICT (username) DO NOTHING;
