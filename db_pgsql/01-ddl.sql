CREATE EXTENSION postgis;
CREATE EXTENSION postgis_raster;
CREATE EXTENSION plpgsql;
CREATE EXTENSION plpython3u;

-- Database: VectorDB (Contains all types of geometrical shape files)

-- DROP DATABASE IF EXISTS "VectorDB";

CREATE DATABASE "VectorDB"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- **********************************************************************************************************************************************
-- Table: public.petascopedb01 (holds metadata for each raster stored in rasdaman)

-- DROP TABLE IF EXISTS public.petascopedb01;

CREATE TABLE IF NOT EXISTS public.petascopedb01
(
    raster_id bigint NOT NULL,
    raster_name character varying COLLATE pg_catalog."default",
    axis_label character varying COLLATE pg_catalog."default",
    axis_type character varying COLLATE pg_catalog."default",
    dom_lower_bound character varying COLLATE pg_catalog."default",
    grid_lower_bound bigint,
    dom_upper_bound character varying COLLATE pg_catalog."default",
    grid_upper_bound bigint,
    resolution double precision,
    scale_factor double precision,
    CONSTRAINT petascopedb01_pkey PRIMARY KEY (raster_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.petascopedb01
    OWNER to postgres;

-- **********************************************************************************************************************************************

-- FUNCTION: rasdaman_op.check_rasdaman_conn()

-- DROP FUNCTION IF EXISTS rasdaman_op.check_rasdaman_conn();

CREATE OR REPLACE FUNCTION rasdaman_op.check_rasdaman_conn(
	OUT db_connector text)
    RETURNS text
    LANGUAGE 'plpython3u'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
from rasdapy.db_connector import DBConnector
from rasdapy.query_executor import QueryExecutor

db_connector = DBConnector("localhost", 7001, "rasadmin", "rasadmin")
query_executor = QueryExecutor(db_connector)

db_connector.open() # connection open

if bool(db_connector) == True: 
	return 'RasDaMan is connected'

db_connector.close()
$BODY$;

ALTER FUNCTION rasdaman_op.check_rasdaman_conn()
    OWNER TO postgres;

-- FUNCTION: rasdaman_op.geo2grid_coords(text)

-- DROP FUNCTION IF EXISTS rasdaman_op.geo2grid_coords(text);

CREATE OR REPLACE FUNCTION rasdaman_op.geo2grid_coords(
	"geoPOLY" text,
	OUT "gridPOLY" text)
    RETURNS text
    LANGUAGE 'plpython3u'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
import numpy as np
import re
import gdal
from affine import Affine
from shapely.geometry import Polygon
from shapely import wkt

-- Required metadata for geo2grid translation. different for each raster  
xmin = 8.979166665862266  
ymax = 50.979166665862266 
pixel_size = 0.008333333332587

def grid2WKT_polygon(y_grid, x_grid):
    coordinates = list(zip(y_grid, x_grid))
    polygon = "POLYGON((" + ", ".join(f"{x} {y}" for x, y in coordinates) + "))"
    return polygon

def geo2grid(lons, lats, xmin, ymax, pixel_size, xskew = 0.0, yskew = 0.0):
    aff_gdal = Affine.from_gdal(xmin, pixel_size, xskew, ymax, 0.0, -pixel_size)
    lons = np.array(lons)
    lats = np.array(lats)
    xs, ys = ~aff_gdal*(lons, lats)
    xs = np.int64(xs)
    ys = np.int64(ys)
    return xs, ys 

def add_closing_coordinates(d):
    i = re.search(r"\d", d).start()
    j = re.search(r'(\d)[^\d]*$', d).start() + 1
    c = d.index(',')    
    return d[:j] + ", " + d[i:c] + d[j:]

def processPOLYGON(inputPOLYGON, regionID = None):
    if inputPOLYGON.area < pixel_size:
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

        x_grid, y_grid = geo2grid(long_list, lat_list, xmin, ymax, pixel_size)
        gridPOLYGON_yx = grid2WKT_polygon(y_grid, x_grid)

        return gridPOLYGON_yx
    else:
        print(f"{regionID}: Polygon Ring Detected")
        mainPOLYGON = Polygon(inputPOLYGON.exterior)  
        gridPOLYGON_yx = processPOLYGON(mainPOLYGON)

        return gridPOLYGON_yx

           
def geoPOLYGON_to_gridPOLYGON_03(inputREGION, regionID = None):
    polygons_array1 = []
    polygons_array2 = []
    i = 0
    r = 0
    inputREGION = wkt.loads(inputREGION)
    if inputREGION.geom_type == 'Polygon':
        return processPOLYGON(inputREGION, regionID)
    
    elif len(list(inputREGION.geoms[0].interiors)) > 0:         
        for polygon in inputREGION.geoms:
            gridPOLYGON = processPOLYGON(polygon)
            polygons_array1.append(gridPOLYGON)
            r = r +1
            
        gridMULTI =  [shapely.wkt.loads(poly) for poly in polygons_array1]
        return shapely.geometry.MultiPolygon(gridMULTI)

    else:                                                  
        print(f"{regionID}: MultiPolygon is processing")
        for polygon in inputREGION.geoms:
            gridPOLYGON = processPOLYGON(polygon)
            polygons_array2.append(gridPOLYGON)
            i = i +1
            
        gridMULTI =  [shapely.wkt.loads(poly) for poly in polygons_array2]
        return shapely.geometry.MultiPolygon(gridMULTI)

gridPOLY = geoPOLYGON_to_gridPOLYGON_03(geoPOLY)
return gridPOLY
$BODY$;

ALTER FUNCTION rasdaman_op.geo2grid_coords(text)
    OWNER TO postgres;

-- FUNCTION: rasdaman_op.query2array(text)

-- DROP FUNCTION IF EXISTS rasdaman_op.query2array(text);

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
	
db_connector = DBConnector("localhost", 7001, "rasadmin", "rasadmin")
query_executor = QueryExecutor(db_connector)
db_connector.open()

try:
   data_array= query2array(query)
   return data_array
finally:
   db_connector.close()
$BODY$;

ALTER FUNCTION rasdaman_op.query2array(text)
    OWNER TO postgres;

-- FUNCTION: rasdaman_op.query2numeric(text)

-- DROP FUNCTION IF EXISTS rasdaman_op.query2numeric(text);

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
	
db_connector = DBConnector("localhost", 7001, "rasadmin", "rasadmin")
query_executor = QueryExecutor(db_connector)
db_connector.open()

try:
   return float("{:.3f}".format(query2result(query)))
finally:
   db_connector.close()
$BODY$;

ALTER FUNCTION rasdaman_op.query2numeric(text)
    OWNER TO postgres;


