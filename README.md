# OntoRaster
Extension of Ontop, a VKG engine over multidimensional array database or Raster data combined with geometrical data (e.g. Vector Data) and Relational Data

This tutorial is adapted from [the Virtual Knowledge Graph](https://github.com/noi-techpark/it.bz.opendatahub.sparql) of the South Tyrolean [Open Data Hub](https://opendatahub.bz.it/).

## Table of contents
### Requirements
 - [Setup Docker](https://www.docker.com/)
 - Setup Git
 - [Setup Docker](#setup-docker)
 - [Start Docker-Compose](#start-docker-compose)
* [Demo](#demo)
* [Framework](#framework)
* [Dataset](#dataset)
* [Mapping](#mapping)
* [More info](#to-know-more)

## Framework

![OntoRaster (2)](https://github.com/aghoshpro/OntoRaster/assets/71174892/49751ecd-ba5b-49ef-8071-18f68e0dde37)



## Clone this repository

On Windows
```sh
git clone https://github.com/aghoshpro/OntoRaster  --config core.autocrlf=input
```

Otherwise, on MacOS and Linux:
```sh
git clone https://github.com/aghoshpro/OntoRaster
```


## Setup Docker

## Start Docker-compose

* Go to the `OntoRaster` repository
* Start the default Docker-compose file

```sh
docker-compose pull && docker-compose up
```

This command starts and initializes the database. Once the database is ready, it launches the SPARQL endpoint from Ontop at http://localhost:8080 .

For this tutorial, we assume that the ports 7777 (used for database) and 8080 (used by Ontop) are free. If you need to use different ports, please edit the file `.env`.

## Demo

First, stop the current docker-compose:
```sh
docker-compose stop
```

Then, specify the file by using *-f* : 
```sh
docker-compose -f docker-compose.ontoraster.yml up
```

This Docker-compose file uses the mapping `vkg/OntoRaster.obda`.

You can see it in Protégé by opening the ontology `vkg/OntoRaster.ttl` in a different window.

For example RasSPARQL queries are available at [endpoint](http://localhost:8082/).


## 2. Datasets
### 2.1 Vector Data
* Download [GADM data](https://gadm.org/download_country.html) GADM data (version 4.1) based on region of interest (ROI) such as Municipalities of Sweden, Germany, Italy.
* User can download vector shape or csv file of their own choice.
### 2.2 Raster Data
#### 2.2.1 MODIS LST TEMP 1 Km
* World: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)
* Sweden: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)
* Italy: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)
* Germany: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)
* India:


## Mapping

## To know more

Visit the official website of Ontop https://ontop-vkg.org, which also provides a more detailed tutorial.



