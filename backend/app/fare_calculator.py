import pandas as pd
import os
from typing import List, Optional, Dict
from app.schemas import FareSegment

class FareCalculator:
    def __init__(self, csv_path: str = None):
        if csv_path is None:
            # Default to data directory relative to backend folder
            import os
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            csv_path = os.path.join(backend_dir, "data", "fare_guide.csv")
        self.csv_path = csv_path
        self.fare_guide = None
        self.load_fare_guide()

    def load_fare_guide(self):
        """Load fare guide from CSV file"""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Fare guide CSV not found at {self.csv_path}")
        
        self.fare_guide = pd.read_csv(self.csv_path)
        # Ensure columns are properly named
        required_columns = ['District', 'Start Location', 'Destination', 'Vehicle', 'Description', 'Fare']
        if not all(col in self.fare_guide.columns for col in required_columns):
            raise ValueError(f"CSV must contain columns: {required_columns}")
    
    def is_valid_location(self, location: str, district: int) -> bool:
        """Check if location is valid for the given district"""
        if self.fare_guide is None:
            return False
        
        district_data = self.fare_guide[self.fare_guide['District'] == district]
        valid_locations = set(district_data['Start Location'].unique()) | set(district_data['Destination'].unique())
        return location.upper() in [loc.upper() for loc in valid_locations]
    
    def find_route_path(self, district_data, start: str, end: str, visited=None, path=None, max_depth=10):
        """
        Recursive function to find a path from start to end using DFS
        Returns list of segment indices that form the path, or None if no path found
        """
        if visited is None:
            visited = set()
        if path is None:
            path = []
        
        # Prevent infinite recursion
        if len(path) > max_depth:
            return None
        
        if start == end:
            return path
        
        visited.add(start)
        
        # Try forward segments
        forward_segments = district_data[
            (district_data['Start Location'].str.upper() == start) &
            (~district_data['Destination'].str.upper().isin(visited))
        ]
        
        for idx, segment in forward_segments.iterrows():
            next_loc = segment['Destination'].upper()
            new_path = path + [idx]
            result = self.find_route_path(district_data, next_loc, end, visited.copy(), new_path, max_depth)
            if result is not None:
                return result
        
        # Try reverse segments
        reverse_segments = district_data[
            (district_data['Destination'].str.upper() == start) &
            (~district_data['Start Location'].str.upper().isin(visited))
        ]
        
        for idx, segment in reverse_segments.iterrows():
            next_loc = segment['Start Location'].upper()
            new_path = path + [idx]
            result = self.find_route_path(district_data, next_loc, end, visited.copy(), new_path, max_depth)
            if result is not None:
                return result
        
        return None
    
    def calculate_fare(self, district: int, start_location: str, destination: Optional[str] = None, include_trike: bool = False) -> Dict:
        """
        Calculate fare based on route segments
        Handles multi-segment routes by finding connecting paths
        """
        if self.fare_guide is None:
            raise ValueError("Fare guide not loaded")
        
        # Auto-set destination to BSU if not provided or if start is BSU
        if destination is None or start_location.upper() == "BSU":
            destination = "BSU"
        
        # Normalize locations - strip whitespace
        start_location = start_location.strip().upper()
        destination = destination.strip().upper()
        
        # Filter fare guide for the district
        district_data = self.fare_guide[self.fare_guide['District'] == district].copy()
        
        if district_data.empty:
            raise ValueError(f"No routes found for district {district}")
        
        # Normalize location names in the dataframe
        district_data['Start Location'] = district_data['Start Location'].str.strip().str.upper()
        district_data['Destination'] = district_data['Destination'].str.strip().str.upper()
        
        # Get all valid locations for better error messages
        valid_locations = set(district_data['Start Location'].unique()) | set(district_data['Destination'].unique())
        
        # Validate locations with better error messages
        if start_location not in valid_locations:
            available = sorted(list(valid_locations))
            raise ValueError(f"Invalid start location '{start_location}' for district {district}. Available locations: {', '.join(available)}")
        if destination not in valid_locations:
            available = sorted(list(valid_locations))
            raise ValueError(f"Invalid destination '{destination}' for district {district}. Available locations: {', '.join(available)}")
        
        # Reset index to use as segment identifiers
        district_data = district_data.reset_index(drop=True)
        
        # Find path from start to destination
        path_indices = self.find_route_path(district_data, start_location, destination)
        
        if path_indices is None:
            raise ValueError(f"No route found from {start_location} to {destination} in district {district}. Please check if these locations are connected.")
        
        # Build segments list from path
        segments = []
        total_fare = 0.0
        current_location = start_location
        
        for idx in path_indices:
            segment = district_data.iloc[idx]
            
            # Determine if segment is forward or reverse
            if segment['Start Location'].upper() == current_location:
                # Forward direction
                segments.append({
                    'vehicle': str(segment['Vehicle']),
                    'description': str(segment['Description']),
                    'fare': float(segment['Fare'])
                })
                total_fare += float(segment['Fare'])
                current_location = segment['Destination'].upper()
            else:
                # Reverse direction - need to reverse the description
                desc = str(segment['Description'])
                # Try to reverse the description (e.g., "A to B" becomes "B to A")
                parts = desc.split(' to ')
                if len(parts) == 2:
                    reversed_desc = f"{parts[1]} to {parts[0]}"
                else:
                    reversed_desc = desc
                
                segments.append({
                    'vehicle': str(segment['Vehicle']),
                    'description': reversed_desc,
                    'fare': float(segment['Fare'])
                })
                total_fare += float(segment['Fare'])
                current_location = segment['Start Location'].upper()
        
        # Calculate trike fare if applicable
        trike_fare = 0.0
        if include_trike:
            # Trike fare is typically a fixed amount or based on distance
            # For now, using a simple calculation: 10% of total fare or minimum 5.0
            trike_fare = max(5.0, total_fare * 0.1)
            total_fare += trike_fare
        
        return {
            'segments': segments,
            'trike_fare': trike_fare,
            'total_fare': total_fare
        }

# Global instance
fare_calculator = None

def get_fare_calculator():
    global fare_calculator
    if fare_calculator is None:
        fare_calculator = FareCalculator()
    return fare_calculator

