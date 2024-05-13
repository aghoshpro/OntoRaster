#!/bin/bash

# shp2pgsql scripts
#TODO: Add scripts
shp2pgsql -s 4326 /db_pgsql/vector_data/Bavaria_1.shp region_Bavaria | psql -h localhost -p 5432 -U postgres -d VectorDB
shp2pgsql -s 4326 /db_pgsql/vector_data/gadm41_SWE_2.shp region_Sweden | psql -h localhost -p 5432 -U postgres -d VectorDB
shp2pgsql -s 4326 /db_pgsql/vector_data/South_Tyrol_LOD3.shp region_South_Tyrol | psql -h localhost -p 5432 -U postgres -d VectorDB
