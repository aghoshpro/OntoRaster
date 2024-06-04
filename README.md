# OntoRaster
Raster Extension of VKG engine Ontop to query over **multidimensional gridded data** or **raster data** or **coverage** combined with **relational data** including geometrical **vector data** of the geospatial domain.

## Table of Contents
1. [Framework](#1-framework)
2. [Demo](#2-demo)
3. [Dataset](#3-dataset)
4. [Mapping](#4-mapping)
5. [Ontology](#5-ontology)
6. [More details](#6-more-details)

## 1. Framework

![OntoRaster (2)](https://github.com/aghoshpro/OntoRaster/assets/71174892/49751ecd-ba5b-49ef-8071-18f68e0dde37)


## 2. Demo
![OntopSolution](https://github.com/aghoshpro/OntoRaster/assets/71174892/c4649b67-3810-411e-a6d1-47ab6fbc42df)


https://github.com/aghoshpro/OntoRaster/assets/71174892/b89a73b8-8ed1-4963-973b-27ef6ee7b82b


### 2.1 Clone this repository

On Windows
```sh
git clone https://github.com/aghoshpro/OntoRaster  --config core.autocrlf=input
```

Otherwise, on MacOS and Linux:
```sh
git clone https://github.com/aghoshpro/OntoRaster
```

### 2.2 Setup Docker
Go to https://docs.docker.com/desktop/ and install docker on your favourite OS.

### 2.3 Run the demo
* Open `terminal` or `cmd` and navigate to the `OntoRaster` repository
  
* Run the following:
```sh
docker-compose -f docker-compose.ontoraster.yml up
```

* This command starts and initializes the PostgreSQL with the PostGIS database. Once the database is ready, 
Rasdaman starts and it imports the raster data.

* Finally, the Ontop SPARQL endpoint becomes available at http://localhost:8082/ 
with a set of sample queries.

* For this tutorial, we assume that the ports `7777`, `7001-7010, 8080` (used for the RDBMS and Array DBMS) and `8082` (used by Ontop) are free. If you need to use different ports, please edit the file `.env`.

* This Docker-compose file uses the mapping `vkg/OntoRaster.obda` and ontology `vkg/OntoRaster.owl`.

* Sample RasSPARQL queries are available at `vkg/OntoRaster.toml`.


## 3. Datasets

### 3.1 Relational Data (including Vector Data)
* [GADM data](https://gadm.org/download_country.html) (version 4.1): Contains a large number of relational data including geometrical vector data based on the user's region of interest (ROI). For this demo, we selected all municipalities of Sweden, Germany, and Italy (approx. 500 unique regions with region shape geometry and other attributes).


### 3.2 Raster Data
* Stored in array DBMS [RasDaMan](https://doc.rasdaman.org/index.html) ("Raster Data Manager")
* World: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)
* Sweden: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)
* Italy: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)
* Germany: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)


## 4. Mapping

## 5. Ontology

![Ontology](https://github.com/aghoshpro/OntoRaster/assets/71174892/d4ba1875-e589-4f36-b108-28b9f5d2cb50)


## 6. More details

Please visit the official website of Ontop https://ontop-vkg.org for more details on Virtual Knowledge Graphs 
and https://doc.rasdaman.org/index.html for more details on array databases.



