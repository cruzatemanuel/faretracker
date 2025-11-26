"""
Consolidated FastAPI application for Fair Fares API
All backend logic in a single file for simplicity
"""
from fastapi import FastAPI, Depends, HTTPException, status, Query, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, func, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from typing import List, Optional, Dict, Tuple
from datetime import datetime, timedelta
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# DATABASE SETUP
# ============================================================================
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/fairfares")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Database dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================================
# DATABASE MODELS (2 tables: user and user_fares)
# ============================================================================
class User(Base):
    __tablename__ = "user"
    
    srcode = Column(String(50), primary_key=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    college = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    fare_records = relationship("UserFares", back_populates="user")

class UserFares(Base):
    __tablename__ = "user_fares"
    
    id = Column(Integer, primary_key=True, index=True)
    user_srcode = Column(String(50), ForeignKey("user.srcode"), nullable=False)
    district = Column(Integer, nullable=False)
    start_location = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    include_trike = Column(Boolean, default=False)
    total_fare = Column(Float, nullable=False)
    trike_fare = Column(Float, default=0.0)
    fare_details = Column(Text, nullable=True)  # JSON string of fare segments
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="fare_records")

# ============================================================================
# PYDANTIC SCHEMAS
# ============================================================================
class UserCreate(BaseModel):
    srcode: str
    name: str
    college: str
    password: str

class UserResponse(BaseModel):
    srcode: str
    name: str
    college: str
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    srcode: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    user: Optional[UserResponse] = None
    message: Optional[str] = None

class FareSegment(BaseModel):
    vehicle: str
    description: str
    fare: float

class FareCalculationRequest(BaseModel):
    district: int
    start_location: str
    destination: Optional[str] = None
    include_trike: bool = False

class FareCalculationResponse(BaseModel):
    segments: List[FareSegment]
    trike_fare: float
    total_fare: float

class FareSaveRequest(BaseModel):
    district: int
    start_location: str
    destination: str
    include_trike: bool
    total_fare: float
    trike_fare: float
    fare_details: str

class FareRecordResponse(BaseModel):
    id: int
    district: int
    start_location: str
    destination: str
    include_trike: bool
    total_fare: float
    trike_fare: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class WeeklyAverageResponse(BaseModel):
    weekly_average: float
    week_start: datetime
    week_end: datetime

# ============================================================================
# AUTHENTICATION FUNCTIONS
# ============================================================================
def normalize_srcode(srcode: Optional[str]) -> str:
    """Normalize SRCODE for consistent lookups"""
    return (srcode or "").strip().upper()

def normalize_password(password: Optional[str]) -> str:
    """Normalize password input without applying hashing"""
    return (password or "").strip()

def normalize_credentials(srcode: Optional[str], password: Optional[str]) -> Tuple[str, str]:
    """Return sanitized SRCODE and password"""
    return normalize_srcode(srcode), normalize_password(password)

def get_current_user(srcode: str = None, db: Session = Depends(get_db)):
    """Get current user from session"""
    clean_srcode = normalize_srcode(srcode)
    if not clean_srcode:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user = db.query(User).filter(User.srcode == clean_srcode).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

def authenticate_user(db: Session, srcode: str, password: str):
    """Simple password authentication"""
    clean_srcode, clean_password = normalize_credentials(srcode, password)
    if not clean_srcode or not clean_password:
        return None
    
    return db.query(User).filter(
        User.srcode == clean_srcode,
        User.password == clean_password
    ).first()

# ============================================================================
# FARE CALCULATOR CLASS
# ============================================================================
class FareCalculator:
    def __init__(self, csv_path: str = None):
        if csv_path is None:
            # Default to data directory relative to backend folder
            backend_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(backend_dir, "data", "fare_guide.csv")
        self.csv_path = csv_path
        self.fare_guide = None  # Will be a dict: {district: {route_key: [segments]}}
        self.load_fare_guide()

    def load_fare_guide(self):
        """Load fare guide from text file with new format"""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Fare guide CSV not found at {self.csv_path}")
        
        self.fare_guide = {}
        current_district = None
        current_route = None
        current_route_key = None
        
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                
                # Check for district header (e.g., "district 1:")
                if line.lower().startswith('district'):
                    # Extract district number
                    parts = line.lower().replace('district', '').replace(':', '').strip()
                    try:
                        current_district = int(parts)
                        if current_district not in self.fare_guide:
                            self.fare_guide[current_district] = {}
                        current_route = None
                        current_route_key = None
                    except ValueError:
                        continue
                    continue
                
                # Check for route header (e.g., "Balayan - BSU:")
                if ' - ' in line and line.endswith(':'):
                    if current_district is None:
                        continue
                    
                    # Extract start and destination
                    route_parts = line.replace(':', '').strip().split(' - ')
                    if len(route_parts) == 2:
                        start = route_parts[0].strip().upper()
                        destination = route_parts[1].strip().upper()
                        current_route_key = (start, destination)
                        current_route = []
                        self.fare_guide[current_district][current_route_key] = current_route
                    continue
                
                # Parse route segment (e.g., "Balayan to Grand Terminal,bus,106.00")
                if current_route is not None and ',' in line:
                    parts = line.split(',')
                    if len(parts) >= 3:
                        segment_desc = parts[0].strip()
                        vehicle = parts[1].strip()
                        try:
                            fare = float(parts[2].strip())
                        except ValueError:
                            continue
                        
                        # Parse "from to" from description
                        if ' to ' in segment_desc:
                            from_to = segment_desc.split(' to ')
                            if len(from_to) == 2:
                                from_loc = from_to[0].strip()
                                to_loc = from_to[1].strip()
                                
                                current_route.append({
                                    'from': from_loc,
                                    'to': to_loc,
                                    'vehicle': vehicle,
                                    'description': segment_desc,
                                    'fare': fare
                                })
    
    def is_valid_location(self, location: str, district: int) -> bool:
        """Check if location is valid for the given district"""
        if self.fare_guide is None:
            return False
        
        if district not in self.fare_guide:
            return False
        
        location_upper = location.strip().upper()
        valid_locations = set()
        
        # Extract all locations from route keys and segments
        for route_key, segments in self.fare_guide[district].items():
            start, destination = route_key
            valid_locations.add(start)
            valid_locations.add(destination)
            for segment in segments:
                valid_locations.add(segment['from'].upper())
                valid_locations.add(segment['to'].upper())
        
        return location_upper in valid_locations
    
    def calculate_fare(self, district: int, start_location: str, destination: Optional[str] = None, include_trike: bool = False) -> Dict:
        """
        Calculate fare based on route segments using direct route lookup
        """
        if self.fare_guide is None:
            raise ValueError("Fare guide not loaded")
        
        # Normalize locations - strip whitespace and uppercase first
        start_location = start_location.strip().upper()
        
        # Auto-set destination to BSU only if not provided
        if destination is None:
            destination = "BSU"
        else:
            destination = destination.strip().upper()
        
        # Check if district exists
        if district not in self.fare_guide:
            raise ValueError(f"No routes found for district {district}")
        
        # Try to find the route
        route_key = (start_location, destination)
        route_segments = None
        
        if route_key in self.fare_guide[district]:
            route_segments = self.fare_guide[district][route_key]
        else:
            # Route not found - get all valid locations for error message
            valid_locations = set()
            for route_key_temp, segments in self.fare_guide[district].items():
                start, dest = route_key_temp
                valid_locations.add(start)
                valid_locations.add(dest)
            
            available = sorted(list(valid_locations))
            raise ValueError(f"No route found from '{start_location}' to '{destination}' in district {district}. Available locations: {', '.join(available)}")
        
        # Build segments list from route
        segments = []
        total_fare = 0.0
        
        for segment in route_segments:
            segments.append({
                'vehicle': segment['vehicle'],
                'description': segment['description'],
                'fare': segment['fare']
            })
            total_fare += segment['fare']
        
        # Calculate trike fare if applicable
        trike_fare = 0.0
        if include_trike:
            # Trike fare is typically a fixed amount or based on distance
            # For now, using a simple calculation: 10% of total fare or minimum 10.0
            trike_fare = max(10.0, total_fare * 0.1)
            total_fare += trike_fare
        
        return {
            'segments': segments,
            'trike_fare': trike_fare,
            'total_fare': total_fare
        }

# Global instance
fare_calculator = None

def get_fare_calculator():
    """Get or create global fare calculator instance"""
    global fare_calculator
    if fare_calculator is None:
        fare_calculator = FareCalculator()
    return fare_calculator

# ============================================================================
# BACKEND LOGIC FUNCTIONS (mapped to user's requested functions)
# ============================================================================
def loadFareGuide():
    """Load fare data from CSV"""
    calculator = get_fare_calculator()
    calculator.load_fare_guide()
    return calculator.fare_guide

def loadUserFares(srcode: str, db: Session):
    """Get user's fare history"""
    records = db.query(UserFares).filter(
        UserFares.user_srcode == srcode
    ).order_by(UserFares.created_at.desc()).all()
    return records

def dataEntry(request: FareCalculationRequest, srcode: str, db: Session):
    """Handle fare calculation input"""
    calculator = get_fare_calculator()
    result = calculator.calculate_fare(
        district=request.district,
        start_location=request.start_location,
        destination=request.destination,
        include_trike=request.include_trike
    )
    return result

def findRecord(srcode: str, db: Session, record_id: Optional[int] = None):
    """Search fare records"""
    if record_id:
        return db.query(UserFares).filter(
            and_(
                UserFares.id == record_id,
                UserFares.user_srcode == srcode
            )
        ).first()
    return loadUserFares(srcode, db)

def isValidLocation(location: str, district: int) -> bool:
    """Validate locations"""
    calculator = get_fare_calculator()
    return calculator.is_valid_location(location, district)

def saveRecord(request: FareSaveRequest, srcode: str, db: Session):
    """Save fare calculation"""
    fare_record = UserFares(
        user_srcode=srcode,
        district=request.district,
        start_location=request.start_location,
        destination=request.destination,
        include_trike=request.include_trike,
        total_fare=request.total_fare,
        trike_fare=request.trike_fare,
        fare_details=request.fare_details
    )
    db.add(fare_record)
    db.commit()
    db.refresh(fare_record)
    return fare_record

def calculateFare(district: int, start_location: str, destination: Optional[str] = None, include_trike: bool = False) -> Dict:
    """Calculate total fare"""
    calculator = get_fare_calculator()
    return calculator.calculate_fare(district, start_location, destination, include_trike)

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================
app = FastAPI(title="Fair Fares API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# AUTH ROUTES
# ============================================================================
@app.post("/auth/signup", response_model=UserResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user account"""
    clean_srcode = normalize_srcode(user_data.srcode)
    clean_name = user_data.name.strip()
    clean_college = user_data.college.strip()
    clean_password = normalize_password(user_data.password)

    if not clean_srcode or not clean_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SRCODE and password are required"
        )
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.srcode == clean_srcode).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SRCODE already registered"
        )
    
    # Create new user with plain password
    new_user = User(
        srcode=clean_srcode,
        name=clean_name,
        college=clean_college,
        password=clean_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.post("/auth/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return user info"""
    clean_srcode, clean_password = normalize_credentials(login_data.srcode, login_data.password)

    if not clean_srcode or not clean_password:
        return LoginResponse(
            success=False,
            message="SRCODE and password are required"
        )

    user = authenticate_user(db, clean_srcode, clean_password)
    if not user:
        return LoginResponse(
            success=False,
            message="Incorrect SRCODE or password. Please signup if you don't have an account."
        )
    
    return LoginResponse(
        success=True,
        user=UserResponse(
            srcode=user.srcode,
            name=user.name,
            college=user.college
        )
    )

@app.get("/auth/me", response_model=UserResponse)
def get_current_user_info(srcode: str = Query(..., description="User SRCODE"), db: Session = Depends(get_db)):
    """Get current authenticated user information"""
    user = get_current_user(srcode, db)
    return UserResponse(
        srcode=user.srcode,
        name=user.name,
        college=user.college
    )

# ============================================================================
# FARE ROUTES
# ============================================================================
@app.post("/fare/calculate", response_model=FareCalculationResponse)
def calculate_fare_endpoint(
    request: FareCalculationRequest,
    srcode: str = Query(..., description="User SRCODE for authentication"),
    db: Session = Depends(get_db)
):
    """Calculate fare based on route parameters"""
    # Verify user is authenticated
    get_current_user(srcode, db)
    
    try:
        result = dataEntry(request, srcode, db)
        return FareCalculationResponse(
            segments=[FareSegment(**seg) for seg in result['segments']],
            trike_fare=result['trike_fare'],
            total_fare=result['total_fare']
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/fare/save")
def save_fare_record(
    request: FareSaveRequest,
    srcode: str = Query(..., description="User SRCODE for authentication"),
    db: Session = Depends(get_db)
):
    """Save a fare calculation record for the current user"""
    # Verify user is authenticated
    get_current_user(srcode, db)
    
    fare_record = saveRecord(request, srcode, db)
    
    return {"message": "Data saved successfully!", "id": fare_record.id}

@app.get("/fare/user-history", response_model=List[FareRecordResponse])
def get_user_history(
    srcode: str = Query(..., description="User SRCODE for authentication"),
    db: Session = Depends(get_db)
):
    """Get all fare records for the current user"""
    # Verify user is authenticated
    get_current_user(srcode, db)
    
    records = loadUserFares(srcode, db)
    return records

@app.delete("/fare/delete/{record_id}")
def delete_fare_record(
    record_id: int,
    srcode: str = Query(..., description="User SRCODE for authentication"),
    db: Session = Depends(get_db)
):
    """Delete a specific fare record"""
    # Verify user is authenticated
    get_current_user(srcode, db)
    
    record = findRecord(srcode, db, record_id)
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fare record not found"
        )
    
    db.delete(record)
    db.commit()
    
    return {"message": "Record deleted successfully"}

@app.get("/fare/weekly-average", response_model=WeeklyAverageResponse)
def get_weekly_average(
    srcode: str = Query(..., description="User SRCODE for authentication"),
    db: Session = Depends(get_db)
):
    """Calculate weekly average fare for the current user"""
    # Verify user is authenticated
    get_current_user(srcode, db)
    
    # Get records from the last 7 days
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    records = db.query(UserFares).filter(
        and_(
            UserFares.user_srcode == srcode,
            UserFares.created_at >= week_ago
        )
    ).all()
    
    if not records:
        return WeeklyAverageResponse(
            weekly_average=0.0,
            week_start=week_ago,
            week_end=datetime.utcnow()
        )
    
    total_fare = sum(record.total_fare for record in records)
    average = total_fare / len(records)
    
    return WeeklyAverageResponse(
        weekly_average=round(average, 2),
        week_start=week_ago,
        week_end=datetime.utcnow()
    )

# ============================================================================
# ROOT ROUTES
# ============================================================================
@app.get("/")
def root():
    return {"message": "Fair Fares API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

