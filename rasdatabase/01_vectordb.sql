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

def geoPOLYGON_to_gridPOLYGON_03(inputREGION, min_lon, max_lat, resolution_lon, resolution_lat):
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

gridPOLY = geoPOLYGON_to_gridPOLYGON_03(geoPOLY, min_lon, max_lat, resolution_lon, resolution_lat)
return gridPOLY


$BODY$;


-- FUNCTION: rasdaman_op.query2array(text)

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
