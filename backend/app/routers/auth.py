from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, LoginRequest, LoginResponse
from app.auth import (
    authenticate_user,
    get_current_user,
    normalize_credentials,
    normalize_password,
    normalize_srcode,
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponse)
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

@router.post("/login", response_model=LoginResponse)
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

@router.get("/me", response_model=UserResponse)
def get_current_user_info(srcode: str = Query(..., description="User SRCODE"), db: Session = Depends(get_db)):
    """Get current authenticated user information"""
    user = get_current_user(srcode, db)
    return UserResponse(
        srcode=user.srcode,
        name=user.name,
        college=user.college
    )

