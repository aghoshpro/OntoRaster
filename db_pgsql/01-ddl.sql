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


-- ###########################################
-- ### LookUp Table Creation In petacopedb ### **********************************************************************************************************************************************
-- ###########################################

-- 1. Selected Tables from petascopedb

SELECT * FROM public.axis_extent

SELECT * FROM public.geo_axis

SELECT * FROM public.index_axis

SELECT * FROM public.coverage

SELECT * FROM public.envelope

SELECT * FROM public.envelope_by_axis

SELECT * FROM public.wgs84_bounding_box
	

-- 2. lookup_temp (to get extent as double)
CREATE OR REPLACE VIEW lookup_temp_X AS
	SELECT coverage.id, coverage.coverage_id, wgs84_bounding_box.max_lat, wgs84_bounding_box.min_lat, wgs84_bounding_box.max_long, wgs84_bounding_box.min_long 	
	FROM public.coverage
	JOIN public.envelope ON coverage.envelope_id = envelope.envelope_id
	JOIN public.envelope_by_axis ON  envelope.envelope_by_axis_id = envelope_by_axis.envelope_by_axis_id
	JOIN public.wgs84_bounding_box ON envelope_by_axis.wgs84_bounding_box_id = wgs84_bounding_box.wgs84_bounding_box_id
		

-- 3. lookup_peta build from selected tables joined lookup_temp.
	
CREATE OR REPLACE VIEW lookup_peta_X AS	
	SELECT coverage.id, coverage.coverage_id,  axis_extent.axis_label, axis_extent.lower_bound, axis_extent.grid_lower_bound, axis_extent.upper_bound, axis_extent.grid_upper_bound,lookup_temp_X.max_lat, lookup_temp_X.min_lat, lookup_temp_X.max_long, lookup_temp_X.min_long, geo_axis.resolution
	FROM public.coverage, public.envelope,  public.axis_extent, public.geo_axis, lookup_temp_X
	WHERE coverage.envelope_id = envelope.envelope_id 
	AND envelope.envelope_by_axis_id = axis_extent.envelope_by_axis_id 
	AND axis_extent.upper_bound = geo_axis.upper_bound
	AND coverage.id = lookup_temp_X.id

SELECT * FROM lookup_peta_X -- Lookup Table in petascopedb

-- 4. Switch to VectorDB and import lookup_peta_X as lookup_main_X1 using dblink

CREATE OR REPLACE VIEW lookup_main_X1 AS		
SELECT *
    FROM dblink('host=localhost dbname=petascopedb user=petauser password=petapasswd options=-csearch_path=',
	   'SELECT id, coverage_id, axis_label, lower_bound, upper_bound, grid_lower_bound, grid_upper_bound, resolution, min_long, max_long, min_lat, max_lat FROM public.lookup_peta_x')
AS remote_table(raster_id text, raster_name text, axis_label text, domain_lower_bound text, domain_upper_bound date, grid_lower_bound date, grid_upper_bound integer, resolution float, min_long float, max_long float, min_lat float, max_lat float);



-- 5. Build sample_lookup_X

CREATE OR REPLACE VIEW sample_lookup_X1 AS
SELECT 
    raster_id,
    raster_name,
    MAX(CASE WHEN axis_label = 'Long' THEN min_long END) AS min_lon,
    MAX(CASE WHEN axis_label = 'Long' THEN max_long END) AS max_lon,
	MAX(CASE WHEN axis_label = 'Long' THEN grid_lower_bound END) AS min_lon_grid,
    MAX(CASE WHEN axis_label = 'Long' THEN grid_upper_bound END) AS max_lon_grid,
	MAX(CASE WHEN axis_label = 'Long' THEN resolution END) AS res_lon,
    MAX(CASE WHEN axis_label = 'Lat' THEN min_lat END) AS min_lat,
    MAX(CASE WHEN axis_label = 'Lat' THEN max_lat END) AS max_lat,
	MAX(CASE WHEN axis_label = 'Lat' THEN grid_lower_bound END) AS min_lat_grid,
    MAX(CASE WHEN axis_label = 'Lat' THEN grid_upper_bound END) AS max_lat_grid,
	MAX(CASE WHEN axis_label = 'Lat' THEN resolution END) AS res_lat,
	MAX(CASE WHEN axis_label = 'ansi' THEN domain_lower_bound date END) AS start_time,
    MAX(CASE WHEN axis_label = 'ansi' THEN domain_upper_bound date END) AS end_time,
	MAX(CASE WHEN axis_label = 'ansi' THEN grid_lower_bound END) AS start_time_grid,
    MAX(CASE WHEN axis_label = 'ansi' THEN grid_upper_bound END) AS end_time_grid,
	MAX(CASE WHEN axis_label = 'ansi' THEN resolution END) AS res_time
FROM lookup_main_X1
GROUP BY raster_id, raster_name;


select * from sample_lookup_X1 -- Build mappings with this table in VectorDB
	

-- ###########################################
-- ### PL/pgsql Functions ### **********************************************************************************************************************************************
-- ###########################################

-- FUNCTION 01: rasdaman_op.timestamp2grid(text, text)

-- DROP FUNCTION IF EXISTS rasdaman_op.timestamp2grid(text, text);

CREATE OR REPLACE FUNCTION rasdaman_op.timestamp2grid(
	input_time text,
	input_raster text)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    example_date_grid_val INTEGER;
BEGIN
    SELECT start_time_grid + EXTRACT(DAY FROM (input_time::TIMESTAMP - start_time::TIMESTAMP))INTO example_date_grid_val
    FROM sample_lookup_X1
    WHERE start_time::TIMESTAMP <= input_time::TIMESTAMP AND end_time::TIMESTAMP >= input_time::TIMESTAMP AND raster_name = input_raster;
    
    RETURN example_date_grid_val;
END;

$BODY$;

ALTER FUNCTION rasdaman_op.timestamp2grid(text, text)
    OWNER TO postgres;

-- FUNCTION 02: rasdaman_op.get_geom_wkt(geometry)

-- DROP FUNCTION IF EXISTS rasdaman_op.get_geom_wkt(geometry);

CREATE OR REPLACE FUNCTION rasdaman_op.get_geom_wkt(
	geometry_wkt geometry)
    RETURNS text
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    out_geom_wkt TEXT;
BEGIN
	SELECT 
	    CASE 
	        WHEN ST_NumGeometries(geometry_wkt) = 1 THEN ST_AsText(ST_GeometryN(geometry_wkt, 1))
	        ELSE ST_AsText(geometry_wkt)
	    END AS geometry_wkt INTO out_geom_wkt;

	RETURN out_geom_wkt;
END;

$BODY$;

ALTER FUNCTION rasdaman_op.get_geom_wkt(geometry)
    OWNER TO postgres;


-- ###########################################
-- ### PL/Python ### **********************************************************************************************************************************************
-- ###########################################


-- FUNCTION: rasdaman_op.geo2grid_final(text, double precision, double precision, double precision, double precision)

-- DROP FUNCTION IF EXISTS rasdaman_op.geo2grid_final(text, double precision, double precision, double precision, double precision);

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
import gdal
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

def add_closing_coordinates(d):
    i = re.search(r"\d", d).start()
    j = re.search(r'(\d)[^\d]*$', d).start() + 1
    c = d.index(',')    
    return d[:j] + ", " + d[i:c] + d[j:]

def processPOLYGON(inputPOLYGON):
    if inputPOLYGON.area < x_scale:
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

ALTER FUNCTION rasdaman_op.geo2grid_final(text, double precision, double precision, double precision, double precision)
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

-- FUNCTION: rasdaman_op.query2string(text)

-- DROP FUNCTION IF EXISTS rasdaman_op.query2string(text);

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
	
db_connector = DBConnector("localhost", 7001, "rasadmin", "rasadmin")
query_executor = QueryExecutor(db_connector)
db_connector.open()

try:
   return query2result(query)
finally:
   db_connector.close()
$BODY$;

ALTER FUNCTION rasdaman_op.query2string(text)
    OWNER TO postgres;




