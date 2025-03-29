#!/bin/bash
echo "Viewing the PostgreSQL Client Version"
psql -Version

echo "Give rasdaman time to finish importing files"
# TODO: Must remove in the future
sleep 90

echo "Set password"
export PGPASSWORD="petapasswd"

# shp2pgsql scripts
echo "Loading vector data for Area of Interest (AOI) Bavaria"
shp2pgsql -s 4326 /data/Bavaria_1.shp region_Bavaria | psql -h rasdatabase -p 5432 -U petauser -d vectordb
sleep 5
echo "Loading vector data for Area of Interest (AOI) Sweden"
shp2pgsql -s 4326 /data/gadm41_SWE_2.shp region_Sweden | psql -h rasdatabase -p 5432 -U petauser -d vectordb
sleep 5
echo "Loading vector data for Area of Interest (AOI) South Tyrol"
shp2pgsql -s 4326 /data/South_Tyrol_LOD3.shp region_South_Tyrol | psql -h rasdatabase -p 5432 -U petauser -d vectordb
echo "Loading 25 Districts of Munich"
shp2pgsql -s 4326 /data/Munich_25_Bezirke_Dissolved.shp public.munich_dist25 | psql -h rasdatabase -p 5432 -U petauser -d vectordb
sleep 5
echo "Loading 105 Sub-Districts of Munich"
shp2pgsql -s 4326 /data/Munich_105_Bezirke.shp public.munich_subdist105 | psql -h rasdatabase -p 5432 -U petauser -d vectordb
sleep 5
echo "Loading OSM buildings of Munich"
shp2pgsql -s 4326 /data/MunichOSM.shp public.munich_bldings_osm | psql -h rasdatabase -p 5432 -U petauser -d vectordb
sleep 5
# Run Python import script for GeoNames data
echo "Importing GeoNames data..."
python3 importGEONAMES.py
sleep 20

echo "------------------ FLAG 1 -----------------------"
# pg_dump copy all data from petascopedb to vectordb since Ontop does not support multiple databases
pg_dump -h rasdatabase -p 5432 -U petauser -d petascopedb -n public --schema-only > schema_dump.sql
pg_dump -h rasdatabase -p 5432 -U petauser -d petascopedb -n public --data-only > data_dump.sql
sleep 10
echo "------------------ FLAG 2 -----------------------"
psql -h rasdatabase -p 5432 -U petauser -d vectordb -f schema_dump.sql
psql -h rasdatabase -p 5432 -U petauser -d vectordb -f data_dump.sql
sleep 10
echo "------------------ FLAG 3 -----------------------"
# Additional scripts to create lookup table
psql -h rasdatabase -p 5432 -U petauser -d vectordb -f lookup_scripts.sql

echo "------------------ FINISHED -----------------------"


unset PGPASSWORD