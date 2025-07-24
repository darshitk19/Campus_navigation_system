import math
from geopy.distance import geodesic

class RouteCalculator:
    def __init__(self, path_loader):
        self.path_loader = path_loader
    
    def get_optimal_path(self, start, end):
        """Get optimal path between two locations"""
        # First, check if we have a direct path in our data
        path_key = f"{start}_to_{end}"
        reverse_path_key = f"{end}_to_{start}"
        
        if path_key in self.path_loader.paths:
            return self.format_path_data(self.path_loader.paths[path_key], start, end)
        elif reverse_path_key in self.path_loader.paths:
            # Use reverse path
            path_data = self.path_loader.paths[reverse_path_key]
            return self.format_path_data(path_data, start, end, reverse=True)
        else:
            # Generate basic path if not in stored data
            return self.generate_basic_path(start, end)
    
    def format_path_data(self, raw_path_data, start, end, reverse=False):
        """Format path data for the application"""
        start_coords = self.path_loader.get_location_coords(start)
        end_coords = self.path_loader.get_location_coords(end)
        
        if not start_coords or not end_coords:
            return None
        
        # Extract coordinates from your path data format
        coordinates = raw_path_data.get('coordinates', [start_coords, end_coords])
        if reverse:
            coordinates = coordinates[::-1]
        
        # Calculate center point for map
        center = [
            sum(coord[0] for coord in coordinates) / len(coordinates),
            sum(coord[1] for coord in coordinates) / len(coordinates)
        ]
        
        # Calculate distance
        total_distance = 0
        for i in range(len(coordinates) - 1):
            total_distance += geodesic(coordinates[i], coordinates[i+1]).meters
        
        return {
            'coordinates': coordinates,
            'start_coords': start_coords,
            'end_coords': end_coords,
            'center': center,
            'distance': f"{total_distance:.0f} meters",
            'duration': f"{total_distance / 83:.1f} minutes",  # Average walking speed
            'waypoints': raw_path_data.get('waypoints', [])
        }
    
    def generate_basic_path(self, start, end):
        """Generate basic straight-line path if no stored path exists"""
        start_coords = self.path_loader.get_location_coords(start)
        end_coords = self.path_loader.get_location_coords(end)
        
        if not start_coords or not end_coords:
            return None
        
        distance = geodesic(start_coords, end_coords).meters
        center = [(start_coords[0] + end_coords[0])/2, (start_coords[1] + end_coords[1])/2]
        
        return {
            'coordinates': [start_coords, end_coords],
            'start_coords': start_coords,
            'end_coords': end_coords,
            'center': center,
            'distance': f"{distance:.0f} meters",
            'duration': f"{distance / 83:.1f} minutes",
            'waypoints': []
        }
