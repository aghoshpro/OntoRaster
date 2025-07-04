from SPARQLWrapper import SPARQLWrapper, JSON, POST
import time
import pandas as pd
import random
from tqdm import tqdm
import psutil
import gc
import docker


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
    
def monitor_memory_usage():
    """Monitor local Python memory usage"""
    process = psutil.Process()
    memory_info = process.memory_info()
    print(f"Python Memory Usage: {memory_info.rss / 1024 / 1024:.2f} MB")

def benchmark(poly):
    """
    Records the query processing time for a SPARQL query with different LIMIT values.
    
    Args:
        point: The LIMIT value for the SPARQL query
        
    Returns:
        float: The time taken to execute the query in seconds
    """
    queryElevation = f"""
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

    queryTEMP_S = f"""
        PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
        PREFIX rdfs:	<http://www.w3.org/2000/01/rdf-schema#>
        PREFIX geo:	<http://www.opengis.net/ont/geosparql#>
        PREFIX rasdb:	<https://github.com/aghoshpro/RasterDataCube/>

        SELECT ?clipped {{
        ?gridCoverage a :Raster .
        ?gridCoverage rasdb:rasterName ?rasterName .
        FILTER (CONTAINS(?rasterName, 'Munich_MODIS_Temperature_1km')) 
        BIND ('{poly}'^^geo:wktLiteral AS ?customRegionWkt)
        BIND ('2022-01-01T00:00:00+00:00'^^xsd:dateTime AS ?timeStamp)
        BIND (rasdb:rasSpatialAverage(?timeStamp, ?customRegionWkt, ?rasterName) AS ?clipped) 
        }}
    """

    queryTEMP_ST = f"""
        PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
        PREFIX rdfs:	<http://www.w3.org/2000/01/rdf-schema#>
        PREFIX geo:	<http://www.opengis.net/ont/geosparql#>
        PREFIX rasdb:	<https://github.com/aghoshpro/RasterDataCube/>

        SELECT ?clipped {{
        ?gridCoverage a :Raster .
        ?gridCoverage rasdb:rasterName ?rasterName .
        FILTER (CONTAINS(?rasterName, 'Munich_MODIS_Temperature_1km')) 
        BIND ('{poly}'^^geo:wktLiteral AS ?customRegionWkt)
        BIND ('2022-01-01T00:00:00+00:00'^^xsd:dateTime AS ?startTimeStamp)
        BIND ('2022-02-01T00:00:00+00:00'^^xsd:dateTime AS ?endTimeStamp)
        BIND (rasdb:rasTemporalAverage(?startTimeStamp, ?endTimeStamp , ?regionWkt, ?rasterName) AS ?answer)
        }}
     """
    
    queryNDVI = f"""
        PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
        PREFIX rdfs:	<http://www.w3.org/2000/01/rdf-schema#>
        PREFIX geo:	<http://www.opengis.net/ont/geosparql#>
        PREFIX rasdb:	<https://github.com/aghoshpro/RasterDataCube/>

        SELECT ?clipped {{
        ?gridCoverage a :Raster .
        ?gridCoverage rasdb:rasterName ?rasterName .
        FILTER (CONTAINS(?rasterName, 'NDVI')) 
        BIND ('{poly}'^^geo:wktLiteral AS ?customRegionWkt)
        BIND ('2022-01-01T00:00:00+00:00'^^xsd:dateTime AS ?timeStamp)
        BIND (rasdb:rasSpatialAverage(?timeStamp, ?customRegionWkt, ?rasterName) AS ?clipped) 
        }}
    """
    querySNOW = f"""
        PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
        PREFIX rdfs:	<http://www.w3.org/2000/01/rdf-schema#>
        PREFIX geo:	<http://www.opengis.net/ont/geosparql#>
        PREFIX rasdb:	<https://github.com/aghoshpro/RasterDataCube/>

        SELECT ?clipped {{
        ?gridCoverage a :Raster .
        ?gridCoverage rasdb:rasterName ?rasterName .
        FILTER (CONTAINS(?rasterName, 'Snow')) 
        BIND ('{poly}'^^geo:wktLiteral AS ?customRegionWkt)
        BIND ('2023-12-20T00:00:00+00:00'^^xsd:dateTime AS ?timeStamp)
        BIND (rasdb:rasSpatialAverage(?timeStamp, ?customRegionWkt, ?rasterName) AS ?clipped) 
        }}
    """

    queryOSM= f"""
        PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
        PREFIX geo:	<http://www.opengis.net/ont/geosparql#>
        PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
        PREFIX rdfs:	<http://www.w3.org/2000/01/rdf-schema#>
        PREFIX lgdo: <http://linkedgeodata.org/ontology/>
        PREFIX rasdb:	<https://github.com/aghoshpro/RasterDataCube/>

        SELECT ?clipped {{
        ?building a lgdo:Residential ; geo:asWKT ?bldgWkt .
        ?gridCoverage a :Raster ; rasdb:rasterName ?rasterName .
        BIND ('{poly}'^^geo:wktLiteral AS ?customRegionWkt)
        FILTER (geof:sfWithin(?bldgWkt,?customRegionWkt))
        FILTER (CONTAINS(?rasterName, 'Munich_MODIS_Temperature_1km')) 
        BIND ('2022-01-01T00:00:00+00:00'^^xsd:dateTime AS ?timeStamp)
        BIND (rasdb:rasSpatialAverage(?timeStamp, ?customRegionWkt, ?rasterName) AS ?clipped) 
        }}
    """

    queryGeoNames= f"""
        PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
        PREFIX gn:  <https://www.geonames.org/ontology#>
        PREFIX geo:	<http://www.opengis.net/ont/geosparql#>
        PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
        PREFIX rdfs:	<http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rasdb:	<https://github.com/aghoshpro/RasterDataCube/>

        SELECT ?clipped {{
        ?gname a gn:RSTN; rdfs:label ?featureName ; geo:asWKT ?pointWkt .
        ?gridCoverage a :Raster ; rasdb:rasterName ?rasterName .
        BIND ('{poly}'^^geo:wktLiteral AS ?customRegionWkt)
        FILTER (geof:sfWithin(?pointWkt,?customRegionWkt))
        FILTER (CONTAINS(?rasterName, 'Munich_MODIS_Temperature_1km')) 
        BIND ('2022-01-01T00:00:00+00:00'^^xsd:dateTime AS ?timeStamp)
        BIND (rasdb:rasSpatialAverage(?timeStamp, ?customRegionWkt, ?rasterName) AS ?clipped) 
        }}
    """
    sparql.setMethod(POST)      # To avoid the SPARQLWrapper.SPARQLExceptions.QueryBadFormed: Error: A bad request has been sent to the endpoint: probably the SPARQL query is badly formed.
    sparql.setQuery(queryOSM)
    # Measure the query execution time
    start_time = time.time()
    sparql.query()
    end_time = time.time()
    # Calculate the processing time
    processing_time = end_time - start_time
    return processing_time


random.seed(777) # OR np.random.seed(42)  # For reproducibility
sparql = SPARQLWrapper("http://localhost:8082/sparql")
sparql.setReturnFormat(JSON)
# sparql.setMethod(POST)
# input_bbox = [11.015629, 55.128649, 24.199222, 69.380313] ## Sweden
# INPUT_BBOX = [11.360694444453532, 48.06152777781623, 11.723194444453823, 48.24819444448305] # MUNICH
# INPUT_BBOX_WKT_STRING = (box(*INPUT_BBOX, ccw=True)).wkt
client = docker.from_env()
ontop = client.containers.get('ontop')

NUM_OF_POINTS = 9904
# AREA_IN_km = 500 
# UNIFORM_FACTOR = 0.9
# XTICKS_BIN = 100
STEPS = 100


# df1= pd.read_pickle('./benchmark_scripts/notebooks/10000points_5km_uf5.pkl')
# df2= pd.read_pickle('./benchmark_scripts/notebooks/10000points_25km_uf5.pkl')
# df3= pd.read_pickle('./benchmark_scripts/notebooks/10000points_50km_uf5.pkl')
# df4= pd.read_pickle('./benchmark_scripts/notebooks/10000points_100km_uf5.pkl')
# df5= pd.read_pickle('./benchmark_scripts/notebooks/10000points_250km_uf5.pkl')
# df6= pd.read_pickle('./benchmark_scripts/notebooks/10000points_500km_uf5.pkl')
# df7= pd.read_pickle('./benchmark_scripts/notebooks/10000points_5km_uf5_1hole.pkl')
# df8 = pd.read_pickle('./benchmark_scripts/notebooks/10000points_25km_uf5_1hole.pkl')
# df9 = pd.read_pickle('./benchmark_scripts/notebooks/10000points_50km_uf5_1hole.pkl')
# df10 = pd.read_pickle('./benchmark_scripts/notebooks/10000points_100km_uf5_1hole.pkl')
# df11 = pd.read_pickle('./benchmark_scripts/notebooks/10000points_250km_uf5_1hole.pkl')
# df12 = pd.read_pickle('./benchmark_scripts/notebooks/10000points_500km_uf5_1hole.pkl')
# print(df6.head(5))
# print(len(df1))
# for point in tqdm(range(3, len(df1), STEPS)):
#     print(f" {point}---- {df1['points'][point]}")

# ontop.stop()
# ontop.start()
print("\n------ ONTOP Restarted #1 ---------\n")
# time.sleep(15)

# print("10000points_5km_uf5")

# df1= pd.read_pickle('./benchmark_scripts/notebooks/10000points_5km_uf5.pkl')

# df1_data = []

# for epoch in tqdm(range(0, NUM_OF_POINTS, STEPS)):
#     try:
#         time_taken = benchmark(df1['geometry'][epoch])
#         df1_data.append({'Points': df1['points'][epoch], 'Processing_Time': time_taken})
#     except Exception as e:
#         print(f"Error with Points {epoch}: {e}")

# bm1 = pd.DataFrame(df1_data)
# bm1.to_csv('./benchmark_scripts/paper/figOSM/Temp_10000points_5km_uf5_OSM_X.csv', index=False)

# del epoch
# del time_taken
# del df1
# gc.collect()

# ontop.stop()
# ontop.start()
# print("\n------ ONTOP Restarted #2 ---------\n")
# time.sleep(30) 


# print("10000points_25km_uf5")

# df2= pd.read_pickle('./benchmark_scripts/notebooks/10000points_25km_uf5.pkl')

# df2_data = []

# for epoch in tqdm(range(0, NUM_OF_POINTS, STEPS)):
#     try:
#         time_taken = benchmark(df2['geometry'][epoch])
#         df2_data.append({'Points': df2['points'][epoch], 'Processing_Time': time_taken})
#     except Exception as e:
#         print(f"Error with Points {epoch}: {e}")

# bm2 = pd.DataFrame(df2_data)
# bm2.to_csv('./benchmark_scripts/paper/figOSM/Temp_10000points_25km_uf5_OSM_X.csv', index=False)

# del epoch
# del time_taken
# del df2
# gc.collect()

# ontop.stop()
# ontop.start()
# print("\n------ ONTOP Restarted #3 ---------\n")
# time.sleep(30) 

print("10000points_50km_uf5")

df3= pd.read_pickle('./benchmark_scripts/notebooks/10000points_50km_uf5.pkl')

df3_data = []

for epoch in tqdm(range(0, NUM_OF_POINTS, STEPS)):
    try:
        time_taken = benchmark(df3['geometry'][epoch])
        df3_data.append({'Points': df3['points'][epoch], 'Processing_Time': time_taken})
    except Exception as e:
        print(f"Error with Points {epoch}: {e}")

bm3 = pd.DataFrame(df3_data)
bm3.to_csv('./benchmark_scripts/paper/figOSM/Temp_10000points_50km_uf5_OSM.csv', index=False)

del epoch
del time_taken
del df3
gc.collect()

ontop.stop()
ontop.start()
print("\n------ ONTOP Restarted #4 ---------\n")
time.sleep(30)

print("10000points_100km_uf5")

df4= pd.read_pickle('./benchmark_scripts/notebooks/10000points_100km_uf5.pkl')

df4_data = []

for epoch in tqdm(range(0, NUM_OF_POINTS, STEPS)):
    try:
        time_taken = benchmark(df4['geometry'][epoch])
        df4_data.append({'Points': df4['points'][epoch], 'Processing_Time': time_taken})
    except Exception as e:
        print(f"Error with Points {epoch}: {e}")

bm4 = pd.DataFrame(df4_data)
bm4.to_csv('./benchmark_scripts/paper/figOSM/Temp_10000points_100km_uf5_OSM.csv', index=False)

del epoch
del time_taken
del df4
gc.collect()

ontop.stop()
ontop.start()
print("\n------ ONTOP Restarted #5 ---------\n")
time.sleep(30) 

print("10000points_250km_uf5")

df5= pd.read_pickle('./benchmark_scripts/notebooks/10000points_250km_uf5.pkl')

df5_data = []

for epoch in tqdm(range(0, NUM_OF_POINTS, STEPS)):
    try:
        time_taken = benchmark(df5['geometry'][epoch])
        df5_data.append({'Points': df5['points'][epoch], 'Processing_Time': time_taken})
    except Exception as e:
        print(f"Error with Points {epoch}: {e}")

bm5 = pd.DataFrame(df5_data)
bm5.to_csv('./benchmark_scripts/paper/figOSM/Temp_10000points_250km_uf5_OSM.csv', index=False)

del epoch
del time_taken
del df5
gc.collect()

ontop.stop()
ontop.start()
print("\n------ ONTOP Restarted #6 ---------\n")
time.sleep(30) 

# print("10000points_500km_uf5")

# df6= pd.read_pickle('./benchmark_scripts/notebooks/10000points_500km_uf5.pkl')

# df6_data = []

# for epoch in tqdm(range(0, NUM_OF_POINTS, STEPS)):
#     try:
#         time_taken = benchmark(df6['geometry'][epoch])
#         df6_data.append({'Points': df6['points'][epoch], 'Processing_Time': time_taken})
#     except Exception as e:
#         print(f"Error with Points {epoch}: {e}")

# bm6 = pd.DataFrame(df6_data)
# bm6.to_csv('./benchmark_scripts/paper/figOSM/Temp_10000points_500km_uf5_OSM.csv', index=False)

# del epoch
# del time_taken
# del df6
# gc.collect()

# ontop.stop()
# ontop.start()
# print("\n------ ONTOP Restarted #7 ---------\n")
# time.sleep(15)

# print("10000points_5km_uf5_1hole")

# df7= pd.read_pickle('./benchmark_scripts/notebooks/10000points_5km_uf5_1hole.pkl')

# df7_data = []

# for epoch in tqdm(range(0, NUM_OF_POINTS, STEPS)):
#     try:
#         time_taken = benchmark(df7['geometry'][epoch])
#         df7_data.append({'Points': df7['points'][epoch], 'Processing_Time': time_taken})
#     except Exception as e:
#         print(f"Error with Points {epoch}: {e}")

# bm7 = pd.DataFrame(df7_data)
# bm7.to_csv('./benchmark_scripts/paper/fig2/Temp_10000points_5km_uf5_1hole_OSM.csv', index=False)

# del epoch
# del time_taken
# del df7
# gc.collect()


# print("10000points_25km_uf5_1hole")
# time.sleep(30) 

# df8 = pd.read_pickle('./benchmark_scripts/notebooks/10000points_25km_uf5_1hole.pkl')
# df8_data = []

# for epoch in tqdm(range(0, NUM_OF_POINTS, STEPS)):
#     try:
#         time_taken = benchmark(df8['geometry'][epoch])
#         df8_data.append({'Points': df8['points'][epoch], 'Processing_Time': time_taken})
#     except Exception as e:
#         print(f"Error with Points {epoch}: {e}")

# bm8 = pd.DataFrame(df8_data)
# bm8.to_csv('./benchmark_scripts/paper/fig2/Temp_10000points_25km_uf5_1hole_OSM.csv', index=False)

# del epoch
# del time_taken
# del df8
# gc.collect()



# print("10000points_50km_uf5_1hole")
# time.sleep(30) 

# df9 = pd.read_pickle('./benchmark_scripts/notebooks/10000points_50km_uf5_1hole.pkl')

# df9_data = []

# for epoch in tqdm(range(0, NUM_OF_POINTS, STEPS)):
#     try:
#         time_taken = benchmark(df9['geometry'][epoch])
#         df9_data.append({'Points': df9['points'][epoch], 'Processing_Time': time_taken})
#     except Exception as e:
#         print(f"Error with Points {epoch}: {e}")

# bm9 = pd.DataFrame(df9_data)
# bm9.to_csv('./benchmark_scripts/paper/fig2/Temp_10000points_50km_uf5_1hole_OSM.csv', index=False)

# del epoch
# del time_taken
# del df9
# gc.collect()

# ontop.stop()
# ontop.start()
# print("\n------ ONTOP Restarted #4 ---------\n")
# time.sleep(15)

# print("10000points_100km_uf5_1hole")


# df10 = pd.read_pickle('./benchmark_scripts/notebooks/10000points_100km_uf5_1hole.pkl')

# df10_data = []

# for epoch in tqdm(range(0, NUM_OF_POINTS, STEPS)):
#     try:
#         time_taken = benchmark(df10['geometry'][epoch])
#         df10_data.append({'Points': df10['points'][epoch], 'Processing_Time': time_taken})
#     except Exception as e:
#         print(f"Error with Points {epoch}: {e}")

# bm10 = pd.DataFrame(df10_data)
# bm10.to_csv('./benchmark_scripts/paper/fig2/Temp_10000points_100km_uf5_1hole_OSM.csv', index=False)

# del epoch
# del time_taken
# del df10
# gc.collect()


# # time.sleep(60)
# print("10000points_250km_uf5_1hole")
# time.sleep(30) 

# df11 = pd.read_pickle('./benchmark_scripts/notebooks/10000points_250km_uf5_1hole.pkl')

# df11_data = []

# for epoch in tqdm(range(0, NUM_OF_POINTS, STEPS)):
#     try:
#         time_taken = benchmark(df11['geometry'][epoch])
#         df11_data.append({'Points': df11['points'][epoch], 'Processing_Time': time_taken})
#     except Exception as e:
#         print(f"Error with Points {epoch}: {e}")

# bm11 = pd.DataFrame(df11_data)
# bm11.to_csv('./benchmark_scripts/paper/fig2/Temp_10000points_250km_uf5_1hole_OSM.csv', index=False)

# del epoch
# del time_taken
# del df11
# gc.collect()


# print("10000points_500km_uf5_1hole")
# time.sleep(30) 

# df12 = pd.read_pickle('./benchmark_scripts/notebooks/10000points_500km_uf5_1hole.pkl')

# df12_data = []

# for epoch in tqdm(range(0, NUM_OF_POINTS, STEPS)):
#     try:
#         time_taken = benchmark(df12['geometry'][epoch])
#         df12_data.append({'Points': df12['points'][epoch], 'Processing_Time': time_taken})
#     except Exception as e:
#         print(f"Error with Points {epoch}: {e}")

# bm12 = pd.DataFrame(df12_data)
# bm12.to_csv('./benchmark_scripts/paper/fig2/Temp_10000points_500km_uf5_1hole_OSM.csv', index=False)

# del epoch
# del time_taken
# del df12
# gc.collect()

ontop.stop()
ontop.start()
print("\n++++++++++++++++++++++++++++++++++++++++++++++ FINISHED +++++++++++++++++++++++++++++++++++++++++++++++\n")