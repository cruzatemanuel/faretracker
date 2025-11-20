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

# Initialize database tables (creates all tables automatically)
# This happens automatically when you start the server, but you can also run:
python -c "from app.database import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine)"

# Start the backend server
uvicorn app.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

**Note:** The first time you run the server, it will automatically create all database tables.

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

### 4. Seed Fare Guide Data (Optional)

```bash
# Still in backend directory with venv activated
python seed_data.py
```

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
- Try recreating tables: Delete database and recreate, then restart server

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

**Users Table:**
- `srcode` (Primary Key) - String(50)
- `name` - String(255)
- `college` - String(255)
- `password` - String(255) - Plain text
- `created_at` - DateTime

**Fare Records Table:**
- `id` (Primary Key) - Integer
- `user_srcode` (Foreign Key) - String(50)
- `district` - Integer
- `start_location` - String(255)
- `destination` - String(255)
- `include_trike` - Boolean
- `total_fare` - Float
- `trike_fare` - Float
- `fare_details` - Text (JSON)
- `created_at` - DateTime

## Production Deployment Notes

Before deploying to production:
1. **IMPORTANT**: Implement proper password hashing (bcrypt)
2. **IMPORTANT**: Use JWT or session tokens for authentication
3. Update CORS origins in `backend/app/main.py`
4. Use environment variables for all sensitive data
5. Set up proper database backups
6. Use HTTPS for all connections
7. Implement rate limiting
8. Add proper error logging
9. Never store plain text passwords in production!
