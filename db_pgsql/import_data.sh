#!/bin/bash

# Vector Geometry Data of REGION_OF_INTEREST(ROI)
shp2pgsql -s 4326 /db_pgsql/vector_data/Bavaria_1.shp region_Bavaria | psql -h localhost -p 5432 -U postgres -d VectorDB
shp2pgsql -s 4326 /db_pgsql/vector_data/gadm41_SWE_2.shp region_Sweden | psql -h localhost -p 5432 -U postgres -d VectorDB
shp2pgsql -s 4326 /db_pgsql/vector_data/South_Tyrol_LOD3.shp region_South_Tyrol | psql -h localhost -p 5432 -U postgres -d VectorDB
# Add more shp2pgsql commands as needed...

# TODO: Check if port is correct or MAPPED_PORT is needed
# TODO: Check if different databases are needed, in that case 2 different docker containers are needed
