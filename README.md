# OntoRaster
Raster Extension of VKG engine Ontop to query over **multidimensional gridded data** or **raster data** or **coverage** combined with **relational data** including geometrical **vector data** of the geospatial domain.

## Table of Contents
1. [Framework](#2-framework)
2. [Demo](#3-demo)
3. [Dataset](#4-dataset)
4. [Mapping](#5-mapping)
5. [Ontology](#6-ontology)
6. [More info](#7-more-details)

## 1. Framework

![OntoRaster (2)](https://github.com/aghoshpro/OntoRaster/assets/71174892/49751ecd-ba5b-49ef-8071-18f68e0dde37)


## 2. Demo
### 3.1 Clone this repository

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
  
* Stop the current docker-compose:-
```sh
docker-compose stop
```

* Run the following:-
```sh
docker-compose -f docker-compose.ontoraster.yml up
```

This Docker-compose file uses the mapping `vkg/OntoRaster.obda`.

This command starts and initializes the database. Once the database is ready, it launches the SPARQL endpoint from Ontop at http://localhost:8082/.

For this tutorial, we assume that the ports `7001-7010, 8082` (used for the database) and `8080` (used by Ontop) are free. If you need to use different ports, please edit the file `.env`.

For example, RasSPARQL queries are available at [endpoint](http://localhost:8082/).


## 4. Datasets

### 4.1 Vector Data
* Download [GADM data](https://gadm.org/download_country.html) GADM data (version 4.1) based on the region of interest (ROI) such as Municipalities of Sweden, Germany, and Italy.
* User can download vector data (in shapefile, CSV) of their own choice.

### 4.2 Raster Data
* World: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)
* Sweden: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)
* Italy: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)
* Germany: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)


## 5. Mapping

## 6. Ontology

![Ontology](https://github.com/aghoshpro/OntoRaster/assets/71174892/d4ba1875-e589-4f36-b108-28b9f5d2cb50)


## 7. More details

Please visit the official website of Ontop https://ontop-vkg.org, which also provides more details.



