from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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

