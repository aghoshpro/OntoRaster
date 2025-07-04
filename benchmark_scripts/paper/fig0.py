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

def genPolygon_AreaFIXED(INPUT_BBOX, num_points=None, area_percentage=None):
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
    if num_points is None:
        num_points = random.randint(3, 20)
    points = []
    
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        
        # Base radius is determined by the desired area
        x_radius = half_width
        y_radius = half_height
        
        # Add some randomness but maintain approximate area
        radius_factor = random.uniform(0.5, 1.0)
        
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

def genPolygon_Area(INPUT_BBOX, num_points=None, area_percentage=None):
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
    if num_points is None:
        num_points = random.randint(3, 20)
    points = []
    
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        
        # Base radius is determined by the desired area
        x_radius = half_width
        y_radius = half_height
        
        # Add some randomness but maintain approximate area
        radius_factor = area_percentage # random.uniform(0.9, 1.1)
        
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

def vizPolygon(wkt_polygons, INPUT_BBOX=None, titles=None, rows=None, cols=None, iteration=None):
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
            cols = min(5, n)  # Maximum 3 columns
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
                    patch = PathPatch(path, facecolor='blue', edgecolor='blue', alpha=0.1)
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
                    
                    # ax.set_xlabel('Longitude', fontsize=12, fontweight='bold')
                    # ax.set_ylabel('Latitude', fontsize=12, fontweight='bold')
                    ax.tick_params(axis='both', which='major', labelsize=13)
                    ax.grid(False)
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
        # plt.tight_layout()
        plt.tight_layout(rect=[0.0205, 0.02, 0.794, 0.814])  # Adjust bottom, left, right, top
        plt.show()
        # fig.savefig('./benchmark_scripts/v'+str(iteration)+'.png')
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


def main(iteration=0):
    # # bbox = left,bottom,right,top
    # # bbox = min Longitude , min Latitude , max Longitude , max Latitude 

    # INPUT_BBOX = [11.015629, 55.128649, 24.199222, 69.380313] ## Sweden
    INPUT_BBOX = [11.360694444453532, 48.06152777781623, 11.723194444453823, 48.24819444448305] ## Munich
    PERCENTAGE_OF_AREA = 0.2 #random.uniform(0.05, 0.7)
    
    # Generate polygons with increasing number of points
    polygons = []
    titles = []
    
    # Base polygon (AOI)
    aoi = genPolygon_Area(INPUT_BBOX, 3, PERCENTAGE_OF_AREA)
    polygons.append(aoi)
    titles.append("AOI")
    pts = [3, 4, 5, 50, 100, 500, 1000, 5000, 10000]
    # Generate additional polygons with increasing points
    for num_points in pts:  # This will create polygons with 3 to 7 points
        poly = genPolygon_AreaFIXED(INPUT_BBOX, num_points, PERCENTAGE_OF_AREA)
        polygons.append(poly)
        titles.append(f"#Points = {num_points}")
    
    # Visualize all polygons in one figure
    try:
        vizPolygon(polygons, INPUT_BBOX, titles, iteration=iteration)
    except Exception as e:
        print(f"Visualization failed: {e}")

if __name__ == "__main__":
    # for iteration in tqdm(range(25)):
    main(0)