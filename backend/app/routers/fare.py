from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import List
import json

from app.database import get_db
from app.models import User, FareRecord
from app.schemas import (
    FareCalculationRequest, 
    FareCalculationResponse, 
    FareSaveRequest,
    FareRecordResponse,
    WeeklyAverageResponse,
    FareSegment
)
from app.auth import get_current_user
from app.fare_calculator import get_fare_calculator

router = APIRouter(prefix="/fare", tags=["fare"])

@router.post("/calculate", response_model=FareCalculationResponse)
def calculate_fare(
    request: FareCalculationRequest,
    srcode: str = Query(..., description="User SRCODE for authentication"),
    db: Session = Depends(get_db)
):
    """Calculate fare based on route parameters"""
    # Verify user is authenticated
    get_current_user(srcode, db)
    
    try:
        calculator = get_fare_calculator()
        result = calculator.calculate_fare(
            district=request.district,
            start_location=request.start_location,
            destination=request.destination,
            include_trike=request.include_trike
        )
        
        return FareCalculationResponse(
            segments=[FareSegment(**seg) for seg in result['segments']],
            trike_fare=result['trike_fare'],
            total_fare=result['total_fare']
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/save")
def save_fare_record(
    request: FareSaveRequest,
    srcode: str = Query(..., description="User SRCODE for authentication"),
    db: Session = Depends(get_db)
):
    """Save a fare calculation record for the current user"""
    # Verify user is authenticated
    get_current_user(srcode, db)
    
    fare_record = FareRecord(
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
    
    return {"message": "Data saved successfully!", "id": fare_record.id}

@router.get("/user-history", response_model=List[FareRecordResponse])
def get_user_history(
    srcode: str = Query(..., description="User SRCODE for authentication"),
    db: Session = Depends(get_db)
):
    """Get all fare records for the current user"""
    # Verify user is authenticated
    get_current_user(srcode, db)
    
    records = db.query(FareRecord).filter(
        FareRecord.user_srcode == srcode
    ).order_by(FareRecord.created_at.desc()).all()
    
    return records

@router.delete("/delete/{record_id}")
def delete_fare_record(
    record_id: int,
    srcode: str = Query(..., description="User SRCODE for authentication"),
    db: Session = Depends(get_db)
):
    """Delete a specific fare record"""
    # Verify user is authenticated
    get_current_user(srcode, db)
    
    record = db.query(FareRecord).filter(
        and_(
            FareRecord.id == record_id,
            FareRecord.user_srcode == srcode
        )
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fare record not found"
        )
    
    db.delete(record)
    db.commit()
    
    return {"message": "Record deleted successfully"}

@router.get("/weekly-average", response_model=WeeklyAverageResponse)
def get_weekly_average(
    srcode: str = Query(..., description="User SRCODE for authentication"),
    db: Session = Depends(get_db)
):
    """Calculate weekly average fare for the current user"""
    # Verify user is authenticated
    get_current_user(srcode, db)
    
    # Get records from the last 7 days
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    records = db.query(FareRecord).filter(
        and_(
            FareRecord.user_srcode == srcode,
            FareRecord.created_at >= week_ago
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

