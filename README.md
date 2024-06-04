# OntoRaster
Raster Extension of Ontop, a Virtual Knowledge Graph (VKG) system to query over **multidimensional gridded data** or **raster data** or **coverage** combined with **relational data** including geometrical **vector data** of the geospatial domain.

We are also working on our methodology which will enable **OntoRaster** to query over generic **raster data** and **vector data** of any domain under the VKG paradigm. 

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

### 2.1 Clone this repository

* On Windows
```sh
git clone https://github.com/aghoshpro/OntoRaster  --config core.autocrlf=input
```

* Otherwise, on MacOS and Linux:
```sh
git clone https://github.com/aghoshpro/OntoRaster
```

### 2.2 Setup Docker
* Go to https://docs.docker.com/desktop/ and install docker on your favourite OS.

### 2.3 Run the demo
* Open `terminal` or `cmd` and navigate to the `OntoRaster` repository
  
* Run the following:
```sh
docker-compose -f docker-compose.ontoraster.yml up
```

* This command starts and initializes the relational database **PostgreSQL** with the spatial extension **PostGIS**. Once the relational database is ready, the array database **Rasdaman** initiates and imports the raster data.

* For this tutorial, we assume that the ports `7777`, `7001-7010, 8080` (used for the RDBMS and Array DBMS) and `8082` (used by Ontop) are free. If you need to use different ports, please edit the file `.env`.

* This Docker-compose file uses the mapping `vkg/OntoRaster.obda` and ontology `vkg/OntoRaster.owl`.

* Finally, the Ontop SPARQL endpoint becomes available at http://localhost:8082/ 
with a set of example RasSPARQL queries.

* RasSPARQL queries are available at `vkg/OntoRaster.toml`.

### 2.3.1 Endpoint

![OntopSolution](https://github.com/aghoshpro/OntoRaster/assets/71174892/c4649b67-3810-411e-a6d1-47ab6fbc42df)


## 3. Datasets

### 3.1 Relational Data (including Vector Data)
* In this demo we used municipalities of Sweden, Bavaria (Germany), and South Tyrol (Italy) as vector data consists a total of approx. 500 unique regions with different geometries and other attributes downloaded from [GADM data](https://gadm.org/download_country.html).

* Stored in **PostgreSQL** with spatial extension PostGIS.
  
* Ideally any user-specific vector data for any region of interest will work.   

### 3.2 Raster Data
* Stored in array DBMS [RasDaMan](https://doc.rasdaman.org/index.html) ("Raster Data Manager")
  
* [World Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)
* [Sweden Land Temperature](https://lpdaac.usgs.gov/products/mod11a1v061/)
* [South Tyrol Temperature](https://lpdaac.usgs.gov/products/mod11a1v061/)
* [Bavaria Surface Temperature](https://lpdaac.usgs.gov/products/mod11a1v061/)

* Ideally any user-specific vector data for any region of interest will work   


## 4. Mapping

## 5. Ontology

![Ontology](https://github.com/aghoshpro/OntoRaster/assets/71174892/d4ba1875-e589-4f36-b108-28b9f5d2cb50)


## 6. More details

Please visit the official website of Ontop https://ontop-vkg.org for more details on Virtual Knowledge Graphs 
and https://doc.rasdaman.org/index.html for more details on array databases.



