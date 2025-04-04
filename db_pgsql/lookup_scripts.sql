CREATE EXTENSION IF NOT EXISTS dblink;

-- ###########################################
-- ### LookUp Table Creation In Petacopedb ### **********************************************************************************************************************************************
-- ###########################################
-- 1. lookup_temp (to get min max values as double)
CREATE OR REPLACE VIEW lookup_temp AS
		SELECT coverage.id, coverage.coverage_id, field.field_id, field.name, nil_value.null_value, uom.code, wgs84_bounding_box.max_lat, wgs84_bounding_box.min_lat, wgs84_bounding_box.max_long, wgs84_bounding_box.min_long 	
		FROM public.coverage
		JOIN public.envelope ON coverage.envelope_id = envelope.envelope_id
		JOIN public.range_type ON coverage.range_type_id = range_type.range_type_id 
		JOIN public.field ON field.data_record_id = range_type.data_record_id
		JOIN public.envelope_by_axis ON  envelope.envelope_by_axis_id = envelope_by_axis.envelope_by_axis_id
		JOIN public.wgs84_bounding_box ON envelope_by_axis.wgs84_bounding_box_id = wgs84_bounding_box.wgs84_bounding_box_id
		JOIN public.quantity ON field.quantity_id = quantity.quantity_id
		JOIN public.nil_value ON nil_value.quantity_id = quantity.quantity_id
		JOIN public.uom ON uom.uom_id = quantity.uom_id;
		
-- 1a. AxisExtent (for DATAGRIP)
CREATE OR REPLACE VIEW lookup_axis AS		
SELECT * FROM public.axis_extent;

-- 1b. GeoAxis (for DATAGRIP)
CREATE OR REPLACE VIEW lookup_geo_axis AS	
SELECT * FROM public.geo_axis;

-- 2. lookup_peta (build from selected tables from petascope and max min from lookup_temp).
--[FIX: axis_extent.resolution = geo_axis.resolution but ISSUE with axis_extent.resolution being numeric instead od float]	
CREATE OR REPLACE VIEW lookup_peta AS	
		SELECT coverage.id, coverage.coverage_id, lookup_temp.field_id, lookup_temp.name, lookup_temp.null_value, lookup_temp.code, axis_extent.axis_label, axis_extent.lower_bound, axis_extent.grid_lower_bound, axis_extent.upper_bound, axis_extent.grid_upper_bound,lookup_temp.max_lat, lookup_temp.min_lat, lookup_temp.max_long, lookup_temp.min_long, geo_axis.resolution
		FROM public.coverage, public.envelope, public.axis_extent, public.geo_axis, lookup_temp
		WHERE coverage.envelope_id = envelope.envelope_id 
		AND envelope.envelope_by_axis_id = axis_extent.envelope_by_axis_id
		AND axis_extent.upper_bound = geo_axis.upper_bound 
		AND coverage.id = lookup_temp.id;

-- 3. Switch to VectorDB and import lookup_peta as lookup_unstructured using dblink

CREATE OR REPLACE VIEW lookup_unstructured AS		
SELECT *
    FROM dblink('host=localhost dbname=vectordb user=petauser password=petapasswd options=-csearch_path=',
	   'SELECT id, coverage_id, field_id, name, null_value, code, axis_label, lower_bound, upper_bound, grid_lower_bound, grid_upper_bound, resolution, min_long, max_long, min_lat, max_lat FROM public.lookup_peta')
AS remote_table(raster_id text, raster_name text, field_id text, field_name text, fill_nan text, scale_factor float, axis_label text, domain_lower_bound text, domain_upper_bound text, grid_lower_bound integer, grid_upper_bound integer, resolution float, min_long float, max_long float, min_lat float, max_lat float);


-- 4. Build raster_lookup

CREATE OR REPLACE VIEW lookup_structured AS
SELECT 
	raster_id,
	raster_name,
	field_id,
	field_name, 
	fill_nan,
	scale_factor,
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
	MAX(CASE WHEN axis_label = 'ansi' THEN domain_lower_bound END) AS start_time,
	MAX(CASE WHEN axis_label = 'ansi' THEN domain_upper_bound END) AS end_time,
	MAX(CASE WHEN axis_label = 'ansi' THEN grid_lower_bound END) AS start_time_grid,
	MAX(CASE WHEN axis_label = 'ansi' THEN grid_upper_bound END) AS end_time_grid,
	MAX(CASE WHEN axis_label = 'ansi' THEN resolution END) AS res_time
FROM lookup_unstructured
GROUP BY raster_id, raster_name, field_id, field_name, fill_nan, scale_factor;


-- 5. Convert view to table with a primary key

CREATE TABLE raster_lookup AS SELECT * FROM lookup_structured;

ALTER TABLE raster_lookup ADD PRIMARY KEY (raster_id);

CREATE TABLE geonames (
                geonameid BIGINT NOT NULL PRIMARY KEY,
                name VARCHAR(200),
                asciiname VARCHAR(200),
                alternatenames VARCHAR(10000),
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8),
                feature_class CHAR(1),
                feature_code VARCHAR(10),
                country_code CHAR(2),
                cc2 VARCHAR(200),
                admin1_code VARCHAR(20),
                admin2_code VARCHAR(80),
                admin3_code VARCHAR(20),
                admin4_code VARCHAR(20),
                population BIGINT,
                elevation INTEGER,
                dem INTEGER,
                timezone VARCHAR(40),
                modification_date DATE);

-- ##########################
-- ### PL/pgsql Functions ### **********************************************************************************************************************************************
-- ##########################


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
FROM raster_lookup
WHERE start_time::TIMESTAMP <= input_time::TIMESTAMP AND end_time::TIMESTAMP >= input_time::TIMESTAMP AND raster_name = input_raster;

RETURN example_date_grid_val;
END;

$BODY$;

-- FUNCTION: rasdaman_op.get_min_longitude(text)

CREATE OR REPLACE FUNCTION rasdaman_op.get_min_longitude(
	input_raster text,
	OUT min_lon double precision)
    RETURNS double precision
    LANGUAGE 'sql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
SELECT min_lon FROM raster_lookup WHERE raster_name = input_raster
    $BODY$;

-- FUNCTION: rasdaman_op.get_res_lon(text)

CREATE OR REPLACE FUNCTION rasdaman_op.get_res_lon(
	input_raster text,
	OUT res_lon double precision)
    RETURNS double precision
    LANGUAGE 'sql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
SELECT res_lon FROM raster_lookup WHERE raster_name = input_raster
    $BODY$;

-- FUNCTION: rasdaman_op.get_max_latitude(text)

CREATE OR REPLACE FUNCTION rasdaman_op.get_max_latitude(
	input_raster text,
	OUT max_lat double precision)
    RETURNS double precision
    LANGUAGE 'sql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
SELECT max_lat FROM raster_lookup WHERE raster_name = input_raster
    $BODY$;

-- FUNCTION: rasdaman_op.get_res_lat(text)

CREATE OR REPLACE FUNCTION rasdaman_op.get_res_lat(
	input_raster text,
	OUT res_lat double precision)
    RETURNS double precision
    LANGUAGE 'sql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
SELECT res_lat FROM raster_lookup WHERE raster_name = input_raster
    $BODY$;

-- FUNCTION: rasdaman_op.get_scalefactor(text)

CREATE OR REPLACE FUNCTION rasdaman_op.get_scalefactor(
	input_raster text,
	OUT scale_factor double precision)
    RETURNS double precision
    LANGUAGE 'sql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
SELECT scale_factor FROM raster_lookup WHERE raster_name = input_raster
    $BODY$;