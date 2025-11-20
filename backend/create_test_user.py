"""
Script to create a test user for development
Run this after setting up the database
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User

def create_test_user():
    """Create a test user"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.srcode == "TEST001").first()
        if existing_user:
            print("Test user already exists!")
            print(f"SRCODE: TEST001")
            print(f"Password: test123")
            return
        
        # Create test user with plain password
        test_user = User(
            srcode="TEST001",
            name="Test User",
            college="IT Department",
            password="test123"
        )
        
        db.add(test_user)
        db.commit()
        print("Test user created successfully!")
        print(f"SRCODE: TEST001")
        print(f"Password: test123")
        print("\nYou can now login with these credentials.")
        
    except Exception as e:
        db.rollback()
        print(f"Error creating test user: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()

