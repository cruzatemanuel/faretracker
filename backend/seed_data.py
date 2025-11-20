"""
Script to seed the database with fare guide data from CSV
Run this after creating the database tables
"""
import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Route, Segment

def load_fare_guide_to_db(csv_path: str = "data/fare_guide.csv"):
    """Load fare guide CSV into database"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(Segment).delete()
        db.query(Route).delete()
        db.commit()
        
        # Read CSV
        df = pd.read_csv(csv_path)
        
        # Group by route (district, start, destination)
        routes_created = {}
        
        for _, row in df.iterrows():
            route_key = (
                int(row['District']),
                str(row['Start Location']).upper(),
                str(row['Destination']).upper()
            )
            
            # Get or create route
            if route_key not in routes_created:
                route = Route(
                    district=route_key[0],
                    start_location=route_key[1],
                    destination=route_key[2]
                )
                db.add(route)
                db.flush()
                routes_created[route_key] = route
            else:
                route = routes_created[route_key]
            
            # Create segment
            segment = Segment(
                route_id=route.id,
                vehicle=str(row['Vehicle']),
                description=str(row['Description']),
                fare=float(row['Fare']),
                order=len([s for s in route.segments]) + 1
            )
            db.add(segment)
        
        db.commit()
        print(f"Successfully loaded {len(routes_created)} routes and {len(df)} segments")
        
    except Exception as e:
        db.rollback()
        print(f"Error loading fare guide: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    load_fare_guide_to_db()

