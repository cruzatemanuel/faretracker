# Fair Fares - Fare Data Management and Analysis System

A full-stack web application for managing and analyzing transportation fare data across multiple districts.

## Tech Stack

- **Frontend**: React 18 with Vite
- **Backend**: FastAPI (Python)
- **Database**: MySQL (via SQLAlchemy)
- **Authentication**: Simple password-based authentication

## Features

✅ User Authentication (Simple password-based login system)
✅ Home Page with navigation and about section
✅ Track Page for fare calculation and data entry
✅ Dashboard with user info, weekly averages, and fare history
✅ Fare calculation based on route segments from CSV guide
✅ Support for multiple districts (1-6)
✅ Optional trike fare calculation
✅ Fare record management (save, view, delete)

## Project Structure

```
finalproject/
├── backend/
│   ├── app.py                   # Consolidated FastAPI application (all backend logic)
│   ├── data/
│   │   └── fare_guide.csv       # Fare guide data
│   ├── requirements.txt
│   ├── create_test_user.py      # Script to create test user
│   └── seed_data.py             # (Deprecated - fare guide loaded from CSV at runtime)
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable components
│   │   ├── pages/               # Page components
│   │   ├── contexts/            # React contexts
│   │   ├── services/            # API services
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- MySQL 8.0+

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the `backend` directory:
   ```env
   DATABASE_URL=mysql+pymysql://username:password@localhost:3306/fairfares
   ```

5. **Create MySQL database and tables:**
   ```sql
   CREATE DATABASE fairfares;
   ```
   
   Then create the tables manually (the application does not auto-create tables):
   ```sql
   USE fairfares;
   
   CREATE TABLE user (
       srcode VARCHAR(50) PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       college VARCHAR(255) NOT NULL,
       password VARCHAR(255) NOT NULL,
       created_at DATETIME DEFAULT CURRENT_TIMESTAMP
   );
   
   CREATE TABLE user_fares (
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
   ```

6. **Run the application:**
   ```bash
   uvicorn app:app --reload --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### Authentication
- `POST /auth/signup` - Create a new user account
- `POST /auth/login` - Login with SRCODE and password
- `GET /auth/me` - Get current user information

### Fare Management
- `POST /fare/calculate` - Calculate fare for a route
- `POST /fare/save` - Save a fare record
- `GET /fare/user-history` - Get user's fare history
- `GET /fare/weekly-average` - Get weekly average fare
- `DELETE /fare/delete/{id}` - Delete a fare record

## Usage

1. **Sign Up / Login:**
   - Navigate to the login page
   - Enter your SRCODE and password
   - After login, you'll be redirected to the home page

2. **Calculate Fare:**
   - Go to the Track page
   - Select district, start location, and optionally include trike
   - Click "Calculate Fare" to see the breakdown
   - Click "Save Record" to save the calculation

3. **View Dashboard:**
   - Go to My Dashboard
   - View your user information
   - See weekly average fare
   - Browse and manage your fare history

## Database Models

- **user**: Stores user account information (srcode, name, college, password, created_at)
- **user_fares**: Stores fare calculation records (id, user_srcode, district, start_location, destination, include_trike, total_fare, trike_fare, fare_details, created_at)

## Fare Guide CSV Format

The fare guide CSV should have the following columns:
- District
- Start Location
- Destination
- Vehicle
- Description
- Fare

## Development Notes

- The fare calculator reads from `backend/data/fare_guide.csv` at runtime
- All backend logic is consolidated in a single `app.py` file for simplicity
- Simple password-based authentication (no JWT or bcrypt)
- All API requests require authentication via SRCODE query parameter
- CORS is configured to allow requests from `localhost:5173` and `localhost:3000`
- Database tables must be created manually - the application does not auto-create them

## Troubleshooting

1. **Database connection errors:**
   - Verify MySQL is running
   - Check DATABASE_URL in `.env` file
   - Ensure database `fairfares` exists

2. **CSV not found:**
   - Ensure `backend/data/fare_guide.csv` exists
   - Check file path in `app.py` (FareCalculator class)

3. **CORS errors:**
   - Verify backend CORS settings in `app.py`
   - Check frontend API base URL in `services/api.js`

## License

This project is for educational purposes.

