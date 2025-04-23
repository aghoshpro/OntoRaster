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

sparql = SPARQLWrapper("http://localhost:8082/sparql")
sparql.setReturnFormat(JSON)

def genPolygonPointsFIXED(input_bbox, num_points=None):
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
    
    # Double-check OGC compliance
    is_valid, message = validate_ogc_polygon(wkt)
    if not is_valid:
        # print("Polygon is not OGC compliant. Attempting to fix...")
        wkt = fix_ogc_polygon(wkt)
        
    return wkt

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
    # if area_percentage is None:
    #     area_percentage = random.uniform(0.1, 1.0)
    
    # if num_points is None:
    #     num_points = random.randint(3, 20)
    
    # Get bbox dimensions
    bbox_width = max_lon - min_lon
    bbox_height = max_lat - min_lat
    
    # Calculate center of bbox
    center_lon = (min_lon + max_lon) / 2
    center_lat = (min_lat + max_lat) / 2

    # Calculate anywhere of bbox
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
input_bbox = [11.360694444453532, 48.06152777781623, 11.723194444453823, 48.24819444448305] ## Munich
NUM_OF_POINTS = 50003 # 1,2 points are not polygon
PERCENTAGE_OF_AREA = 0.25
XTICKS_BIN = 1000
# Create a list to store benchmark results
benchmark_data = []

# Run benchmarks with increasing LIMIT values
point_values = list(range(3, NUM_OF_POINTS, 1000))  # 10, 20, 30, ... 100

for point in tqdm(point_values):
    try:
        # simple_poly_fixed = genPolygonPointsFIXED(input_bbox, point)
        sample_polygon = genPolygon_AreaFIXED(input_bbox, point, area_percentage=PERCENTAGE_OF_AREA)
        # print(simple_poly_fixed)
        time_taken = benchmark(sample_polygon)
        # sample_polygon = None
        del sample_polygon
        gc.collect()
        benchmark_data.append({'Points': point, 'Processing_Time': time_taken})
        # print(f"Points {point}: {time_taken:.4f} sec")
        # print(simple_poly_fixed)
    except Exception as e:
        print(f"Error with Points {point}: {e}")

# Create a pandas DataFrame from the benchmark data
df = pd.DataFrame(benchmark_data)
## Save the benchmark data to a CSV file
df.to_csv('./benchmark_scripts/sparql_benchmark_results.csv', index=False)

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
plt.figure(figsize=(25, 10))
bars = plt.bar(df['Points'], df['Processing_Time'], align='center', color=colors, width=999)
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
plt.savefig('./benchmark_scripts/benchmark_bar_plot.png')

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
plt.figure(figsize=(25, 10))
barsh = plt.bar(x, df['Processing_Time'], color=colors, align='center', width=999)

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
plt.savefig('./benchmark_scripts/benchmark_line_plot_log_scale_trend.png')
plt.show()

# print("Benchmark completed and saved to CSV and PNG files.")