#!/bin/bash

echo "Viewing the PostgreSQL Client Version"
psql -Version

echo "Give rasdaman time to finish importing files"
# TODO: Must remove in the future
sleep 90

echo "Set password"
export PGPASSWORD="petapasswd"

# shp2pgsql scripts
echo "Load Bavaria2"
shp2pgsql -s 4326 /data/Bavaria_1.shp region_Bavaria | psql -h rasdatabase -p 5432 -U petauser -d vectordb
sleep 5
echo "Load Sweden"
shp2pgsql -s 4326 /data/gadm41_SWE_2.shp region_Sweden | psql -h rasdatabase -p 5432 -U petauser -d vectordb
sleep 5
echo "Load South Tyrol"
shp2pgsql -s 4326 /data/South_Tyrol_LOD3.shp region_South_Tyrol | psql -h rasdatabase -p 5432 -U petauser -d vectordb
sleep 10


# Additional scripts to create lookup table
# TODO: Custom scripts for either petascopedb or vectordb
psql -h rasdatabase -p 5432 -U petauser -d petascopedb -f scripts.sql



unset PGPASSWORD