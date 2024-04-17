#!/bin/bash

# shp2pgsql scripts
#TODO: Add scripts
shp2pgsql -s 4326 /path_to_shapefile/Bavaria_mun.shp region_Bavaria | psql -h localhost -p 5432 -U postgres -d VectorDB
shp2pgsql -s 4326 /path_to_shapefile/Sweden_mun.shp region_Sweden | psql -h localhost -p 5432 -U postgres -d VectorDB
shp2pgsql -s 4326 /path_to_shapefile/South_Tyrol_LOD3.shp region_South_Tyrol | psql -h localhost -p 5432 -U postgres -d VectorDB
