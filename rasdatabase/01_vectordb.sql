CREATE DATABASE vectordb;
\connect vectordb;
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_raster;
-- CREATE EXTENSION plpgsql;
CREATE EXTENSION plpython3u;

-- Activate plpython venv
-- Create function to activate specific Python venv
-- CREATE OR REPLACE FUNCTION activate_python_venv(venv text) returns void
--     language plpython3u
-- as
-- $BODY$
--     import os
--     import sys
--
--     if sys.platform in ('win32', 'win64', 'cygwin'):
--         activate_this = os.path.join(venv, 'Scripts', 'activate_this.py')
--     else:
--         activate_this = os.path.join(venv, 'bin', 'activate_this.py')
--
--     exec(open(activate_this).read(), dict(__file__=activate_this))
-- $BODY$;
--
-- SELECT activate_python_venv('/opt/envrasdaman');

CREATE SCHEMA IF NOT EXISTS rasdaman_op;


-- FUNCTION: rasdaman_op.geo2grid_final(text, double precision, double precision, double precision, double precision)

CREATE OR REPLACE FUNCTION rasdaman_op.geo2grid_final(
	"geoPOLY" text,
	min_lon double precision,
	max_lat double precision,
	resolution_lon double precision,
	resolution_lat double precision,
	OUT "gridPOLY" text)
    RETURNS text
    LANGUAGE 'plpython3u'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
import numpy as np
import re

from affine import Affine
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely import wkt

def grid2WKT_polygon(y_grid, x_grid):
    coordinates = list(zip(y_grid, x_grid))
    polygon = "POLYGON((" + ", ".join(f"{x} {y}" for x, y in coordinates) + "))"
    return polygon

def geo2grid(lons, lats, xmin, ymax, x_scale, y_scale, xskew = 0.0, yskew = 0.0):
    aff_gdal = Affine.from_gdal(xmin, x_scale, xskew, ymax, 0.0, -y_scale)
    lons = np.array(lons)
    lats = np.array(lats)
    xs, ys = ~aff_gdal*(lons, lats)
    xs = np.int64(xs)
    ys = np.int64(ys)
    return xs, ys

def processPOLYGON(inputPOLYGON):
    if inputPOLYGON.area == 0:
	    pass
    elif len(inputPOLYGON.interiors) == 0:
        coords = np.dstack(inputPOLYGON.boundary.xy).tolist()[0][:-1]
        expected_list_of_coordinates_for_received_code = [{"long": x, "lat": y} for x, y in coords]
        lat_arr = []
        long_arr = []
        for i in range(len(expected_list_of_coordinates_for_received_code)):
            long_arr = np.append(long_arr, expected_list_of_coordinates_for_received_code[i]['long'])
            lat_arr = np.append(lat_arr, expected_list_of_coordinates_for_received_code[i]['lat'])

        long_list = long_arr.tolist()
        lat_list = lat_arr.tolist()

        x_grid, y_grid = geo2grid(long_list, lat_list, xmin, ymax, x_scale, y_scale)
        gridPOLYGON_yx = grid2WKT_polygon(y_grid, x_grid)

        return gridPOLYGON_yx
    else:
        mainPOLYGON = Polygon(inputPOLYGON.exterior)
        gridPOLYGON_yx = processPOLYGON(mainPOLYGON)

        return gridPOLYGON_yx

def geoPOLYGON_to_gridPOLYGON(inputREGION, min_lon, max_lat, resolution_lon, resolution_lat):
    polygons_array1 = []
    polygons_array2 = []
    i = 0
    r = 0
    global xmin
    xmin = min_lon
    global ymax
    ymax= max_lat
    global x_scale
    x_scale = resolution_lon
    global y_scale
    y_scale = resolution_lat

    inputREGION = wkt.loads(inputREGION)
    if inputREGION.geom_type == 'Polygon':
        return processPOLYGON(inputREGION)

    elif len(list(inputREGION.geoms[0].interiors)) > 0:
        for polygon in inputREGION.geoms:
            gridPOLYGON = processPOLYGON(polygon)
            polygons_array1.append(gridPOLYGON)

        gridMULTI =  [wkt.loads(poly) for poly in polygons_array1]
        return shapely.geometry.MultiPolygon(gridMULTI)

    else:
        for polygon in inputREGION.geoms:
            gridPOLYGON = processPOLYGON(polygon)
            polygons_array2.append(gridPOLYGON)

        gridMULTI =  [wkt.loads(poly) for poly in polygons_array2]
        return unary_union(gridMULTI)

gridPOLY = geoPOLYGON_to_gridPOLYGON(geoPOLY, min_lon, max_lat, resolution_lon, resolution_lat)
return gridPOLY
$BODY$;


-- FUNCTION: rasdaman_op.query2array(text) - works in ontoraster v1.3, v1.51

CREATE OR REPLACE FUNCTION rasdaman_op.query2array(
	query text,
	OUT data_array double precision[])
    RETURNS double precision[]
    LANGUAGE 'plpython3u'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
from rasdapy.db_connector import DBConnector
from rasdapy.query_executor import QueryExecutor

def query2array(query):
    result = query_executor.execute_read(query)
    numpy_array = result.to_array()
    return numpy_array.tolist()

db_connector = DBConnector("host.docker.internal", 7001, "rasadmin", "rasadmin")
query_executor = QueryExecutor(db_connector)
db_connector.open()

try:
   data_array= query2array(query)
   return data_array
finally:
   db_connector.close()
$BODY$;

-- FUNCTION: rasdaman_op.query2array03(text, text)
-- CREATE OR REPLACE FUNCTION rasdaman_op.query2array03(
--     query text,
--     input_raster text,
--     OUT cleaned_array double precision[])
--     RETURNS double precision[]
--     LANGUAGE 'plpython3u'
--     COST 100
--     VOLATILE PARALLEL UNSAFE
-- AS $BODY$
-- from rasdapy.db_connector import DBConnector
-- from rasdapy.query_executor import QueryExecutor

-- fill_nan_query = f"SELECT fill_nan FROM raster_lookup WHERE raster_name = '{input_raster}'"
-- plan = plpy.prepare(fill_nan_query)
-- result = plpy.execute(plan)
-- fill_nan = result[0]['fill_nan'] if result else 0

-- def query2array(query, fill_nan):
--     result = query_executor.execute_read(query) 
--     numpy_array = result.to_array()
--     numpy_array = numpy_array.astype('float')
--     numpy_array[numpy_array == fill_nan] = 'nan'
--     return numpy_array.tolist()  

-- db_connector = DBConnector("localhost", 7001, "rasadmin", "rasadmin")
-- query_executor = QueryExecutor(db_connector)
-- db_connector.open()
-- try:
--     cleaned_array = query2array(query, fill_nan)
--     return cleaned_array
-- finally:
--     db_connector.close()
-- $BODY$;

-- FUNCTION: rasdaman_op.query2numeric(text)

CREATE OR REPLACE FUNCTION rasdaman_op.query2numeric(
	query text,
	OUT double precision)
    RETURNS double precision
    LANGUAGE 'plpython3u'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
from rasdapy.db_connector import DBConnector
from rasdapy.query_executor import QueryExecutor

def query2result(query):
   output_val = query_executor.execute_read(query)
   output_val = float("{}".format(output_val))
   return output_val

db_connector = DBConnector("host.docker.internal", 7001, "rasadmin", "rasadmin")
query_executor = QueryExecutor(db_connector)
db_connector.open()

try:
   return float("{:.3f}".format(query2result(query)))
finally:
   db_connector.close()
$BODY$;

-- FUNCTION: rasdaman_op.query2string(text)

CREATE OR REPLACE FUNCTION rasdaman_op.query2string(
	query text,
	OUT text)
    RETURNS text
    LANGUAGE 'plpython3u'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
from rasdapy.db_connector import DBConnector
from rasdapy.query_executor import QueryExecutor

def query2result(query):
   output_val = query_executor.execute_read(query)
   return output_val

db_connector = DBConnector("host.docker.internal", 7001, "rasadmin", "rasadmin")
query_executor = QueryExecutor(db_connector)
db_connector.open()

try:
   return query2result(query)
finally:
   db_connector.close()
$BODY$;

-- FUNCTION: rasdaman_op.query2geotiff(text, text, text, double precision)

CREATE OR REPLACE FUNCTION rasdaman_op.query2geotiff(
	query text,
	regionWkt text,
	filename text,
	fill_val double precision,
	OUT folium text)
    RETURNS text
    LANGUAGE 'plpython3u'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
from rasdapy.db_connector import DBConnector
from rasdapy.query_executor import QueryExecutor
from shapely import Point, Polygon, bounds, wkt
import numpy as np
import os
import gdal
from osgeo import osr
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import rasterio
from rasterio.plot import show, reshape_as_image, reshape_as_raster, reshape_as_image
import folium
from folium.raster_layers import ImageOverlay

def get_polygon_extent(polygon):
    coords = list(polygon.exterior.coords)
    xs = [x for x, y in coords]
    ys = [y for x, y in coords]
    return [min(xs), min(ys), max(xs), max(ys)]
	
def getGeoTransform(extent, nlines, ncols):
    resx = (extent[2] - extent[0]) / ncols
    resy = (extent[3] - extent[1]) / nlines
    return [extent[0], resx, 0, extent[3] , 0, -resy]
	
def query2folium(query, regionWkt, filename, fill_val):
    result = query_executor.execute_read(query) 
    numpy_array = result.to_array()
    if fill_val is not None:
        numpy_array = numpy_array.astype('float')
        numpy_array[numpy_array == fill_val] = 'nan'

    driver = gdal.GetDriverByName('GTiff')  
    nrows = numpy_array.shape[0]
    ncols = numpy_array.shape[1]
    data_type = gdal.GDT_Float32
    grid_data = driver.Create('grid_data', ncols, nrows, 1, data_type)
    grid_data.GetRasterBand(1).WriteArray(numpy_array)
    srs = osr.SpatialReference()
    srs.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
    grid_data.SetProjection(srs.ExportToWkt())
    regionWkt = wkt.loads(regionWkt)
    extent = get_polygon_extent(regionWkt)
    grid_data.SetGeoTransform(getGeoTransform(extent, nrows, ncols))	
    file_name = str(filename)+'.tif'
    driver.CreateCopy(file_name, grid_data, 0)  
    driver = None
    grid_data = None          
    os.remove('grid_data')
    elevRaster = rasterio.open(file_name)
    elevArray = elevRaster.read(1)
    boundList = [x for x in elevRaster.bounds]
    norm = Normalize(vmin=np.nanmin(elevArray), vmax=np.nanmax(elevArray))
    cmap = plt.cm.get_cmap('jet')
    def colormap_function(x):
        rgba = cmap(norm(x))
        return (rgba[0], rgba[1], rgba[2], rgba[3])

    rasLon = (boundList[3] + boundList[1])/2
    rasLat = (boundList[2] + boundList[0])/2
    mapCenter = [rasLon, rasLat]

    mf = folium.Map(location=mapCenter, zoom_start=13)
    folium.raster_layers.ImageOverlay(
        image=elevArray,
        bounds=[[boundList[1], boundList[0]], [boundList[3], boundList[2]]],
        opacity=0.52,
        colormap=colormap_function,  
		interactive=True,
        cross_origin=False,
    ).add_to(mf)
    
    return mf

db_connector = DBConnector("localhost", 7001, "rasadmin", "rasadmin")
query_executor = QueryExecutor(db_connector)
db_connector.open()

try:
   folium= query2folium(query, regionWkt, None, None)
   return folium
finally:
   db_connector.close()	
$BODY$;