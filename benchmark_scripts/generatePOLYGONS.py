# Create a python script to run the following function and variations of it
# # bbox = left,bottom,right,top
# # bbox = min Longitude , min Latitude , max Longitude , max Latitude 
# # north, south, east, west = 48.24819444448305, 48.06152777781623, 11.360694444453532, 11.723194444453823
# INPUT_BBOX = [11.015629,55.128649,24.199222,69.380313]

# def genPolygonPoints(INPUT_BBOX):
#     """This function will generate different polygon within the INPUT_BBOX and EPSG:4326 - WGS 84 ranges from simple polygon (3 points) to dense polygon (infinitely many points) in OGC WKT format"""

# def genPolygon_Area(INPUT_BBOX):
#     """This function will generate different polygon within the INPUT_BBOX and EPSG:4326 - WGS 84 ranges from small area polygon to large polygons with large area in OGC WKT format"""

# def 
import numpy as np
import random
import math
from shapely.geometry import Polygon, box
from shapely.validation import explain_validity
import matplotlib.pyplot as plt
from tqdm import tqdm # or from tqdm.notebook import tqdm # FOR FANCY GREEN BAR

def genPolygonPointsFIXED(INPUT_BBOX, num_points=None):
    """
    Generate different polygons within the INPUT_BBOX in EPSG:4326 - WGS 84
    Ranges from simple polygon (3 points) to dense polygon (many points) in OGC WKT format
    
    Args:
        INPUT_BBOX: List [min_lon, min_lat, max_lon, max_lat]
        num_points: Optional int, number of points in the polygon. If None, a random number between 3 and 20 is used.
        
    Returns:
        String: WKT format polygon
    """
    min_lon, min_lat, max_lon, max_lat = INPUT_BBOX
    
    # Determine number of points if not specified
    if num_points is None:
        num_points = random.randint(3, 20)
    
    # Generate points for the polygon
    points = []
    
    # For more complex shapes, we'll use a circular distribution with random perturbations
    center_lon = (min_lon + max_lon) / 2
    center_lat = (min_lat + max_lat) / 2

    # Maximum radius that fits in the bbox (approximate)
    max_radius_lon = (max_lon - min_lon) / 2 * 0.9
    max_radius_lat = (max_lat - min_lat) / 2 * 0.9
    
    for i in range(num_points):
        # Calculate angle for this point
        angle = 2 * math.pi * i / num_points
        
        # Add some randomness to the radius
        radius_factor = random.uniform(0.5, 1.0)
        
        # Calculate coordinates
        x = center_lon + math.cos(angle) * max_radius_lon * radius_factor
        y = center_lat + math.sin(angle) * max_radius_lat * radius_factor
        
        # Ensure points are within the bbox
        x = max(min(x, max_lon), min_lon)
        y = max(min(y, max_lat), min_lat)
        
        points.append((x, y))
    
    # Close the polygon by adding the first point at the end
    points.append(points[0])
    
    # Convert to WKT format
    wkt = "POLYGON (("
    wkt += ", ".join([f"{p[0]} {p[1]}" for p in points])
    wkt += "))"
    
    # Double-check OGC compliance
    is_valid, message = validate_ogc_polygon(wkt)
    if not is_valid:
        # Try to fix the polygon
        wkt = fix_ogc_polygon(wkt)
        
    return wkt

def genPolygonPoints(INPUT_BBOX, num_points=None):
    """
    Generate different polygons within the INPUT_BBOX in EPSG:4326 - WGS 84
    Ranges from simple polygon (3 points) to dense polygon (many points) in OGC WKT format
    
    Args:
        INPUT_BBOX: List [min_lon, min_lat, max_lon, max_lat]
        num_points: Optional int, number of points in the polygon. If None, a random number between 3 and 20 is used.
        
    Returns:
        String: WKT format polygon
    """
    min_lon, min_lat, max_lon, max_lat = INPUT_BBOX
    
    # Determine number of points if not specified
    if num_points is None:
        num_points = random.randint(3, 20)
    
    # Generate points for the polygon
    points = []
    
    # For more complex shapes, we'll use a circular distribution with random perturbations
    # center_lon = (min_lon + max_lon) / 2
    # center_lat = (min_lat + max_lat) / 2

    center_lon = random.uniform(min_lon, max_lon)
    center_lat = random.uniform(min_lat, max_lat)
    
    # Maximum radius that fits in the bbox (approximate)
    max_radius_lon = (max_lon - min_lon) / 2 * 0.9
    max_radius_lat = (max_lat - min_lat) / 2 * 0.9
    
    for i in range(num_points):
        # Calculate angle for this point
        angle = 2 * math.pi * i / num_points
        
        # Add some randomness to the radius
        radius_factor = random.uniform(0.5, 1.0)
        
        # Calculate coordinates
        x = center_lon + math.cos(angle) * max_radius_lon * radius_factor
        y = center_lat + math.sin(angle) * max_radius_lat * radius_factor
        
        # Ensure points are within the bbox
        x = max(min(x, max_lon), min_lon)
        y = max(min(y, max_lat), min_lat)
        
        points.append((x, y))
    
    # Close the polygon by adding the first point at the end
    points.append(points[0])
    
    # Convert to WKT format
    wkt = "POLYGON (("
    wkt += ", ".join([f"{p[0]} {p[1]}" for p in points])
    wkt += "))"
    
    # Double-check OGC compliance
    is_valid, message = validate_ogc_polygon(wkt)
    if not is_valid:
        # Try to fix the polygon
        wkt = fix_ogc_polygon(wkt)
        
    return wkt

def genPolygon_AreaFIXED(INPUT_BBOX, area_percentage=None):
    """
    Generate different polygons within the INPUT_BBOX in EPSG:4326 - WGS 84
    Ranges from small area polygon to large polygons with large area in OGC WKT format
    
    Args:
        INPUT_BBOX: List [min_lon, min_lat, max_lon, max_lat]
        area_percentage: Optional float between 0 and 1, representing what percentage of the bbox area 
                        the polygon should occupy. If None, a random value is used.
        
    Returns:
        String: WKT format polygon
    """
    min_lon, min_lat, max_lon, max_lat = INPUT_BBOX
    
    # Determine area percentage if not specified
    if area_percentage is None:
        area_percentage = random.uniform(0.1, 1.0)
    
    # Get bbox dimensions
    bbox_width = max_lon - min_lon
    bbox_height = max_lat - min_lat
    
    # Calculate center of bbox
    center_lon = (min_lon + max_lon) / 2
    center_lat = (min_lat + max_lat) / 2

    # center_lon = random.uniform(min_lon, max_lon)
    # center_lat = random.uniform(min_lat, max_lat)
    
    # Calculate polygon dimensions based on area percentage
    # For simplicity, we'll create a rectangular polygon
    scale_factor = math.sqrt(area_percentage)
    poly_width = bbox_width * scale_factor
    poly_height = bbox_height * scale_factor
    
    # Calculate polygon corners
    half_width = poly_width / 2
    half_height = poly_height / 2
    
    # Create a more interesting polygon by adding some random points and perturbations
    num_points = random.randint(3, 100)
    points = []
    
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        
        # Base radius is determined by the desired area
        x_radius = half_width
        y_radius = half_height
        
        # Add some randomness but maintain approximate area
        radius_factor = random.uniform(0.9, 1.1)
        
        x = center_lon + math.cos(angle) * x_radius * radius_factor
        y = center_lat + math.sin(angle) * y_radius * radius_factor
        
        # Ensure points are within the bbox
        x = max(min(x, max_lon), min_lon)
        y = max(min(y, max_lat), min_lat)
        
        points.append((x, y))
    
    # Close the polygon by adding the first point at the end
    points.append(points[0])
    
    # Convert to WKT format
    wkt = "POLYGON (("
    wkt += ", ".join([f"{p[0]} {p[1]}" for p in points])
    wkt += "))"

    # Double-check OGC compliance
    is_valid, message = validate_ogc_polygon(wkt)
    if not is_valid:
        # Try to fix the polygon
        wkt = fix_ogc_polygon(wkt)
    
    return wkt

def genPolygon_Area(INPUT_BBOX, area_percentage=None):
    """
    Generate different polygons within the INPUT_BBOX in EPSG:4326 - WGS 84
    Ranges from small area polygon to large polygons with large area in OGC WKT format
    
    Args:
        INPUT_BBOX: List [min_lon, min_lat, max_lon, max_lat]
        area_percentage: Optional float between 0 and 1, representing what percentage of the bbox area 
                        the polygon should occupy. If None, a random value is used.
        
    Returns:
        String: WKT format polygon
    """
    min_lon, min_lat, max_lon, max_lat = INPUT_BBOX
    
    # Determine area percentage if not specified
    if area_percentage is None:
        area_percentage = random.uniform(0.1, 1.0)
    
    # Get bbox dimensions
    bbox_width = max_lon - min_lon
    bbox_height = max_lat - min_lat
    
    # Calculate center of bbox
    # center_lon = (min_lon + max_lon) / 2
    # center_lat = (min_lat + max_lat) / 2

    center_lon = random.uniform(min_lon, max_lon)
    center_lat = random.uniform(min_lat, max_lat)
    
    # Calculate polygon dimensions based on area percentage
    # For simplicity, we'll create a rectangular polygon
    scale_factor = math.sqrt(area_percentage)
    poly_width = bbox_width * scale_factor
    poly_height = bbox_height * scale_factor
    
    # Calculate polygon corners
    half_width = poly_width / 2
    half_height = poly_height / 2
    
    # Create a more interesting polygon by adding some random points and perturbations
    num_points = random.randint(3, 100)
    points = []
    
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        
        # Base radius is determined by the desired area
        x_radius = half_width
        y_radius = half_height
        
        # Add some randomness but maintain approximate area
        radius_factor = random.uniform(0.9, 1.1)
        
        x = center_lon + math.cos(angle) * x_radius * radius_factor
        y = center_lat + math.sin(angle) * y_radius * radius_factor
        
        # Ensure points are within the bbox
        x = max(min(x, max_lon), min_lon)
        y = max(min(y, max_lat), min_lat)
        
        points.append((x, y))
    
    # Close the polygon by adding the first point at the end
    points.append(points[0])
    
    # Convert to WKT format
    wkt = "POLYGON (("
    wkt += ", ".join([f"{p[0]} {p[1]}" for p in points])
    wkt += "))"

    # Double-check OGC compliance
    is_valid, message = validate_ogc_polygon(wkt)
    if not is_valid:
        # Try to fix the polygon
        wkt = fix_ogc_polygon(wkt)
    
    return wkt

def genPolygon_with_hole(INPUT_BBOX, num_points=None, area_percentage=None, hole_size=None):
    """
    Generate a polygon with one hole within the INPUT_BBOX in EPSG:4326 - WGS 84
    
    Args:
        INPUT_BBOX: List [min_lon, min_lat, max_lon, max_lat]
        num_points: Optional int, number of points in the outer polygon. If None, a random number is used.
        area_percentage: Optional float between 0 and 1, representing what percentage of the bbox area 
                        the outer polygon should occupy. If None, a random value is used.
        hole_size: Optional float between 0 and 1, representing the size of the hole relative to the outer polygon.
                  If None, a random value is used.
        
    Returns:
        String: WKT format polygon with a hole
    """
    min_lon, min_lat, max_lon, max_lat = INPUT_BBOX
    
    # Determine parameters if not specified
    if num_points is None:
        num_points = random.randint(6, 15)
    
    if area_percentage is None:
        area_percentage = random.uniform(0.4, 0.9)  # Larger area to accommodate a hole
    
    if hole_size is None:
        hole_size = random.uniform(0.2, 0.6)  # Size of hole relative to outer polygon
    
    # Generate outer polygon
    # We'll start with a base shape like a circle to ensure we can create a valid hole
    center_lon = (min_lon + max_lon) / 2
    center_lat = (min_lat + max_lat) / 2
    
    # Scale the bbox to the area percentage
    scale = math.sqrt(area_percentage)
    poly_width = (max_lon - min_lon) * scale
    poly_height = (max_lat - min_lat) * scale
    
    # Generate outer points with some randomness
    outer_points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        
        # Add some randomness but maintain shape
        radius_factor = random.uniform(0.85, 1.15)
        
        x = center_lon + math.cos(angle) * (poly_width / 2) * radius_factor
        y = center_lat + math.sin(angle) * (poly_height / 2) * radius_factor
        
        # Ensure points are within the bbox
        x = max(min(x, max_lon), min_lon)
        y = max(min(y, max_lat), min_lat)
        
        outer_points.append((x, y))
    
    # Close the outer ring
    outer_points.append(outer_points[0])
    
    # Generate a hole (smaller similar shape)
    hole_points = []
    # Use a smaller number of points for the hole
    hole_num_points = max(3, num_points // 2)
    
    for i in range(hole_num_points):
        angle = 2 * math.pi * i / hole_num_points
        # Rotate the hole slightly to avoid point overlap
        angle += math.pi / hole_num_points
        
        # Use a smaller radius for the hole
        radius_factor = random.uniform(0.85, 1.15) * hole_size
        
        x = center_lon + math.cos(angle) * (poly_width / 2) * radius_factor
        y = center_lat + math.sin(angle) * (poly_height / 2) * radius_factor
        
        hole_points.append((x, y))
    
    # Close the hole ring
    hole_points.append(hole_points[0])
    
    # Ensure OGC compliance: exterior should be clockwise, interior counterclockwise
    if is_clockwise(outer_points):
        # Good, exterior is already clockwise
        pass
    else:
        # Fix exterior orientation
        outer_points = outer_points[:1] + outer_points[1:-1][::-1] + outer_points[-1:]
    
    if not is_clockwise(hole_points):
        # Good, interior is already counterclockwise
        pass
    else:
        # Fix interior orientation
        hole_points = hole_points[:1] + hole_points[1:-1][::-1] + hole_points[-1:]
    
    # Convert to WKT format
    wkt = "POLYGON (("
    wkt += ", ".join([f"{p[0]} {p[1]}" for p in outer_points])
    wkt += "), ("
    wkt += ", ".join([f"{p[0]} {p[1]}" for p in hole_points])
    wkt += "))"
    
    # Double-check OGC compliance
    is_valid, message = validate_ogc_polygon(wkt)
    if not is_valid:
        # Try to fix the polygon
        wkt = fix_ogc_polygon(wkt)
        
    return wkt

def genPolygon_with_multiple_holes(INPUT_BBOX, num_points=None, area_percentage=None, num_holes=None, hole_sizes=None):
    """
    Generate a polygon with multiple holes within the INPUT_BBOX in EPSG:4326 - WGS 84
    Ensures OGC compliance
    
    Args:
        INPUT_BBOX: List [min_lon, min_lat, max_lon, max_lat]
        num_points: Optional int, number of points in the outer polygon. If None, a random number is used.
        area_percentage: Optional float between 0 and 1, representing what percentage of the bbox area 
                        the outer polygon should occupy. If None, a random value is used.
        num_holes: Optional int, number of holes. If None, a random number between 1 and 4 is used.
        hole_sizes: Optional list of floats between 0 and 1, representing the size of each hole relative 
                   to the outer polygon. If None, random values are used.
        
    Returns:
        String: OGC compliant WKT format polygon with multiple holes
    """
    min_lon, min_lat, max_lon, max_lat = INPUT_BBOX
    
    # Determine parameters if not specified
    if num_points is None:
        num_points = random.randint(8, 20)
    
    if area_percentage is None:
        area_percentage = random.uniform(0.5, 0.95)  # Larger area to accommodate multiple holes
    
    if num_holes is None:
        num_holes = random.randint(1, 4)
    
    if hole_sizes is None:
        # Generate random hole sizes, smaller with more holes
        max_size = min(0.6, 1.5 / num_holes)
        hole_sizes = [random.uniform(0.1, max_size) for _ in range(num_holes)]
    
    # Generate outer polygon similar to genPolygon_with_hole
    center_lon = (min_lon + max_lon) / 2
    center_lat = (min_lat + max_lat) / 2
    
    # Scale the bbox to the area percentage
    scale = math.sqrt(area_percentage)
    poly_width = (max_lon - min_lon) * scale
    poly_height = (max_lat - min_lat) * scale
    
    # Generate outer points similar to genPolygon_with_hole
    outer_points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        radius_factor = random.uniform(0.85, 1.15)
        x = center_lon + math.cos(angle) * (poly_width / 2) * radius_factor
        y = center_lat + math.sin(angle) * (poly_height / 2) * radius_factor
        x = max(min(x, max_lon), min_lon)
        y = max(min(y, max_lat), min_lat)
        outer_points.append((x, y))
    
    # Close the outer ring
    outer_points.append(outer_points[0])
    
    # Generate multiple holes
    all_holes = []
    
    for h in range(num_holes):
        hole_points = []
        hole_num_points = max(3, num_points // 2)
        hole_size = hole_sizes[h]
        
        # Offset the hole from the center (except for the first hole which stays centered)
        if h == 0:
            hole_center_lon = center_lon
            hole_center_lat = center_lat
        else:
            # Place holes at different positions
            angle = 2 * math.pi * h / num_holes
            offset_factor = random.uniform(0.2, 0.6)  # How far from center
            hole_center_lon = center_lon + math.cos(angle) * (poly_width / 4) * offset_factor
            hole_center_lat = center_lat + math.sin(angle) * (poly_height / 4) * offset_factor
        
        for i in range(hole_num_points):
            angle = 2 * math.pi * i / hole_num_points
            # Add a phase offset to make holes look different
            angle += h * math.pi / num_holes
            
            radius_factor = random.uniform(0.85, 1.15) * hole_size
            
            x = hole_center_lon + math.cos(angle) * (poly_width / 3) * radius_factor
            y = hole_center_lat + math.sin(angle) * (poly_height / 3) * radius_factor
            
            hole_points.append((x, y))
        
        # Close the hole ring
        hole_points.append(hole_points[0])
        
        # Ensure OGC compliance: interior should be counterclockwise
        if not is_clockwise(hole_points):
            # Good, already counterclockwise
            pass
        else:
            # Fix orientation
            hole_points = hole_points[:1] + hole_points[1:-1][::-1] + hole_points[-1:]
        
        all_holes.append(hole_points)
    
    # Ensure exterior is clockwise
    if is_clockwise(outer_points):
        # Good, already clockwise
        pass
    else:
        # Fix orientation
        outer_points = outer_points[:1] + outer_points[1:-1][::-1] + outer_points[-1:]
    
    # Convert to WKT format
    wkt = "POLYGON (("
    wkt += ", ".join([f"{p[0]} {p[1]}" for p in outer_points])
    
    for hole in all_holes:
        wkt += "), ("
        wkt += ", ".join([f"{p[0]} {p[1]}" for p in hole])
    
    wkt += "))"
    
    # Double-check OGC compliance
    # is_valid, message = validate_ogc_polygon(wkt)
    # if not is_valid:
    #     # Try to fix the polygon
    #     wkt_valid = fix_ogc_polygon(wkt)
        
    return wkt, fix_ogc_polygon(wkt)

# def genPolygon_Random(INPUT_BBOX, num_points=None):
#     """
#     Generate a completely random polygon within the INPUT_BBOX in EPSG:4326 - WGS 84
    
#     Args:
#         INPUT_BBOX: List [min_lon, min_lat, max_lon, max_lat]
        
#     Returns:
#         String: WKT format polygon
#     """
#     min_lon, min_lat, max_lon, max_lat = INPUT_BBOX
    
#     # Determine number of points if not specified
#     if num_points is None:
#         num_points = random.randint(3, 20)
    
#     # Generate random points
#     random_points = []
#     for _ in range(num_points):
#         x = random.uniform(min_lon, max_lon)
#         y = random.uniform(min_lat, max_lat)
#         random_points.append((x, y))
    
#     # Create a valid polygon using convex hull
#     try:
#         from shapely.geometry import MultiPoint
#         hull = MultiPoint(random_points).convex_hull
        
#         # Convert to WKT and extract just the coordinates
#         wkt = hull.wkt
        
#         # If it's a valid polygon, return it
#         if hull.geom_type == 'Polygon':
#             return wkt, num_points
#     except:
#         pass
    
#     # Fallback if shapely is not available or returned invalid polygon
#     # Sort points by their angle from the center
#     center_x = sum(p[0] for p in random_points) / len(random_points)
#     center_y = sum(p[1] for p in random_points) / len(random_points)
    
#     def angle_from_center(point):
#         return math.atan2(point[1] - center_y, point[0] - center_x)
    
#     sorted_points = sorted(random_points, key=angle_from_center)
    
#     # Close the polygon by adding the first point at the end
#     sorted_points.append(sorted_points[0])
    
#     # Convert to WKT format
#     wkt = "POLYGON (("
#     wkt += ", ".join([f"{p[0]} {p[1]}" for p in sorted_points])
#     wkt += "))"
    
#     return wkt, num_points

def genPolygon_Random(INPUT_BBOX, num_holes=None, num_points=None, with_holes=False, area_percentage=None):
    """
    Generate a completely random polygon within the INPUT_BBOX in EPSG:4326 - WGS 84
    Enhanced version that can include holes and area constraints
    
    Args:
        INPUT_BBOX: List [min_lon, min_lat, max_lon, max_lat]
        with_holes: Boolean, whether to include holes
        num_holes: Optional int, number of holes if with_holes is True
        area_percentage: Optional float between 0 and 1, representing what percentage of the bbox area 
                        the polygon should occupy
        
    Returns:
        String: WKT format polygon
    """
    # Determine if we should generate a polygon with holes
    if with_holes is None:
        with_holes = random.choice([True, False])
    
    # Generate polygon with holes if requested
    if with_holes:
        if random.random() < 0.3:  # 30% chance for multiple holes
            return genPolygon_with_multiple_holes(INPUT_BBOX, area_percentage=area_percentage, num_holes=num_holes)
        else:
            return genPolygon_with_hole(INPUT_BBOX, area_percentage=area_percentage)
    
    # Otherwise, use the area parameter to generate a polygon without holes
    min_lon, min_lat, max_lon, max_lat = INPUT_BBOX
    
    # Determine area percentage if not specified
    if area_percentage is None:
        area_percentage = random.uniform(0.1, 0.9)
    
    # Generate a random number of points between 4 and 20
    if num_points is None:
       num_points = random.randint(4, 20)
    
    # Use various strategies to generate random polygons
    strategy = random.choice(['convex', 'star', 'irregular'])
    
    if strategy == 'convex':
        # Generate a convex polygon
        return genPolygon_Convex(INPUT_BBOX, num_points)
    
    elif strategy == 'star':
        # Generate a star-like shape (which could be concave)
        return genPolygon_Concave(INPUT_BBOX, random.uniform(0.2, 0.8))
    
    else:
        # Generate an irregular shape with area constraints
        center_lon = (min_lon + max_lon) / 2
        center_lat = (min_lat + max_lat) / 2
        
        # Scale the bbox to the area percentage
        scale = math.sqrt(area_percentage)
        poly_width = (max_lon - min_lon) * scale
        poly_height = (max_lat - min_lat) * scale
        
        # Generate points with varying distances from center
        points = []
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            
            # Vary the distance from center randomly
            distance_factor = random.uniform(0.5, 1.5)
            distance = distance_factor * scale
            
            x = center_lon + math.cos(angle) * (poly_width / 2) * distance
            y = center_lat + math.sin(angle) * (poly_height / 2) * distance
            
            # Ensure points are within the bbox
            x = max(min(x, max_lon), min_lon)
            y = max(min(y, max_lat), min_lat)
            
            points.append((x, y))
        
        # Create a valid polygon by sorting points around the center
        def angle_from_center(point):
            return math.atan2(point[1] - center_lat, point[0] - center_lon)
        
        sorted_points = sorted(points, key=angle_from_center)
        
        # Close the polygon
        sorted_points.append(sorted_points[0])
        
        # Convert to WKT format
        wkt = "POLYGON (("
        wkt += ", ".join([f"{p[0]} {p[1]}" for p in sorted_points])
        wkt += "))"
        
        return wkt, num_points
    
def genPolygon_Convex(INPUT_BBOX, num_points=None):
    """
    Generate a convex polygon within the INPUT_BBOX in EPSG:4326 - WGS 84
    
    Args:
        INPUT_BBOX: List [min_lon, min_lat, max_lon, max_lat]
        num_points: Optional int, number of points in the polygon. If None, a random number between 4 and 12 is used.
        
    Returns:
        String: WKT format polygon
    """
    if num_points is None:
        num_points = random.randint(4, 12)
    
    # Generate random points
    random_points = genRandomPoints(INPUT_BBOX, num_points)
    
    # Create convex hull (automatically sorts points correctly)
    try:
        from shapely.geometry import MultiPoint
        hull = MultiPoint(random_points).convex_hull
        return hull.wkt
    except ImportError:
        # Manual convex hull algorithm if shapely is not available
        return genPolygon_Random(INPUT_BBOX)

def genPolygon_Concave(INPUT_BBOX, complexity=None):
    """
    Generate a concave (non-convex) polygon within the INPUT_BBOX in EPSG:4326 - WGS 84
    
    Args:
        INPUT_BBOX: List [min_lon, min_lat, max_lon, max_lat]
        complexity: Optional float between 0 and 1, determining how concave the polygon is.
                   If None, a random value is used.
        
    Returns:
        String: WKT format polygon
    """
    min_lon, min_lat, max_lon, max_lat = INPUT_BBOX
    
    # Determine complexity if not specified
    if complexity is None:
        complexity = random.uniform(0.2, 0.8)
    
    # Start with a simple convex shape (e.g. a circle)
    num_points = random.randint(6, 15)
    
    center_lon = (min_lon + max_lon) / 2
    center_lat = (min_lat + max_lat) / 2
    
    # Maximum radius that fits in the bbox
    max_radius_lon = (max_lon - min_lon) / 2 * 0.9
    max_radius_lat = (max_lat - min_lat) / 2 * 0.9
    
    points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        
        # Add "dents" to create concavity
        radius_factor = 1.0
        if i % 2 == 0:  # Every other point gets pushed inward
            radius_factor = 1.0 - complexity * 0.7
        
        x = center_lon + math.cos(angle) * max_radius_lon * radius_factor
        y = center_lat + math.sin(angle) * max_radius_lat * radius_factor
        
        # Ensure points are within the bbox
        x = max(min(x, max_lon), min_lon)
        y = max(min(y, max_lat), min_lat)
        
        points.append((x, y))
    
    # Close the polygon by adding the first point at the end
    points.append(points[0])
    
    # Convert to WKT format
    wkt = "POLYGON (("
    wkt += ", ".join([f"{p[0]} {p[1]}" for p in points])
    wkt += "))"
    
    # Double-check OGC compliance
    is_valid, message = validate_ogc_polygon(wkt)
    if not is_valid:
        wkt = fix_ogc_polygon(wkt)
        
    return wkt

def genRandomPoints(INPUT_BBOX, num_points):
    """Helper function to generate random points within the bbox"""
    min_lon, min_lat, max_lon, max_lat = INPUT_BBOX
    points = []
    for _ in range(num_points):
        x = random.uniform(min_lon, max_lon)
        y = random.uniform(min_lat, max_lat)
        points.append((x, y))
    return points

def visualize_polygon_02(wkt_polygons, INPUT_BBOX=None, titles=None, rows=None, cols=None, iteration=None):
    """
    Visualize multiple WKT polygons in subplots within a single figure
    
    Args:
        wkt_polygons: List of WKT format polygon strings
        INPUT_BBOX: Optional bounding box to display on each subplot
        titles: Optional list of titles for each subplot
        rows: Optional number of rows for the subplot grid (auto-calculated if None)
        cols: Optional number of columns for the subplot grid (auto-calculated if None)
    """
    try:
        from shapely import wkt as shapely_wkt       
        # Determine grid size if not provided
        n = len(wkt_polygons)
        if rows is None or cols is None:
            cols = min(4, n)  # Maximum 3 columns
            rows = math.ceil(n / cols)
        
        # Create figure with subplots
        # plt.ion()
        # clear_output(wait=True)
        fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 4*rows))
        # Flatten axes array for easy indexing if there are multiple subplots
        if n > 1:
            if rows == 1 and cols == 1:
                axes = np.array([axes])
            axes_flat = axes.flatten()
        else:
            axes_flat = [axes]
        
        # Plot each polygon in its own subplot
        for i, wkt in enumerate(wkt_polygons):
            if i < len(axes_flat):
                ax = axes_flat[i]
                
                # Parse the WKT string
                try:
                    polygon = shapely_wkt.loads(wkt)
                    
                    # Plot the polygon
                    x, y = polygon.exterior.xy
                    ax.plot(x, y, 'b-')
                    ax.fill(x, y, alpha=0.2, fc='blue')
                    
                                        # For polygons with holes, plot each interior ring
                    if hasattr(polygon, 'interiors') and polygon.interiors:
                        for interior in polygon.interiors:
                            x_hole, y_hole = interior.xy
                            ax.plot(x_hole, y_hole, 'r-')  # Use red for holes
                            ax.fill(x_hole, y_hole, alpha=1, fc='white')
                    
                    # Fill the polygon correctly with holes
                    # We need to use a special patch for this
                    from matplotlib.patches import PathPatch
                    from matplotlib.path import Path
                    
                    # Create vertices and codes for the Path
                    vertices = []
                    codes = []
                    
                    # Add exterior
                    for x_coord, y_coord in zip(*polygon.exterior.xy):
                        vertices.append((x_coord, y_coord))
                    
                    # Start with a MOVETO code, then use LINETO, end with CLOSEPOLY
                    codes.append(Path.MOVETO)
                    codes.extend([Path.LINETO] * (len(polygon.exterior.xy[0]) - 2))
                    codes.append(Path.CLOSEPOLY)
                    
                    # Add interiors (holes)
                    for interior in polygon.interiors:
                        vertices.append((interior.xy[0][0], interior.xy[1][0]))  # Start point of hole
                        codes.append(Path.MOVETO)
                        
                        for x_coord, y_coord in zip(interior.xy[0][1:-1], interior.xy[1][1:-1]):
                            vertices.append((x_coord, y_coord))
                            codes.append(Path.LINETO)
                        
                        vertices.append((interior.xy[0][0], interior.xy[1][0]))  # Back to start point
                        codes.append(Path.CLOSEPOLY)
                    
                    path = Path(vertices, codes)
                    patch = PathPatch(path, facecolor='blue', edgecolor='blue', alpha=0.3)
                    ax.add_patch(patch)
                    
                    # If bbox is provided, plot it
                    if INPUT_BBOX:
                        min_lon, min_lat, max_lon, max_lat = INPUT_BBOX
                        ax.plot([min_lon, max_lon, max_lon, min_lon, min_lon], 
                               [min_lat, min_lat, max_lat, max_lat, min_lat], 'r--')
                    
                    # Set title if provided
                    if titles and i < len(titles):
                        ax.set_title(titles[i], fontsize=15, fontweight='bold')
                    else:
                        ax.set_title(f"Polygon {i+1}")
                    
                    ax.set_xlabel('Longitude')
                    ax.set_ylabel('Latitude')
                    ax.grid(True)
                    ax.axis('equal')
                except Exception as e:
                    ax.text(0.5, 0.5, f"Error: {str(e)}", ha='center', va='center')
                    ax.axis('off')
            
        # Hide any unused subplots
        iteration = iteration + 1
        for i in range(len(wkt_polygons), len(axes_flat)):
            axes_flat[i].axis('off')
        fig.suptitle('WKT Polygons (v' + str(iteration) + ')', fontsize=20)
        # plt.ioff()  # Turn off interactive mode
        # plt.pause(0.7)  # Pause to update the plot
        plt.tight_layout()
        # plt.show()
        fig.savefig('./benchmark_scripts/v'+str(iteration)+'.png')
        # plt.clf()
        # input("Press enter to continue")

    except ImportError as e:
        print(f"Visualization requires shapely and matplotlib packages. Error: {e}")

###############################
### OGC Compliancy Checking ###
###############################
def validate_ogc_polygon(wkt):
    """
    Validate that a polygon in WKT format is OGC compliant
    
    Args:
        wkt: WKT format polygon string
        
    Returns:
        tuple: (is_valid, message) where is_valid is a boolean and message describes any issues
    """
    try:
        from shapely import wkt as shapely_wkt
        import shapely.geometry
        
        # Parse the WKT string
        polygon = shapely_wkt.loads(wkt)
        
        # Check if the geometry is a polygon
        if not isinstance(polygon, shapely.geometry.Polygon):
            return False, "Not a polygon geometry"
        
        # Check if the polygon is valid according to OGC
        if not polygon.is_valid:
            reason = shapely.validation.explain_validity(polygon)
            return False, f"Invalid polygon: {reason}"
        
        # Check if the exterior ring is clockwise
        exterior_ring = polygon.exterior
        is_ext_clockwise = is_clockwise(exterior_ring.coords)
        if not is_ext_clockwise:
            return False, "Exterior ring is not clockwise (OGC requires clockwise)"
        
        # Check if interior rings (holes) are counterclockwise
        for interior in polygon.interiors:
            if is_clockwise(interior.coords):
                return False, "Interior ring (hole) is not counterclockwise (OGC requires counterclockwise)"
        
        # Check for self-intersections
        if not polygon.is_simple:
            return False, "Polygon has self-intersections"
        
        return True, "Polygon is OGC compliant"
        
    except ImportError:
        return False, "Validation requires shapely package"
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def is_clockwise(coordinates):
    """
    Determine if a ring is clockwise by calculating the signed area
    
    Args:
        coordinates: List of (x, y) coordinates representing a ring
        
    Returns:
        boolean: True if clockwise, False if counterclockwise
    """
    # Shoelace formula to compute the signed area
    area = 0.0
    for i in range(len(coordinates) - 1):  # -1 because the last point is the same as the first
        j = (i + 1) % (len(coordinates) - 1)
        area += coordinates[i][0] * coordinates[j][1]
        area -= coordinates[j][0] * coordinates[i][1]
    
    # If area is positive, the ring is counterclockwise
    # If area is negative, the ring is clockwise
    return area < 0

def fix_ring_orientation(coordinates, should_be_clockwise=True):
    """
    Fix the orientation of a ring to be clockwise or counterclockwise
    
    Args:
        coordinates: List of (x, y) coordinates representing a ring
        should_be_clockwise: Boolean, True if the ring should be clockwise
        
    Returns:
        list: Coordinates in the correct orientation
    """
    is_clock = is_clockwise(coordinates)
    
    if (should_be_clockwise and not is_clock) or (not should_be_clockwise and is_clock):
        # Reverse the order of the coordinates, but keep the first/last point the same
        fixed = coordinates[:1] + coordinates[1:-1][::-1] + coordinates[-1:]
        return fixed
    
    return coordinates

def fix_ogc_polygon(wkt):
    """
    Fix common OGC compliance issues in a polygon
    
    Args:
        wkt: WKT format polygon string
        
    Returns:
        string: Fixed WKT polygon or the original if it cannot be fixed
    """
    try:
        from shapely import wkt as shapely_wkt
        import shapely.geometry
        
        # Parse the WKT string
        polygon = shapely_wkt.loads(wkt)
        
        if not isinstance(polygon, shapely.geometry.Polygon):
            return wkt  # Can't fix non-polygons
        
        # Fix self-intersections and other validity issues
        if not polygon.is_valid:
            polygon = polygon.buffer(0)  # This often fixes invalid polygons
        
        # Fix ring orientations
        exterior_coords = list(polygon.exterior.coords)
        fixed_exterior = fix_ring_orientation(exterior_coords, True)  # Exterior should be clockwise
        
        fixed_interiors = []
        for interior in polygon.interiors:
            interior_coords = list(interior.coords)
            fixed_interior = fix_ring_orientation(interior_coords, False)  # Interior should be counterclockwise
            fixed_interiors.append(fixed_interior)
        
        # Reconstruct the WKT
        wkt = "POLYGON (("
        wkt += ", ".join([f"{p[0]} {p[1]}" for p in fixed_exterior])
        wkt += ")"
        
        for interior in fixed_interiors:
            wkt += ", ("
            wkt += ", ".join([f"{p[0]} {p[1]}" for p in interior])
            wkt += ")"
        
        wkt += ")"
        
        return wkt
        
    except Exception as e:
        print(f"Error fixing polygon: {e}")
        return wkt  # Return the original if we can't fix it

def check_all_polygons_ogc_compliance(polygons_wkt, titles=None):
    """
    Check if all polygons are OGC compliant and print results
    
    Args:
        polygons_wkt: List of WKT format polygon strings
        titles: Optional list of titles for each polygon
        
    Returns:
        tuple: (all_valid, results) where all_valid is a boolean indicating if all polygons are valid,
               and results is a list of (polygon_index, title, is_valid, message) tuples
    """
    results = []
    all_valid = True
    
    for i, wkt in enumerate(polygons_wkt):
        title = titles[i] if titles and i < len(titles) else f"Polygon {i+1}"
        is_valid, message = validate_ogc_polygon(wkt)
        
        results.append((i, title, is_valid, message))
        
        if not is_valid:
            all_valid = False
    
    # Print results
    print("\nOGC Compliance Check Results:")
    print("-----------------------------")
    
    for i, title, is_valid, message in results:
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{i+1}. {title}: {status}")
        if not is_valid:
            print(f"   Reason: {message}")
    
    print(f"\nOverall: {'All polygons are OGC compliant' if all_valid else 'Some polygons are not OGC compliant'}")
    
    return all_valid, results

def main(iteration):
    # # bbox = left,bottom,right,top
    # # bbox = min Longitude , min Latitude , max Longitude , max Latitude 

    # INPUT_BBOX = [11.015629, 55.128649, 24.199222, 69.380313] ## Sweden
    INPUT_BBOX = [11.360694444453532, 48.06152777781623, 11.723194444453823, 48.24819444448305] ## Munich

    NUM_OF_POINTS = random.randint(3, 100)
    PERCENTAGE_OF_AREA = random.uniform(0.01, 1.0)
    
    #########################
    ### OGC Polygon Types ###
    #########################

    simple_poly_fixed = genPolygonPointsFIXED(INPUT_BBOX, NUM_OF_POINTS)
    # print(f"\n1. Simple Polygon Fixed Points ({num_points}):\n")
    # print(simple_poly_fixed)

    simple_poly = genPolygonPoints(INPUT_BBOX, NUM_OF_POINTS)
    # print(f"\n1. Simple Polygon Points ({num_points}):\n")
    # print(simple_poly)
    
    simple_poly_area_fixed  = genPolygon_AreaFIXED(INPUT_BBOX, PERCENTAGE_OF_AREA)

    simple_poly_area = genPolygon_Area(INPUT_BBOX, PERCENTAGE_OF_AREA)
    # print(f"\n3. Simple Polygon Area ({area_percentage * 100:.2f}% of bbox):\n")
    # print(small_poly) genPolygon_AreaFIXED
    
    # print("\n4. Polygon with a Hole:\n")
    single_hole_poly = genPolygon_with_hole(INPUT_BBOX, NUM_OF_POINTS)
    # print(single_hole_poly)

    # print("\n5. Polygon with Multiple Holes :\n")
    multi_hole_poly, multi_hole_poly_valid = genPolygon_with_multiple_holes(INPUT_BBOX, NUM_OF_POINTS, num_holes=5)
    # print(multi_hole_poly)

    # print("\n6. Random Polygon:\n")
    random_poly = genPolygon_Random(INPUT_BBOX, None, NUM_OF_POINTS, with_holes=True)
    # print(random_poly)
    
    # print("\n6. Convex Polygon:")
    convex_poly = genPolygon_Convex(INPUT_BBOX)
    # print(convex_poly)
    
    # print("\n7. Concave Polygon:")
    concave_poly = genPolygon_Concave(INPUT_BBOX, NUM_OF_POINTS)
    # print(concave_poly)
    

    # Store all polygons and their titles
    polygons = [
        simple_poly_fixed,
        simple_poly,
        simple_poly_area_fixed,
        simple_poly_area,
        single_hole_poly,
        multi_hole_poly,
        multi_hole_poly_valid, 
        convex_poly,
        concave_poly,
    ]
    

    
    titles = [
        "BM1 - "+ str(NUM_OF_POINTS)+" POINTS (center)",
        "BM2 - "+ str(NUM_OF_POINTS)+" POINTS (anywhere)",
        "BM3 - "+ str(round(PERCENTAGE_OF_AREA * 100.0, 2))+"% of BBOX Area (center)",
        "BM4 - "+ str(round(PERCENTAGE_OF_AREA * 100.0, 2))+"% of BBOX Area (anywhere)",
        "BM5 - Single Hole",
        "BM6 - Multiple Holes (INVALID OGC)",
        "BM6 - Multiple Holes (VALID OGC)",
        # "Random (all in one)"
        "Convex Polygon",
        "Concave Polygon"
    ]
    
    # Visualize all polygons in one figure
    try:
        # print("\nVisualizing all polygons in subplots...")
        all_valid, results = check_all_polygons_ogc_compliance(polygons, titles)
        # visualize_polygon_02(polygons, INPUT_BBOX, titles, iteration=iteration)
    except Exception as e:
        print(f"Visualization failed: {e}")
        print("Make sure you have shapely and matplotlib installed.")
if __name__ == "__main__":
    for iteration in tqdm(range(25)):
        main(iteration)