from SPARQLWrapper import SPARQLWrapper, JSON, POST
import time
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import numpy as np
from tqdm import tqdm
import gc

from shapely.geometry import Polygon, box
from shapely import wkt
from shapely.ops import transform
from pyproj import Transformer

sparql = SPARQLWrapper("http://localhost:8082/sparql")
sparql.setReturnFormat(JSON)

def calculateArea(poly_wkt_str):
    polygon = wkt.loads(poly_wkt_str)
    area_sq_degrees = polygon.area
    centroid = polygon.centroid
    lon, lat = centroid.x, centroid.y
    utm_zone = int((lon + 180) / 6) + 1
    proj_string = f"+proj=utm +zone={utm_zone} +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
    # # Set up the transformation
    transformer = Transformer.from_crs("EPSG:4326", proj_string, always_xy=True)
    utm_polygon = transform(transformer.transform, polygon)
    area_sq_meters = utm_polygon.area
    area_sq_kilometers = area_sq_meters / 1_000_000  # Convert to square kilometers
    return float(format(area_sq_kilometers, '.2f'))

def genPolygonExp(INPUT_BBOX, NUM_OF_POINTS, AREA_IN_km, UNIFORM_FACTOR):
    """
    Generate a polygon with specified area in square kilometers
    
    Parameters:
    INPUT_BBOX: WKT string representing the bounding box
    NUM_OF_POINTS: Number of points in the polygon
    AREA_IN_km²: Target area in square kilometers
    UNIFORM_FACTOR: Controls shape regularity (0.0: very irregular, 1.0: perfectly regular)
    
    Returns:
    WKT string representing the generated polygon in EPSG:4326
    """
    # Parse the bounding box
    if type(INPUT_BBOX) == str:
        bbox = wkt.loads(INPUT_BBOX)
        bbox_bounds = bbox.bounds
        min_x, min_y, max_x, max_y = bbox_bounds
    else:
        min_x, min_y, max_x, max_y = INPUT_BBOX
        bbox = wkt.loads((box(*INPUT_BBOX, ccw=True)).wkt)
    
    # Compute the centroid for UTM zone determination
    centroid_x = (min_x + max_x) / 2
    centroid_y = (min_y + max_y) / 2
    
    # Determine UTM zone
    utm_zone = int((centroid_x + 180) / 6) + 1
    proj_string = f"+proj=utm +zone={utm_zone} +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
    
    # Create transformers for WGS84 <-> UTM conversion
    transformer_to_utm = Transformer.from_crs("EPSG:4326", proj_string, always_xy=True)
    transformer_from_utm = Transformer.from_crs(proj_string, "EPSG:4326", always_xy=True)
    
    # Transform the bounding box to UTM
    utm_bbox = transform(transformer_to_utm.transform, bbox)
    utm_bounds = utm_bbox.bounds
    utm_min_x, utm_min_y, utm_max_x, utm_max_y = utm_bounds
    
    # Calculate the center point of the bounding box in UTM
    center_x = (utm_min_x + utm_max_x) / 2
    center_y = (utm_min_y + utm_max_y) / 2
    
    # Calculate the radius needed for the target area
    # For a regular polygon with n sides, area = (n/4) * r² * sin(2π/n)
    # Solving for r: r = sqrt(area / ((n/4) * sin(2π/n)))
    target_area_m2 = AREA_IN_km * 1_000_000  # Convert km² to m²
    
    # For a regular polygon, calculate the radius
    n = NUM_OF_POINTS
    regular_radius = math.sqrt(target_area_m2 / ((n/4) * math.sin(2 * math.pi / n)))
    
    # Generate points for the polygon
    angles = np.linspace(0, 2 * np.pi, NUM_OF_POINTS, endpoint=False)
    
    utm_points = []
    for angle in angles:
        # Start with perfectly regular distance (radius)
        base_distance = regular_radius
        
        # Add randomness based on the uniformity factor
        if UNIFORM_FACTOR < 1.0:
            # The lower the uniformity factor, the more randomness
            random_variation = (1.0 - UNIFORM_FACTOR) * random.uniform(0.5, 1.5)
            distance = base_distance * (1.0 + (1.0 - UNIFORM_FACTOR) * (random_variation - 1.0))
        else:
            distance = base_distance
        
        # Calculate point coordinates
        x = center_x + distance * np.cos(angle)
        y = center_y + distance * np.sin(angle)
        utm_points.append((x, y))
    
    # Create the polygon in UTM
    utm_polygon = Polygon(utm_points)
    
    # Calculate the area of the generated polygon
    initial_area_m2 = utm_polygon.area
    
    # Scale the polygon to match the target area
    scaling_factor = math.sqrt(target_area_m2 / initial_area_m2)
    
    # Apply scaling: translate to origin, scale, translate back
    def scale_around_center(x, y):
        dx = x - center_x
        dy = y - center_y
        return center_x + dx * scaling_factor, center_y + dy * scaling_factor
    
    scaled_utm_polygon = transform(lambda x, y: scale_around_center(x, y), utm_polygon)
    
    # Transform the UTM polygon back to WGS84 (EPSG:4326)
    wgs84_polygon = transform(transformer_from_utm.transform, scaled_utm_polygon)
    
    # Return the WKT representation
    return wgs84_polygon.wkt

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
    
def benchmark(poly):
    """
    Records the query processing time for a SPARQL query with different LIMIT values.
    
    Args:
        point: The LIMIT value for the SPARQL query
        
    Returns:
        float: The time taken to execute the query in seconds
    """
    query = f"""
        PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
        PREFIX rdfs:	<http://www.w3.org/2000/01/rdf-schema#>
        PREFIX geo:	<http://www.opengis.net/ont/geosparql#>
        PREFIX rasdb:	<https://github.com/aghoshpro/RasterDataCube/>

        SELECT ?clipped {{
        ?gridCoverage a :Raster .
        ?gridCoverage rasdb:rasterName ?rasterName .
        FILTER (CONTAINS(?rasterName, 'Elevation')) 
        BIND ('{poly}'^^geo:wktLiteral AS ?customRegionWkt)
        BIND ('2000-02-11T00:00:00+00:00'^^xsd:dateTime AS ?timeStamp)
        BIND (rasdb:rasSpatialAverage(?timeStamp, ?customRegionWkt, ?rasterName) AS ?clipped) 
        }}
    """
    
    sparql.setQuery(query)
    sparql.setMethod(POST) # ro avoid the followinf error SPARQLWrapper.SPARQLExceptions.QueryBadFormed: QueryBadFormed: A bad request has been sent to the endpoint: probably the SPARQL query is badly formed.
    # Measure the query execution time
    start_time = time.time()
    results = sparql.query()
    end_time = time.time()
    # Calculate the processing time
    processing_time = end_time - start_time
    return processing_time

# input_bbox = [11.015629, 55.128649, 24.199222, 69.380313] ## Sweden
INPUT_BBOX = [11.360694444453532, 48.06152777781623, 11.723194444453823, 48.24819444448305] # MUNICH
INPUT_BBOX_WKT_STRING = (box(*INPUT_BBOX, ccw=True)).wkt
NUM_OF_POINTS = 500 # 1,2 points are not polygon
AREA_IN_km = 100 
UNIFORM_FACTOR = 0.9
XTICKS_BIN = 50
# Create a list to store benchmark results
benchmark_data = []

# Run benchmarks with increasing LIMIT values
point_values = list(range(3, NUM_OF_POINTS, 10))  # 10, 20, 30, ... 100

for point in tqdm(point_values):
    try:
        sample_polygon = genPolygonExp(INPUT_BBOX, point, AREA_IN_km, UNIFORM_FACTOR)
        time_taken = benchmark(sample_polygon)
        del sample_polygon
        gc.collect()
        benchmark_data.append({'Points': point, 'Processing_Time': time_taken})
    except Exception as e:
        print(f"Error with Points {point}: {e}")

# Create a pandas DataFrame from the benchmark data
df = pd.DataFrame(benchmark_data)
## Save the benchmark data to a CSV file
df.to_csv('./benchmark_scripts/bm1_20000.csv', index=False)

# df = pd.read_csv('./benchmark_scripts/sparql_benchmark_results.csv')

# Identify min and max processing time
min_time = df['Processing_Time'].min()
max_time = df['Processing_Time'].max()

# Log-transform the y-values
y = df['Processing_Time']
x = df['Points']

# Fit a linear regression: log(y) = m*x + b
m1, c = np.polyfit(x, y, 1)

# Calculate fitted values for the trend line (in log scale)
trend_log_y1 = m1 * x + c
trend_y1 = 10 ** trend_log_y1  # Convert back to original scale


# Assign colors
colors = ['green' if t == min_time else 'red' if t == max_time else 'deepskyblue' for t in df['Processing_Time']]
# Plot the results
plt.figure(figsize=(20, 10))
bars = plt.bar(df['Points'], df['Processing_Time'], align='center', color=colors, width=10)
# Get min and max heights
min_height = min(bar.get_height() for bar in bars)
max_height = max(bar.get_height() for bar in bars)
# Label only min and max bars
for bar in bars:
    height = bar.get_height()
    if height == min_height or height == max_height:
        plt.text(bar.get_x() + bar.get_width() / 2, height,
                 f'{height:.2f}', ha='center', va='bottom', color='blue', fontsize=10, fontweight='bold')
# Plot the results
# plt.plot(x, trend_y1, color='black', linestyle='--', label=f'Trend: y = {m1:.8f}x + {c:.4f}')
plt.title('Query Processing Time VS Varying Points of Fixed Area Uniform Polygon (Case 1)', fontsize=20, fontweight='bold')
plt.xlabel('Points', fontsize=15, fontweight='bold')
plt.ylabel('Processing Time (seconds)', fontsize=15, fontweight='bold')
plt.xticks(range(df['Points'].min(), df['Points'].max() + 1, XTICKS_BIN), fontsize=12, rotation = 35)
plt.yticks(fontsize=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.margins(x=0)
plt.savefig('./benchmark_scripts/bm1_bar_plot20000.png')

# plt.figure(figsize=(20, 10))
# bars = plt.bar(df['Points'], df['Processing_Time'], color=colors, align='center', width=1)
# # Label only min and max bars
# for bar in bars:
#     height = bar.get_height()
#     if height == min_height or height == max_height:
#         plt.text(bar.get_x() + bar.get_width() / 2, height,
#                  f'{height:.2f}', ha='center', va='bottom', color='blue', fontsize=10, fontweight='bold')
        
# plt.title('OntoRaster Performance Benchmark (log scale)', fontsize=20, fontweight='bold')
# plt.yscale('log')  # Set y-axis to log scale
# plt.xticks(range(df['Points'].min(), df['Points'].max() + 1, 100))
# plt.xlabel('Varying Points of Polygon')
# plt.ylabel('Log Scale of Processing Time (seconds)')
# plt.grid(axis='y', which='both', linestyle='--', alpha=0.7)
# plt.tight_layout()
# plt.margins(x=0)
# plt.savefig('./benchmark_scripts/benchmark_bar_plot_log_scale.png')


# # Plot the results
# plt.figure(figsize=(25, 10))
# # sns.color_palette("icefire", as_cmap=True)
# # sns.barplot(data = df, x='Points', y='Processing_Time', palette="icefire")
# snscolors = sns.color_palette("Spectral_r", n_colors=len(df))
# ax = sns.barplot(data=df, x='Points', y='Processing_Time', palette=snscolors)
# plt.title('Processing Time by Points', fontsize=16, fontweight='bold', pad=20)
# plt.xlabel('Varying Points of Fixed Area Uniform Polygon', fontsize=12, labelpad=10)
# plt.ylabel('Processing Time (seconds)', fontsize=12, labelpad=10)
# plt.xticks(ticks=range(len(df)), labels=df['Points'], rotation=0)
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# sns.despine(left=False, bottom=False)
# plt.tight_layout()
# plt.margins(x=0)
# plt.savefig('./benchmark_scripts/benchmark_bar_plot_log_sns.png')


# plt.plot(df['Points'], df['Processing_Time'], color='red', marker='o', linestyle='')
# plt.title('OntoRaster Performance Benchmark', fontsize=20, fontweight='bold')
# plt.xticks(range(df['Points'].min(), df['Points'].max() + 1, XTICKS_BIN))
# plt.xlabel('Varying Points of Polygon', fontsize=15, fontweight='bold')
# plt.ylabel('Processing Time (seconds)', fontsize=15, fontweight='bold')
# plt.grid(True)
# plt.margins(x=0)
# # plt.savefig('./benchmark_scripts/benchmark_line_plot.png')

# Log-transform the y-values
log_y = np.log10(df['Processing_Time'])
x = df['Points']

# Fit a linear regression: log(y) = m*x + b
m, b = np.polyfit(x, log_y, 1)

# Calculate fitted values for the trend line (in log scale)
trend_log_y = m * x + b
trend_y = 10 ** trend_log_y  # Convert back to original scale

# Plot the bar chart
plt.figure(figsize=(20, 10))
barsh = plt.bar(x, df['Processing_Time'], color=colors, align='center', width=10)

# Add value labels on top of each bar
# for bar in bars:
#     height = bar.get_height()
#     plt.text(bar.get_x() + bar.get_width() / 2, height,
#              f'{height:.2f}', ha='center', va='bottom', fontsize=10)

# Label only min and max bars
for bar in barsh:
    height = bar.get_height()
    if height == min_height or height == max_height:
        plt.text(bar.get_x() + bar.get_width() / 2, height,
                 f'{height:.2f}', ha='center', va='bottom', color='blue', fontsize=10, fontweight='bold')
        
# Plot the trend line
plt.plot(x, trend_y, color='black', linestyle='--', label=f'Trend: log₁₀(y) = {m:.8f}x + {b:.2f}')
plt.yscale('log')
plt.title('Query Processing Time VS Varying Points of Fixed Area Uniform Polygon (Case 1)', fontsize=20, fontweight='bold')
plt.xlabel('Points', fontsize=15, fontweight='bold')
plt.ylabel('Log Scale Time (seconds)', fontsize=15, fontweight='bold')
plt.xticks(range(df['Points'].min(), df['Points'].max() + 1, XTICKS_BIN), fontsize=12, rotation=35)
plt.yticks(fontsize=15)
plt.grid(axis='y', which='both', linestyle='--', alpha=0.7)
plt.legend(loc='upper right', borderaxespad=0)
plt.tight_layout()
plt.margins(x=0)
plt.savefig('./benchmark_scripts/bm1_log_scale20000.png')
plt.show()

# print("Benchmark completed and saved to CSV and PNG files.")