# Fair Fares - Fare Data Management and Analysis System

A full-stack web application for managing and analyzing transportation fare data across multiple districts.

## Tech Stack

- **Frontend**: React 18 with Vite
- **Backend**: FastAPI (Python)
- **Database**: MySQL (via SQLAlchemy)
- **Authentication**: JWT (JSON Web Tokens)

## Features

✅ User Authentication (JWT-based login system)
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
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── database.py          # Database configuration
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── auth.py              # Authentication logic
│   │   ├── fare_calculator.py   # Fare calculation logic
│   │   └── routers/
│   │       ├── auth.py          # Authentication endpoints
│   │       └── fare.py          # Fare management endpoints
│   ├── data/
│   │   └── fare_guide.csv       # Fare guide data
│   ├── requirements.txt
│   └── seed_data.py             # Database seeding script
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
   SECRET_KEY=your-secret-key-here-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Create MySQL database:**
   ```sql
   CREATE DATABASE fairfares;
   ```

6. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

7. **Seed the database (optional):**
   ```bash
   python seed_data.py
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
- `POST /auth/login` - Login and get JWT token
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

- **User**: Stores user account information (SRCODE, name, department)
- **FareRecord**: Stores fare calculation records
- **Route**: Stores route information (district, start, destination)
- **Segment**: Stores fare segments for routes

## Fare Guide CSV Format

The fare guide CSV should have the following columns:
- District
- Start Location
- Destination
- Vehicle
- Description
- Fare

## Development Notes

- The fare calculator reads from `backend/data/fare_guide.csv`
- JWT tokens are stored in localStorage on the frontend
- All API requests require authentication except `/auth/login` and `/auth/signup`
- CORS is configured to allow requests from `localhost:5173` and `localhost:3000`

## Troubleshooting

1. **Database connection errors:**
   - Verify MySQL is running
   - Check DATABASE_URL in `.env` file
   - Ensure database `fairfares` exists

2. **CSV not found:**
   - Ensure `backend/data/fare_guide.csv` exists
   - Check file path in `fare_calculator.py`

3. **CORS errors:**
   - Verify backend CORS settings in `main.py`
   - Check frontend API base URL in `services/api.js`

## License

This project is for educational purposes.

