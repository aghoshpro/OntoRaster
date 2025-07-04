import random
import math
from shapely.geometry import Polygon, box
import matplotlib.pyplot as plt

def genPolygonPoints(input_bbox, num_points=None):
    """
    Generate different polygons within the input_bbox in EPSG:4326 - WGS 84
    Ranges from simple polygon (3 points) to dense polygon (many points) in OGC WKT format
    
    Args:
        input_bbox: List [min_lon, min_lat, max_lon, max_lat]
        num_points: Optional int, number of points in the polygon. If None, a random number between 3 and 20 is used.
        
    Returns:
        String: WKT format polygon
    """
    min_lon, min_lat, max_lon, max_lat = input_bbox
    
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
    
    return wkt, num_points

def genPolygon_Area(input_bbox, area_percentage=None):
    """
    Generate different polygons within the input_bbox in EPSG:4326 - WGS 84
    Ranges from small area polygon to large polygons with large area in OGC WKT format
    
    Args:
        input_bbox: List [min_lon, min_lat, max_lon, max_lat]
        area_percentage: Optional float between 0 and 1, representing what percentage of the bbox area 
                        the polygon should occupy. If None, a random value is used.
        
    Returns:
        String: WKT format polygon
    """
    min_lon, min_lat, max_lon, max_lat = input_bbox
    
    # Determine area percentage if not specified
    if area_percentage is None:
        area_percentage = random.uniform(0.1, 0.9)
    
    # Get bbox dimensions
    bbox_width = max_lon - min_lon
    bbox_height = max_lat - min_lat
    
    # Calculate center of bbox
    center_lon = (min_lon + max_lon) / 2
    center_lat = (min_lat + max_lat) / 2
    
    # Calculate polygon dimensions based on area percentage
    # For simplicity, we'll create a rectangular polygon
    scale_factor = math.sqrt(area_percentage)
    poly_width = bbox_width * scale_factor
    poly_height = bbox_height * scale_factor
    
    # Calculate polygon corners
    half_width = poly_width / 2
    half_height = poly_height / 2
    
    # Create a more interesting polygon by adding some random points and perturbations
    num_points = random.randint(4, 10)
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
    
    return wkt, area_percentage

def genPolygon_Random(input_bbox):
    """
    Generate a completely random polygon within the input_bbox in EPSG:4326 - WGS 84
    
    Args:
        input_bbox: List [min_lon, min_lat, max_lon, max_lat]
        
    Returns:
        String: WKT format polygon
    """
    min_lon, min_lat, max_lon, max_lat = input_bbox
    
    # Generate a random number of points between 3 and 15
    num_points = random.randint(3, 15)
    
    # Generate random points
    random_points = []
    for _ in range(num_points):
        x = random.uniform(min_lon, max_lon)
        y = random.uniform(min_lat, max_lat)
        random_points.append((x, y))
    
    # Create a valid polygon using convex hull
    try:
        from shapely.geometry import MultiPoint
        hull = MultiPoint(random_points).convex_hull
        
        # Convert to WKT and extract just the coordinates
        wkt = hull.wkt
        
        # If it's a valid polygon, return it
        if hull.geom_type == 'Polygon':
            return wkt
    except:
        pass
    
    # Fallback if shapely is not available or returned invalid polygon
    # Sort points by their angle from the center
    center_x = sum(p[0] for p in random_points) / len(random_points)
    center_y = sum(p[1] for p in random_points) / len(random_points)
    
    def angle_from_center(point):
        return math.atan2(point[1] - center_y, point[0] - center_x)
    
    sorted_points = sorted(random_points, key=angle_from_center)
    
    # Close the polygon by adding the first point at the end
    sorted_points.append(sorted_points[0])
    
    # Convert to WKT format
    wkt = "POLYGON (("
    wkt += ", ".join([f"{p[0]} {p[1]}" for p in sorted_points])
    wkt += "))"
    
    return wkt

def visualize_polygon_02(wkt_polygons, input_bbox=None, titles=None, rows=None, cols=None):
    """
    Visualize multiple WKT polygons in subplots within a single figure
    
    Args:
        wkt_polygons: List of WKT format polygon strings
        input_bbox: Optional bounding box to display on each subplot
        titles: Optional list of titles for each subplot
        rows: Optional number of rows for the subplot grid (auto-calculated if None)
        cols: Optional number of columns for the subplot grid (auto-calculated if None)
    """
    try:
        from shapely import wkt as shapely_wkt
        import matplotlib.pyplot as plt
        import numpy as np
        import math
        
        # Determine grid size if not provided
        n = len(wkt_polygons)
        if rows is None or cols is None:
            cols = min(3, n)  # Maximum 3 columns
            rows = math.ceil(n / cols)
        
        # Create figure with subplots
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
                    ax.fill(x, y, alpha=0.3, fc='blue')
                    
                    # If bbox is provided, plot it
                    if input_bbox:
                        min_lon, min_lat, max_lon, max_lat = input_bbox
                        ax.plot([min_lon, max_lon, max_lon, min_lon, min_lon], 
                               [min_lat, min_lat, max_lat, max_lat, min_lat], 'r--')
                    
                    # Set title if provided
                    if titles and i < len(titles):
                        ax.set_title(titles[i])
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
        for i in range(len(wkt_polygons), len(axes_flat)):
            axes_flat[i].axis('off')
        
        plt.tight_layout()
        plt.show()
        
    except ImportError as e:
        print(f"Visualization requires shapely and matplotlib packages. Error: {e}")

def main():
    # Example bounding box (from the input)
    input_bbox = [11.015629, 55.128649, 24.199222, 69.380313]
    
    print("Generating Various Polygons Within Bounding Box:")
    print(f"Bounding Box: {input_bbox}")
    
    # Generate and demonstrate different polygon types

    simple_poly, num_points = genPolygonPoints(input_bbox, random.randint(3, 100))
    print(f"\n1. Simple Polygon ({num_points}):\n")
    print(simple_poly)
 

    small_poly, area_percentage = genPolygon_Area(input_bbox, random.uniform(0.01, 0.1))
    print(f"\n3. Small Area Polygon ({area_percentage * 100:.2f}% of bbox):\n")
    print(small_poly)
    
   
    print("\n5. Random Polygon:\n")
    random_poly = genPolygon_Random(input_bbox)
    print(random_poly)
    
  
    # Store all polygons and their titles
    polygons = [
        simple_poly,
        small_poly,
        random_poly,
    ]
    
    titles = [
        "Simple Polygon ("+ str(num_points)+" points)",
        # "Complex Polygon (15 points)",
        "Small Area Polygon ("+ str(round(area_percentage * 100.0, 2))+"%)",
        # "Large Area Polygon (80%)",
        "Random Polygon",
        # "Convex Polygon",
        # "Concave Polygon"
    ]
    
    # Visualize all polygons in one figure
    try:
        # print("\nVisualizing all polygons in subplots...")
        visualize_polygon_02(polygons, input_bbox, titles)
    except Exception as e:
        print(f"Visualization failed: {e}")
        print("Make sure you have shapely and matplotlib installed.")
if __name__ == "__main__":
    main()