from SPARQLWrapper import SPARQLWrapper, JSON, POST
import time
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import numpy as np
from tqdm import tqdm

from shapely.geometry import Polygon, box
from shapely import wkt
from shapely.ops import transform
from pyproj import Transformer

# sparql = SPARQLWrapper("http://localhost:8082/sparql")
# sparql.setReturnFormat(JSON)

# def calculateArea(poly_wkt_str):
#     polygon = wkt.loads(poly_wkt_str)
#     area_sq_degrees = polygon.area
#     centroid = polygon.centroid
#     lon, lat = centroid.x, centroid.y
#     utm_zone = int((lon + 180) / 6) + 1
#     proj_string = f"+proj=utm +zone={utm_zone} +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
#     # # Set up the transformation
#     transformer = Transformer.from_crs("EPSG:4326", proj_string, always_xy=True)
#     utm_polygon = transform(transformer.transform, polygon)
#     area_sq_meters = utm_polygon.area
#     area_sq_kilometers = area_sq_meters / 1_000_000  # Convert to square kilometers
#     return float(format(area_sq_kilometers, '.2f'))

# def genPolygonExp(INPUT_BBOX, NUM_OF_POINTS, AREA_IN_km, UNIFORM_FACTOR):
#     """
#     Generate a polygon with specified area in square kilometers
    
#     Parameters:
#     INPUT_BBOX: WKT string representing the bounding box
#     NUM_OF_POINTS: Number of points in the polygon
#     AREA_IN_km²: Target area in square kilometers
#     UNIFORM_FACTOR: Controls shape regularity (0.0: very irregular, 1.0: perfectly regular)
    
#     Returns:
#     WKT string representing the generated polygon in EPSG:4326
#     """
#     # Parse the bounding box
#     if type(INPUT_BBOX) == str:
#         bbox = wkt.loads(INPUT_BBOX)
#         bbox_bounds = bbox.bounds
#         min_x, min_y, max_x, max_y = bbox_bounds
#     else:
#         min_x, min_y, max_x, max_y = INPUT_BBOX
#         bbox = wkt.loads((box(*INPUT_BBOX, ccw=True)).wkt)
    
#     # Compute the centroid for UTM zone determination
#     centroid_x = (min_x + max_x) / 2
#     centroid_y = (min_y + max_y) / 2
    
#     # Determine UTM zone
#     utm_zone = int((centroid_x + 180) / 6) + 1
#     proj_string = f"+proj=utm +zone={utm_zone} +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
    
#     # Create transformers for WGS84 <-> UTM conversion
#     transformer_to_utm = Transformer.from_crs("EPSG:4326", proj_string, always_xy=True)
#     transformer_from_utm = Transformer.from_crs(proj_string, "EPSG:4326", always_xy=True)
    
#     # Transform the bounding box to UTM
#     utm_bbox = transform(transformer_to_utm.transform, bbox)
#     utm_bounds = utm_bbox.bounds
#     utm_min_x, utm_min_y, utm_max_x, utm_max_y = utm_bounds
    
#     # Calculate the center point of the bounding box in UTM
#     center_x = (utm_min_x + utm_max_x) / 2
#     center_y = (utm_min_y + utm_max_y) / 2
    
#     # Calculate the radius needed for the target area
#     # For a regular polygon with n sides, area = (n/4) * r² * sin(2π/n)
#     # Solving for r: r = sqrt(area / ((n/4) * sin(2π/n)))
#     target_area_m2 = AREA_IN_km * 1_000_000  # Convert km² to m²
    
#     # For a regular polygon, calculate the radius
#     n = NUM_OF_POINTS
#     regular_radius = math.sqrt(target_area_m2 / ((n/4) * math.sin(2 * math.pi / n)))
    
#     # Generate points for the polygon
#     angles = np.linspace(0, 2 * np.pi, NUM_OF_POINTS, endpoint=False)
    
#     utm_points = []
#     for angle in angles:
#         # Start with perfectly regular distance (radius)
#         base_distance = regular_radius
        
#         # Add randomness based on the uniformity factor
#         if UNIFORM_FACTOR < 1.0:
#             # The lower the uniformity factor, the more randomness
#             random_variation = (1.0 - UNIFORM_FACTOR) * random.uniform(0.5, 1.5)
#             distance = base_distance * (1.0 + (1.0 - UNIFORM_FACTOR) * (random_variation - 1.0))
#         else:
#             distance = base_distance
        
#         # Calculate point coordinates
#         x = center_x + distance * np.cos(angle)
#         y = center_y + distance * np.sin(angle)
#         utm_points.append((x, y))
    
#     # Create the polygon in UTM
#     utm_polygon = Polygon(utm_points)
    
#     # Calculate the area of the generated polygon
#     initial_area_m2 = utm_polygon.area
    
#     # Scale the polygon to match the target area
#     scaling_factor = math.sqrt(target_area_m2 / initial_area_m2)
    
#     # Apply scaling: translate to origin, scale, translate back
#     def scale_around_center(x, y):
#         dx = x - center_x
#         dy = y - center_y
#         return center_x + dx * scaling_factor, center_y + dy * scaling_factor
    
#     scaled_utm_polygon = transform(lambda x, y: scale_around_center(x, y), utm_polygon)
    
#     # Transform the UTM polygon back to WGS84 (EPSG:4326)
#     wgs84_polygon = transform(transformer_from_utm.transform, scaled_utm_polygon)
    
#     # Return the WKT representation
#     return wgs84_polygon.wkt

# def validate_ogc_polygon(wkt):
#     """
#     Validate that a polygon in WKT format is OGC compliant
    
#     Args:
#         wkt: WKT format polygon string
        
#     Returns:
#         tuple: (is_valid, message) where is_valid is a boolean and message describes any issues
#     """
#     try:
#         from shapely import wkt as shapely_wkt
#         import shapely.geometry
        
#         # Parse the WKT string
#         polygon = shapely_wkt.loads(wkt)
        
#         # Check if the geometry is a polygon
#         if not isinstance(polygon, shapely.geometry.Polygon):
#             return False, "Not a polygon geometry"
        
#         # Check if the polygon is valid according to OGC
#         if not polygon.is_valid:
#             reason = shapely.validation.explain_validity(polygon)
#             return False, f"Invalid polygon: {reason}"
        
#         # Check if the exterior ring is clockwise
#         exterior_ring = polygon.exterior
#         is_ext_clockwise = is_clockwise(exterior_ring.coords)
#         if not is_ext_clockwise:
#             return False, "Exterior ring is not clockwise (OGC requires clockwise)"
        
#         # Check if interior rings (holes) are counterclockwise
#         for interior in polygon.interiors:
#             if is_clockwise(interior.coords):
#                 return False, "Interior ring (hole) is not counterclockwise (OGC requires counterclockwise)"
        
#         # Check for self-intersections
#         if not polygon.is_simple:
#             return False, "Polygon has self-intersections"
        
#         return True, "Polygon is OGC compliant"
        
#     except ImportError:
#         return False, "Validation requires shapely package"
#     except Exception as e:
#         return False, f"Validation error: {str(e)}"

# def is_clockwise(coordinates):
#     """
#     Determine if a ring is clockwise by calculating the signed area
    
#     Args:
#         coordinates: List of (x, y) coordinates representing a ring
        
#     Returns:
#         boolean: True if clockwise, False if counterclockwise
#     """
#     # Shoelace formula to compute the signed area
#     area = 0.0
#     for i in range(len(coordinates) - 1):  # -1 because the last point is the same as the first
#         j = (i + 1) % (len(coordinates) - 1)
#         area += coordinates[i][0] * coordinates[j][1]
#         area -= coordinates[j][0] * coordinates[i][1]
    
#     # If area is positive, the ring is counterclockwise
#     # If area is negative, the ring is clockwise
#     return area < 0

# def fix_ring_orientation(coordinates, should_be_clockwise=True):
#     """
#     Fix the orientation of a ring to be clockwise or counterclockwise
    
#     Args:
#         coordinates: List of (x, y) coordinates representing a ring
#         should_be_clockwise: Boolean, True if the ring should be clockwise
        
#     Returns:
#         list: Coordinates in the correct orientation
#     """
#     is_clock = is_clockwise(coordinates)
    
#     if (should_be_clockwise and not is_clock) or (not should_be_clockwise and is_clock):
#         # Reverse the order of the coordinates, but keep the first/last point the same
#         fixed = coordinates[:1] + coordinates[1:-1][::-1] + coordinates[-1:]
#         return fixed
    
#     return coordinates

# def fix_ogc_polygon(wkt):
#     """
#     Fix common OGC compliance issues in a polygon
    
#     Args:
#         wkt: WKT format polygon string
        
#     Returns:
#         string: Fixed WKT polygon or the original if it cannot be fixed
#     """
#     try:
#         from shapely import wkt as shapely_wkt
#         import shapely.geometry
        
#         # Parse the WKT string
#         polygon = shapely_wkt.loads(wkt)
        
#         if not isinstance(polygon, shapely.geometry.Polygon):
#             return wkt  # Can't fix non-polygons
        
#         # Fix self-intersections and other validity issues
#         if not polygon.is_valid:
#             polygon = polygon.buffer(0)  # This often fixes invalid polygons
        
#         # Fix ring orientations
#         exterior_coords = list(polygon.exterior.coords)
#         fixed_exterior = fix_ring_orientation(exterior_coords, True)  # Exterior should be clockwise
        
#         fixed_interiors = []
#         for interior in polygon.interiors:
#             interior_coords = list(interior.coords)
#             fixed_interior = fix_ring_orientation(interior_coords, False)  # Interior should be counterclockwise
#             fixed_interiors.append(fixed_interior)
        
#         # Reconstruct the WKT
#         wkt = "POLYGON (("
#         wkt += ", ".join([f"{p[0]} {p[1]}" for p in fixed_exterior])
#         wkt += ")"
        
#         for interior in fixed_interiors:
#             wkt += ", ("
#             wkt += ", ".join([f"{p[0]} {p[1]}" for p in interior])
#             wkt += ")"
        
#         wkt += ")"
        
#         return wkt
        
#     except Exception as e:
#         print(f"Error fixing polygon: {e}")
#         return wkt  # Return the original if we can't fix it
    
# def benchmark(poly):
#     """
#     Records the query processing time for a SPARQL query with different LIMIT values.
    
#     Args:
#         point: The LIMIT value for the SPARQL query
        
#     Returns:
#         float: The time taken to execute the query in seconds
#     """
#     query = f"""
#         PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
#         PREFIX rdfs:	<http://www.w3.org/2000/01/rdf-schema#>
#         PREFIX geo:	<http://www.opengis.net/ont/geosparql#>
#         PREFIX rasdb:	<https://github.com/aghoshpro/RasterDataCube/>

#         SELECT ?clipped {{
#         ?gridCoverage a :Raster .
#         ?gridCoverage rasdb:rasterName ?rasterName .
#         FILTER (CONTAINS(?rasterName, 'Elevation')) 
#         BIND ('{poly}'^^geo:wktLiteral AS ?customRegionWkt)
#         BIND ('2000-02-11T00:00:00+00:00'^^xsd:dateTime AS ?timeStamp)
#         BIND (rasdb:rasSpatialAverage(?timeStamp, ?customRegionWkt, ?rasterName) AS ?clipped) 
#         }}
#     """
    
#     sparql.setQuery(query)
#     sparql.setMethod(POST) # ro avoid the following error SPARQLWrapper.SPARQLExceptions.QueryBadFormed: QueryBadFormed: A bad request has been sent to the endpoint: probably the SPARQL query is badly formed.
#     # Measure the query execution time
#     start_time = time.time()
#     results = sparql.query()
#     end_time = time.time()
#     # Calculate the processing time
#     processing_time = end_time - start_time
#     return processing_time

# random.seed(777) # OR np.random.seed(42)  # For reproducibility
# # input_bbox = [11.015629, 55.128649, 24.199222, 69.380313] ## Sweden
# INPUT_BBOX = [11.360694444453532, 48.06152777781623, 11.723194444453823, 48.24819444448305] # MUNICH
# INPUT_BBOX_WKT_STRING = (box(*INPUT_BBOX, ccw=True)).wkt
# NUM_OF_POINTS = 10004 
# AREA_IN_km = 500 
# UNIFORM_FACTOR = 0.9
XTICKS_BIN = 1000
STEPS = 100

# bm500_data = []

# bm1_data = []

# bm11_data = []

# bm111_data = []

# bm1111_data = []

# bm11111_data = []

# for point in tqdm(range(3, NUM_OF_POINTS, STEPS)):
#     try:
#         poly_bm500 = genPolygonExp(INPUT_BBOX, point, 500, UNIFORM_FACTOR)
#         time_taken = benchmark(poly_bm500)
#         bm500_data.append({'Points': point, 'Processing_Time': time_taken})
#         del time_taken
#         del poly_bm500
#         poly_bm1 = genPolygonExp(INPUT_BBOX, point, 250, UNIFORM_FACTOR)
#         time_taken = benchmark(poly_bm1)
#         bm1_data.append({'Points': point, 'Processing_Time': time_taken})
#         del time_taken
#         del poly_bm1
#         poly_bm11 = genPolygonExp(INPUT_BBOX, point, 100, UNIFORM_FACTOR)
#         time_taken = benchmark(poly_bm11)
#         bm11_data.append({'Points': point, 'Processing_Time': time_taken})
#         del time_taken
#         del poly_bm11
#         poly_bm111 = genPolygonExp(INPUT_BBOX, point, 50, UNIFORM_FACTOR)
#         time_taken = benchmark(poly_bm111)
#         bm111_data.append({'Points': point, 'Processing_Time': time_taken})
#         del time_taken
#         del poly_bm111
#         poly_bm1111 = genPolygonExp(INPUT_BBOX, point, 25, UNIFORM_FACTOR)
#         time_taken = benchmark(poly_bm1111)
#         bm1111_data.append({'Points': point, 'Processing_Time': time_taken})
#         del time_taken
#         del poly_bm1111
#         poly_bm11111 = genPolygonExp(INPUT_BBOX, point, 5, UNIFORM_FACTOR)
#         time_taken = benchmark(poly_bm11111)
#         bm11111_data.append({'Points': point, 'Processing_Time': time_taken})
#         del time_taken
#         del poly_bm11111
#     except Exception as e:
#         print(f"Error with Points {point}: {e}")

# bm500 = pd.DataFrame(bm500_data)
# bm500.to_csv('./benchmark_scripts/bm500_100.csv', index=False)

# bm1 = pd.DataFrame(bm1_data)
# bm1.to_csv('./benchmark_scripts/bm1_100.csv', index=False)

# bm11 = pd.DataFrame(bm11_data)
# bm11.to_csv('./benchmark_scripts/bm11_100.csv', index=False)

# bm111 = pd.DataFrame(bm111_data)
# bm111.to_csv('./benchmark_scripts/bm111_100.csv', index=False)

# bm1111 = pd.DataFrame(bm1111_data)
# bm1111.to_csv('./benchmark_scripts/bm1111_100.csv', index=False)

# bm11111 = pd.DataFrame(bm11111_data)
# bm11111.to_csv('./benchmark_scripts/bm11111_100.csv', index=False)

# del point
# del time_taken

# bm1_data = []
# # point_values = list(range(3, NUM_OF_POINTS, 10000))  # 10, 20, 30, ... 100

# for point in tqdm(range(3, NUM_OF_POINTS, STEPS)):
#     try:
#         poly_bm1 = genPolygonExp(INPUT_BBOX, point, 250, UNIFORM_FACTOR)
#         time_taken = benchmark(poly_bm1)
#         bm1_data.append({'Points': point, 'Processing_Time': time_taken})
#     except Exception as e:
#         print(f"Error with Points {point}: {e}")



# del point
# del time_taken

# bm11_data = []
# for point in tqdm(range(3, NUM_OF_POINTS, STEPS)):
#     try:
#         poly_bm11 = genPolygonExp(INPUT_BBOX, point, 100, UNIFORM_FACTOR)
#         time_taken = benchmark(poly_bm11)
#         bm11_data.append({'Points': point, 'Processing_Time': time_taken})
#     except Exception as e:
#         print(f"Error with Points {point}: {e}")



# del point
# del time_taken

# bm111_data = []
# for point in tqdm(range(3, NUM_OF_POINTS, STEPS)):
#     try:
#         poly_bm111 = genPolygonExp(INPUT_BBOX, point, 50, UNIFORM_FACTOR)
#         time_taken = benchmark(poly_bm111)
#         bm111_data.append({'Points': point, 'Processing_Time': time_taken})
#     except Exception as e:
#         print(f"Error with Points {point}: {e}")

# bm111 = pd.DataFrame(bm111_data)
# bm111.to_csv('./benchmark_scripts/bm111_100.csv', index=False)

# del point
# del time_taken

# bm1111_data = []
# for point in tqdm(range(3, NUM_OF_POINTS, STEPS)):
#     try:
#         poly_bm1111 = genPolygonExp(INPUT_BBOX, point, 25, UNIFORM_FACTOR)
#         time_taken = benchmark(poly_bm1111)
#         bm1111_data.append({'Points': point, 'Processing_Time': time_taken})
#     except Exception as e:
#         print(f"Error with Points {point}: {e}")

# bm1111 = pd.DataFrame(bm1111_data)
# bm1111.to_csv('./benchmark_scripts/bm1111_100.csv', index=False)


# del point
# del time_taken

# bm11111_data = []
# for point in tqdm(range(3, NUM_OF_POINTS, STEPS)):
#     try:
#         poly_bm11111 = genPolygonExp(INPUT_BBOX, point, 5, UNIFORM_FACTOR)
#         time_taken = benchmark(poly_bm11111)
#         bm11111_data.append({'Points': point, 'Processing_Time': time_taken})
#     except Exception as e:
#         print(f"Error with Points {point}: {e}")

# bm11111 = pd.DataFrame(bm11111_data)
# bm11111.to_csv('./benchmark_scripts/bm11111_100.csv', index=False)

# bm500 = pd.read_csv('./benchmark_scripts/results/1/bm500_100.csv')
# bm1 = pd.read_csv('./benchmark_scripts//results/1/bm1_100.csv')
# bm11 = pd.read_csv('./benchmark_scripts/results/1/bm11_100.csv')
# bm111 = pd.read_csv('./benchmark_scripts/results/1/bm111_100.csv')
# bm1111 = pd.read_csv('./benchmark_scripts/results/1/bm1111_100.csv')
# bm11111 = pd.read_csv('./benchmark_scripts/results/1/bm11111_100.csv')

bm500_2 = pd.read_csv('./benchmark_scripts/results/2/bm500_100.csv')
bm12 = pd.read_csv('./benchmark_scripts//results/2/bm1_100.csv')
bm112 = pd.read_csv('./benchmark_scripts/results/2/bm11_100.csv')
bm1112 = pd.read_csv('./benchmark_scripts/results/2/bm111_100.csv')
bm11112 = pd.read_csv('./benchmark_scripts/results/2/bm1111_100.csv')
bm111112 = pd.read_csv('./benchmark_scripts/results/2/bm11111_100.csv')

# bm500_3 = pd.read_csv('./benchmark_scripts/results/3/bm500_NDVI.csv')
# bm13 = pd.read_csv('./benchmark_scripts//results/3/bm1_NDVI.csv')
# bm113 = pd.read_csv('./benchmark_scripts/results/3/bm11_NDVI.csv')
# bm1113 = pd.read_csv('./benchmark_scripts/results/3/bm111_NDVI.csv')
# bm11113 = pd.read_csv('./benchmark_scripts/results/3/bm1111_NDVI.csv')
# bm111113 = pd.read_csv('./benchmark_scripts/results/3/bm11111_NDVI.csv')

# bm500_4 = pd.read_csv('./benchmark_scripts/results/4/bm500_NDVI.csv') # SNOW
# bm14 = pd.read_csv('./benchmark_scripts//results/4/bm1_NDVI.csv')
# bm114 = pd.read_csv('./benchmark_scripts/results/4/bm11_NDVI.csv')
# bm1114 = pd.read_csv('./benchmark_scripts/results/4/bm111_NDVI.csv')
# bm11114 = pd.read_csv('./benchmark_scripts/results/4/bm1111_NDVI.csv')
# bm111114 = pd.read_csv('./benchmark_scripts/results/4/bm11111_NDVI.csv')


bm500_5 = pd.read_csv('./benchmark_scripts/results/5/bm500_time.csv')
bm15 = pd.read_csv('./benchmark_scripts//results/5/bm1_time.csv')
bm115 = pd.read_csv('./benchmark_scripts/results/5/bm11_time.csv')
bm1115 = pd.read_csv('./benchmark_scripts/results/5/bm111_time.csv')
bm11115 = pd.read_csv('./benchmark_scripts/results/5/bm1111_time.csv')
bm111115 = pd.read_csv('./benchmark_scripts/results/5/bm11111_time.csv')


#y_min = np.min(np.array[np.array([bm500['Processing_Time'].min, bm1['Processing_Time'].min, bm11['Processing_Time'].min, bm111['Processing_Time'].min, bm1111['Processing_Time'].min, bm11111['Processing_Time'].min])])
# y_max = max(bm500['Processing_Time'].max, bm1['Processing_Time'].max, bm11['Processing_Time'].max, bm111['Processing_Time'].max, bm1111['Processing_Time'].max, bm11111['Processing_Time'].max)

# List of all dataframes you want to plot
dataframes = [bm500_2, bm12, bm112, bm1112, bm11112, bm111112, bm500_5, bm15, bm115, bm1115, bm11115, bm111115] #, bm500_2, bm12, bm112, bm1112, bm11112, bm111112, bm500_3, bm13, bm113, bm1113, bm11113, bm111113, bm500_4, bm14, bm114, bm1114, bm11114, bm111114]
# titles = ['500 km² (R1)', '250 km² (R1)', '100 km² (R1)', '50 km² (R1)', '25 km² (R1)', '5 km² (R1)', '500 km² (R2)', '250 km² (R2)', '100 km² (R2)', '50 km² (R2)', '25 km² (R2)', '5 km² (R2)', '500 km² (R3)', '250 km² (R3)', '100 km² (R3)', '50 km² (R3)', '25 km² (R3)', '5 km² (R3)', '500 km² (R4)', '250 km² (R4)', '100 km² (R4)', '50 km² (R4)', '25 km² (R4)', '5 km² (R4)']

titles = ['500 km² (R2)', '250 km² (R2)', '100 km² (R2)', '50 km² (R2)', '25 km² (R2)', '5 km² (R2)', '500 km² (R2)', '250 km² (R2)', '100 km² (R2)', '50 km² (R2)', '25 km² (R2)', '5 km² (R2)']#, '500 km² (R3)', '250 km² (R3)', '100 km² (R3)', '50 km² (R3)', '25 km² (R3)', '5 km² (R3)', '500 km² (R4)', '250 km² (R4)', '100 km² (R4)', '50 km² (R4)', '25 km² (R4)', '5 km² (R4)']


y_min = min(df['Processing_Time'].min() for df in dataframes)
y_max = max(df['Processing_Time'].max() for df in dataframes)


# Calculate the grid dimensions
n = len(dataframes)
cols = 6
rows = int(np.ceil(n / cols))

# Create figure and subplots
fig, axes = plt.subplots(rows, cols, figsize=(20, 10))
axes = axes.flatten()  # Flatten to easily iterate through axes

# Plot each dataframe as a bar plot in its respective subplot
for i, (df, title) in enumerate(zip(dataframes, titles)):
    if i < len(axes):  # Make sure we don't exceed the number of available subplots
        colors = ['green' if t == df['Processing_Time'].min() else 'red' if t == df['Processing_Time'].max() else 'deepskyblue' for t in df['Processing_Time']]
        # df.plot(kind='bar', ax=axes[i])
        # axes[i].bar(df['Points'], df['Processing_Time'], color=colors, alpha=0.7)
        axes[i].bar(df['Points'], df['Processing_Time'],color=colors, alpha=0.7,  width=STEPS)
        axes[i].set_title(title, fontsize=15, fontweight='bold')
        axes[i].set_xticks(range(df['Points'].min(), df['Points'].max() + 1, XTICKS_BIN), fontsize=15, fontweight='bold', rotation = 35)
        # axes[i].set_yticks(df['Processing_Time'], fontsize=15)
        axes[i].set_yticks(np.arange(df['Processing_Time'].min(), df['Processing_Time'].max(), 0.5),  fontsize=15, fontweight='bold')
        # axes[i].set_xlabel('Points', fontsize=15, fontweight='bold')
        # axes[i].set_ylabel('Time (seconds)', fontsize=15, fontweight='bold')
        # axes[i].legend(loc='upper right')
        axes[i].grid(True, axis='y', linestyle='--', alpha=0.7)
        axes[i].margins(x=0)
        # axes[i].set_ylim(0, 2.0)
        axes[i].set_xlim(3, 5003)
        # axes[i].set_yscale('log')
# Hide any empty subplots
for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)

# plt.tight_layout(rect=[0, 0, 0, 0]) 
plt.tight_layout(rect=[0.044, 0.03, 0.98, 0.922])  # Adjust bottom, left, right, top
fig.suptitle('Polygon vs Raster R2: Temp (1000m) (SPATIAL and TEMPORAL)', fontsize=20, fontweight='bold')
# fig.suptitle('Polygon vs Raster R1: DEM (30m) | R2: TEMP (1km) | R3: NDVI (250m) | R4: Snow (500m)', fontsize=20, fontweight='bold')


# del fig
# del axes

# y_min_log = min(min(np.log10(df['Processing_Time'])) for df in dataframes)
# y_max_log = max(max(np.log10(df['Processing_Time'])) for df in dataframes)


# fig, axes = plt.subplots(rows, cols, figsize=(20, 10))
# axes = axes.flatten()  # Flatten to easily iterate through axes

# # Plot each dataframe as a bar plot in its respective subplot
# for i, (df, title) in enumerate(zip(dataframes, titles)):
#     if i < len(axes):  # Make sure we don't exceed the number of available subplots
#         # Log-transform the y-values
#         log_y = np.log10(df['Processing_Time'])
#         x = df['Points']
#         m, b = np.polyfit(x, log_y, 1)
#         trend_log_y = m * x + b
#         trend_y = 10 ** trend_log_y  

#         colors = ['green' if t == df['Processing_Time'].min() else 'red' if t == df['Processing_Time'].max() else 'deepskyblue' for t in df['Processing_Time']]
#         axes[i].bar(x, trend_y,color=colors, alpha=0.7,  width=STEPS)
#         axes[i].set_title(title, fontsize=15, fontweight='bold')
#         axes[i].set_xticks(range(df['Points'].min(), df['Points'].max() + 1, XTICKS_BIN), fontsize=15, fontweight='bold', rotation = 35)
#         axes[i].set_yticks(np.arange(np.min(trend_y), np. max(trend_y), 0.5),  fontsize=15, fontweight='bold')
#         # axes[i].set_xlabel('Points', fontsize=15, fontweight='bold')
#         # axes[i].set_ylabel('Time (seconds)', fontsize=15, fontweight='bold')
#         axes[i].grid(True, axis='y', linestyle='--', alpha=0.7)
#         axes[i].margins(x=0)
#         axes[i].set_xlim(3, 5003)
#         axes[i].set_ylim(0.0, 5.0)
#         # print(y_min_log, y_max_log)
# # Hide any empty subplots
# for j in range(i + 1, len(axes)):
#     axes[j].set_visible(False)

# plt.tight_layout(rect=[0, 0, 0, 0.05])  # Adjust bottom, left, right, top
# fig.suptitle('POLYGON ( 100 points | 0.9 uniformity)', fontsize=20, fontweight='bold')
# plt.yscale('log')
plt.show()