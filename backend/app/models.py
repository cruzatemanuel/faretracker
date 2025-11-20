from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    srcode = Column(String(50), primary_key=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    college = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    fare_records = relationship("FareRecord", back_populates="user")

class Route(Base):
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    district = Column(Integer, nullable=False)
    start_location = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    
    segments = relationship("Segment", back_populates="route", cascade="all, delete-orphan")

class Segment(Base):
    __tablename__ = "segments"
    
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    vehicle = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    fare = Column(Float, nullable=False)
    order = Column(Integer, nullable=False)
    
    route = relationship("Route", back_populates="segments")

class FareRecord(Base):
    __tablename__ = "fare_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_srcode = Column(String(50), ForeignKey("users.srcode"), nullable=False)
    district = Column(Integer, nullable=False)
    start_location = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    include_trike = Column(Boolean, default=False)
    total_fare = Column(Float, nullable=False)
    trike_fare = Column(Float, default=0.0)
    fare_details = Column(Text, nullable=True)  # JSON string of fare segments
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="fare_records")

