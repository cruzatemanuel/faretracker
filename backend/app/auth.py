from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Tuple
from app.database import get_db
from app.models import User

# Simple session storage (in-memory)
# In production, you might want to use Redis or database sessions
active_sessions = {}

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
