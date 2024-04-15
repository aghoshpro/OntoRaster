# OntoRaster
Extension of Ontop, a VKG engine over multidimensional array database or Raster data combined with geomtrical data (e.g. Vector Data) and Relational Data

![OntoRaster](https://github.com/aghoshpro/OntoRaster/assets/71174892/d3d00767-20d3-4e52-bae7-c1a72fff5d17)

## Table of Contents
0. Pre-requisite Installation
1. [Installation](https://github.com/aghoshpro/myPhD/tree/main/RasDaMan#installation)


## 0. Pre-requisite Installation [for first time users]

(i) **Install Python 3.8 or more on Ubuntu 22.04**
Install the required dependency for adding custom PPAs.

* ```sudo apt install software-properties-common -y```

Then proceed and add the deadsnakes PPA to the APT package manager sources list as below.

* ```sudo add-apt-repository ppa:deadsnakes/ppa```

Press Enter to continue. Now download Python 3.10 with the single command below.

* ```sudo apt install python3.10```

Verify the installation by checking the installed version.
* ```python3 --version```

(ii) **install netcdf4 package**
``` sudo pip3 install netCDF4```

## 1. Installation
### 1.1. PostgreSQL Installation
### 1.2 Rasdaman Installation

* Source: https://doc.rasdaman.org/stable/02_inst-guide.html#installation-and-administration-guide

#### 1.2.1 Open terminal in Ubuntu 20.04 LTS 

```
wget -O - https://download.rasdaman.org/packages/rasdaman.gpg | sudo apt-key add -
```

```
echo "deb [arch=amd64] https://download.rasdaman.org/packages/deb focal stable" | sudo tee /etc/apt/sources.list.d/rasdaman.list
```

```
sudo apt-get update
```

```
sudo apt-get install rasdaman
```

```
source /etc/profile.d/rasdaman.sh
```

#### 1.2.2 Check if `rasql` is installed and set in path or not 
```
rasql -q 'select c from RAS_COLLECTIONNAMES as c' --out string
```
```
rasql: rasdaman query tool 10.0.5.
Opening database RASBASE at 127.0.0.1:7001... ok.
Executing retrieval query... ok.
Query result collection has 0 element(s):
rasql done
```

#### 1.2.3 Check petascope config 
#### [OGC Web Coverage Service Endpoint](http://localhost:8080/rasdaman/ows) 
```
$ cd /opt/rasdaman/etc
```
```
$  nano petascope.properties 
```
##### Default configuration of petascope for all DBMS.
```
spring.datasource.url=jdbc:postgresql://localhost:5432/petascopedb
spring.datasource.username=petauser
spring.datasource.password=petapasswd
spring.datasource.jdbc_jar_path=
```
#### 1.2.4 Status
```
service rasdaman start
service rasdaman stop
service rasdaman status
```

#### 1.2.5 Updating
```
sudo apt-get update
sudo service rasdaman stop
sudo apt-get install rasdaman
```

## 2. Datasets
### 2.1 Vector Data
* [Municipalities of Sweden](https://gadm.org/download_country.html) 
* [Municipalities of Bavaria](https://gadm.org/download_country.html) 
* [Municipalities of South Tyrol](https://gadm.org/download_country.html) 
### 2.2 Raster Data
#### 2.2.1 MODIS LST TEMP 1 Km
* World: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)
* Sweden: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)
* Italy: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)
* Germany: [Air Temperature](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html)
* India:
  
### 2.3 Data Exploration 
#### Check the metadata of data using [gdal](https://gdal.org/)
   * GeoTIFF
```
gdalinfo /home/arkaghosh/Downloads/RAS_DATA/MOD11A1.006_LST_Night_1km_doy2017001_aid0001.tif
```
   * netCDF
```
gdalinfo /home/arkaghosh/Downloads/RAS_DATA/air.mon.mean.v401.nc
```

## 3. Source Preparation
### 3.1 PostgrSQL
Create a database namned ~VectorTablesDB~. Then create extensions for POSTGIS,POSTGISraster, PlPython and dblink to enable ~VectorTablesDB~ database. 

```
-- Database: VectorDB

CREATE DATABASE "VectorDB"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE "VectorDB"
    IS 'Contains all vector data and relational data based on user's regions of interest (ROI)
    which will be used querying raster data stored in Rasdaman';
```
```
CREATE EXTENSION IF NOT EXISTS postgis;
-- enabling raster support
CREATE EXTENSION IF NOT EXISTS postgis_raster;
-- enabling plpython
CREATE EXTENSION IF NOT EXISTS plpython3u;
-- dblink
CREATE EXTENSION IF NOT EXISTS dblink;
```
Now we import the downloaded shapefiles into VectorTablesDB database using the `shp2pgsql` command. In this way, each shapefile is loaded into a separate tables like `region_Bavaria`, `region_Sweden` etc., in the VectorTablesDB database. Each one of these tables contains a column where geometries are stored in binary format (WKB) and an index has been built on that column. 

```
shp2pgsql -s 4326 /home/arkaghosh/Downloads/Bolzano/Vector/South_Tyrol_LOD3.shp region_Bavaria | psql -h localhost -p 5432 -U postgres -d VectorDB
shp2pgsql -s 4326 /home/arkaghosh/Downloads/Bolzano/Vector/South_Tyrol_LOD3.shp region_Sweden | psql -h localhost -p 5432 -U postgres -d VectorDB
shp2pgsql -s 4326 /home/arkaghosh/Downloads/Bolzano/Vector/South_Tyrol_LOD3.shp region_South_Tyrol | psql -h localhost -p 5432 -U postgres -d VectorDB
```





