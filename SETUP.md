# Quick Setup Guide

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8+ installed
- ✅ Node.js 16+ installed
- ✅ MySQL 8.0+ installed and running
- ✅ MySQL root password (or create a new user)

## Step-by-Step Setup

### 1. Database Setup

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE fairfares;

# Exit MySQL
exit;
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/fairfares
EOF

# Edit .env file with your MySQL credentials
# Replace 'your_password' with your actual MySQL password

# Create database tables manually (the application does not auto-create tables)
# Run this in MySQL:
mysql -u root -p fairfares << EOF
CREATE TABLE IF NOT EXISTS user (
    srcode VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    college VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_fares (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_srcode VARCHAR(50) NOT NULL,
    district INT NOT NULL,
    start_location VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    include_trike BOOLEAN DEFAULT FALSE,
    total_fare FLOAT NOT NULL,
    trike_fare FLOAT DEFAULT 0.0,
    fare_details TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_srcode) REFERENCES user(srcode)
);
EOF

# Start the backend server
uvicorn app:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

**Note:** Database tables must be created manually before starting the server. The application does not auto-create tables.

### 3. Create Test User (Optional)

```bash
# Make sure you're in the backend directory with venv activated
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Create test user
python create_test_user.py
```

This creates a test user:
- **SRCODE**: TEST001
- **Password**: test123
- **College**: IT Department

### 4. Fare Guide Data

The fare guide is loaded directly from `backend/data/fare_guide.csv` at runtime. No database seeding is required.

### 5. Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## First-Time Setup Summary

1. **Database**: Create `fairfares` database in MySQL
2. **Backend**: 
   - Install Python dependencies
   - Create `.env` file with database URL
   - Start server (tables auto-create)
3. **Frontend**: 
   - Install npm dependencies
   - Start dev server
4. **User Account**: 
   - Sign up through the web interface at `/signup`
   - Or create test user using `create_test_user.py`

## Testing the Application

1. Open browser to `http://localhost:5173`
2. **Sign Up** (if you don't have an account):
   - Click "Sign Up" link on login page
   - Fill in: SRCODE, Name, College, Password
   - Click "Sign Up"
   - You'll be redirected to login
3. **Login**:
   - Enter your SRCODE and password
   - Click "Login"
4. You should be redirected to the Home page
5. Navigate to "Track" to calculate fares
6. Navigate to "My Dashboard" to view your records

## Authentication System

The application uses **simplified authentication**:
- No JWT tokens or bcrypt hashing
- Simple password storage (plain text)
- Session managed via localStorage
- User identified by SRCODE (primary key)

**Signup Fields:**
- SRCODE (unique identifier)
- Name
- College
- Password

**Login Fields:**
- SRCODE
- Password

## Troubleshooting

### Backend won't start
- Check MySQL is running: `mysql -u root -p`
- Verify DATABASE_URL in `.env` file
- Check if port 8000 is available
- Ensure all tables are created (restart server if needed)

### Frontend won't start
- Check Node.js version: `node --version` (should be 16+)
- Delete `node_modules` and run `npm install` again
- Check if port 5173 is available

### Database connection errors
- Verify MySQL credentials in `.env`
- Ensure database `fairfares` exists
- Check MySQL service is running
- Verify that both `user` and `user_fares` tables exist
- Check table structure matches the schema in README.md

### CSV file not found
- Ensure `backend/data/fare_guide.csv` exists
- Check file permissions

### User authentication errors
- Make sure you've signed up first
- Check that user exists in database
- Verify SRCODE and password are correct

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database Schema

**user Table:**
- `srcode` (Primary Key) - VARCHAR(50)
- `name` - VARCHAR(255) NOT NULL
- `college` - VARCHAR(255) NOT NULL
- `password` - VARCHAR(255) NOT NULL (Plain text - no hashing)
- `created_at` - DATETIME DEFAULT CURRENT_TIMESTAMP

**user_fares Table:**
- `id` (Primary Key) - INT AUTO_INCREMENT
- `user_srcode` (Foreign Key) - VARCHAR(50) NOT NULL, REFERENCES user(srcode)
- `district` - INT NOT NULL
- `start_location` - VARCHAR(255) NOT NULL
- `destination` - VARCHAR(255) NOT NULL
- `include_trike` - BOOLEAN DEFAULT FALSE
- `total_fare` - FLOAT NOT NULL
- `trike_fare` - FLOAT DEFAULT 0.0
- `fare_details` - TEXT (JSON string)
- `created_at` - DATETIME DEFAULT CURRENT_TIMESTAMP

## Production Deployment Notes

Before deploying to production:
1. **IMPORTANT**: Implement proper password hashing (bcrypt)
2. **IMPORTANT**: Use JWT or session tokens for authentication
3. Update CORS origins in `backend/app.py`
4. Use environment variables for all sensitive data
5. Set up proper database backups
6. Use HTTPS for all connections
7. Implement rate limiting
8. Add proper error logging
9. Never store plain text passwords in production!
