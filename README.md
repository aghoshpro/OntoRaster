# OntoRaster
Raster Extension of VKG engine Ontop to query over multidimensional Raster Data combined with Relational data including Geometrical Vector Data

## Table of Contents
### 1. Requirements
 - [Setup Docker](https://www.docker.com/)
 - Setup Git
 - [Setup Docker](#setup-docker)
 - [Start Docker-Compose](#start-docker-compose)
* [Framework](#2-framework)
* [Demo](#3-demo)
* [Dataset](#4-dataset)
* [Mapping](#5-mapping)
* [Ontology](#6-ontology)
* [More info](#7-to-know-more)

## 2. Framework

![OntoRaster (2)](https://github.com/aghoshpro/OntoRaster/assets/71174892/49751ecd-ba5b-49ef-8071-18f68e0dde37)


## 3. Demo
### 3.1 Clone this repository

On Windows
```sh
git clone https://github.com/aghoshpro/OntoRaster  --config core.autocrlf=input
```

Otherwise, on MacOS and Linux:
```sh
git clone https://github.com/aghoshpro/OntoRaster
```

### 3.2 Setup Docker
Go to https://docs.docker.com/desktop/ and install docker on your favourite os.

### 3.3 Run the demo
* Go to the `OntoRaster` repository
  
* First, stop the current docker-compose:
```sh
docker-compose stop
```

* Then, specify the file by using *-f* : 
```sh
docker-compose -f docker-compose.ontoraster.yml up
```

This Docker-compose file uses the mapping `vkg/OntoRaster.obda`.

This command starts and initializes the database. Once the database is ready, it launches the SPARQL endpoint from Ontop at http://localhost:8082/.

For this tutorial, we assume that the ports `7001-7010, 8082` (used for database) and `8080` (used by Ontop) are free. If you need to use different ports, please edit the file `.env`.

For example, RasSPARQL queries are available at [endpoint](http://localhost:8082/).


## 4. Datasets

### 4.1 Vector Data
* Download [GADM data](https://gadm.org/download_country.html) GADM data (version 4.1) based on region of interest (ROI) such as Municipalities of Sweden, Germany, Italy.
* User can download vector shape or csv file of their own choice.

### 4.2 Raster Data
* World: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)
* Sweden: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)
* Italy: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)
* Germany: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)


## 5. Mapping

## 6. Ontology

![Ontology](https://github.com/aghoshpro/OntoRaster/assets/71174892/d4ba1875-e589-4f36-b108-28b9f5d2cb50)


## 7. To know more

Visit the official website of Ontop https://ontop-vkg.org, which also provides a more detailed tutorial.



