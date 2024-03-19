#!/bin/bash

# Vector Geometry Data of REGION_OF_INTEREST(ROI)
shp2pgsql -s 4326 /home/arkaghosh/Downloads/Bolzano/Vector/South_Tyrol_LOD3.shp region_South_Tyrol | psql -h localhost -p 5432 -U postgres -d VectorDB
shp2pgsql -s 4326 /home/arkaghosh/Downloads/Baveria/Vector/Baveria_1.shp region_bavaria | psql -h localhost -p 5432 -U postgres -d VectorDB
shp2pgsql -s 4326 /home/arkaghosh/Downloads/Sweden/Vector/SWE_adm2.shp region_sweden | psql -h localhost -p 5432 -U postgres -d VectorDB
# Add more shp2pgsql commands as needed...

# TODO: Check if port is correct or MAPPED_PORT is needed
# TODO: Check if different databases are needed, in that case 2 different docker containers are needed
