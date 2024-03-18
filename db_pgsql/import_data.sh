#!/bin/bash

shp2pgsql -s 4326 /home/arkaghosh/Downloads/Bolzano/Vector/South_Tyrol_LOD3.shp region_South_Tyrol | psql -h localhost -p 5432 -U postgres -d VectorDB
shp2pgsql -s 4326 /home/arkaghosh/Downloads/Baveria/Vector/Baveria_1 baveria_districts | psql -h localhost -p 5432 -U postgres -d Baveria
# Add more shp2pgsql commands as needed...
# TODO: Check if port is correct or MAPPED_PORT is needed
# TODO: Check if different databases are needed, in that case 2 different docker containers are needed
