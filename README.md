# OntoRaster
Extension of Ontop, a VKG engine over multidimensional array database or Raster data combined with geomtrical data (e.g. Vector Data) and Relational Data

![OntoRaster](https://github.com/aghoshpro/OntoRaster/assets/71174892/bbf751b2-78fc-43e0-8225-825f3228c902)

## Table of Contents
0. [Pre-requisite Installation](https://github.com/aghoshpro/OntoRaster/blob/main/README.md#0-pre-requisite-installation-for-first-time-users) 
1. [Installation](https://github.com/aghoshpro/myPhD/tree/main/RasDaMan#installation)
2. [Datasets](https://github.com/aghoshpro/OntoRaster#2-datasets)
3. [Source Preperation](https://github.com/aghoshpro/OntoRaster#3-source-preparation)
4. [Query Answering](https://github.com/aghoshpro/OntoRaster#4-queries)


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
```
$ sudo service postgresql status

● postgresql.service - PostgreSQL RDBMS
     Loaded: loaded (/lib/systemd/system/postgresql.service; enabled; vendor preset: enabled)
     Active: active (exited) since Tue 2023-07-25 14:36:14 IST; 23min ago
    Process: 1432 ExecStart=/bin/true (code=exited, status=0/SUCCESS)
   Main PID: 1432 (code=exited, status=0/SUCCESS)

Jul 25 14:36:14 lat7410g systemd[1]: Starting PostgreSQL RDBMS...
Jul 25 14:36:14 lat7410g systemd[1]: Finished PostgreSQL RDBMS.
```
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
* Download [GADM data](https://gadm.org/download_country.html) GADM data (version 4.1) based on region of interest (ROI) such as Municipalities of Sweden, Germany, Italy.
* User can download vector shape or csv file of their own choice.
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
Create a database namned *VectorTablesDB*. Then create extensions for POSTGIS,POSTGISraster, PlPython and dblink to enable VectorTablesDB database. 

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
$ shp2pgsql -s 4326 /path_to_shapefile/Bavaria_mun.shp region_Bavaria | psql -h localhost -p 5432 -U postgres -d VectorDB
$ shp2pgsql -s 4326 /path_to_shapefile/Sweden_mun.shp region_Sweden | psql -h localhost -p 5432 -U postgres -d VectorDB
$ shp2pgsql -s 4326 /path_to_shapefile/South_Tyrol_LOD3.shp region_South_Tyrol | psql -h localhost -p 5432 -U postgres -d VectorDB
```

### 3.2 Raster Data

To import data into Rasdaman a shell command `wcst_import.sh` is used and takes follwing two inputs:

* ```Recipe``` - A recipe is a class implementing the BaseRecipe that based on a set of parameters (ingredients) can import a set of files into WCS forming a well defined structure (image, regular timeseries, irregular timeseries etc). 4 types of recipe are as follows (General Recipe,Mosaic Map, Regular Timeseries, Irregular Timeseries) [List of recipes](http://rasdaman.org/browser/applications/wcst_import/recipes?order=name)

* ```Ingredients``` - An ingredients file is a json file containing a set of parameters that define how the recipe should behave (e.g. the WCS endpoint, the CRS resolver etc are all ingredients). [List of ingredients](http://rasdaman.org/browser/applications/wcst_import/ingredients/possible_ingredients.json)

**NOTE** Its only input is an "**ingredient**" file telling everything about the import process that the utility needs to know. (On a side note, such ingredients files constitute an excellent [documentation](http://rasdaman.org/wiki/WCSTImportGuide).)

#### 3.2.1 NetCDF Format
#### **DATA**: [/Datasets/udel.airt.precip/v401/air.mon.mean.v401.nc](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html) 
* **Temporal Resolution**: Monthly values for 1901/01 - 2014/12 (V4.01)
* **Spatial Coverage**: 0.5 degree latitude x 0.5 degree longitude | global grid (720x360) | 3D datacube (time x lat x long = 1380 x 720 x 360).

#### **Ingredient File (AIR_TEMP_RAS_X.json)**
```{
    "config": {
        "service_url": "http://localhost:8080/rasdaman/ows",
        "tmp_directory": "/tmp/",
        "mock": false,
        "automated": true,
        "track_files": false
    },
    "input": {
        "coverage_id":"AIR_TEMP_X",
        "paths": [
            "/home/arkaghosh/Downloads/RAS_DATA/air.mon.mean.v401.nc"
        ]
    },
    "recipe": {
        "name": "general_coverage",
        "options": {
            "coverage": {
                "crs": "OGC/0/AnsiDate@EPSG/0/4326",
                "metadata": {
                    "type": "xml",
                    "global": "auto"
                },
                "slicer": {
                    "type": "netcdf",
                    "pixelIsPoint": true,
                    "bands": [{
                        "name": "air",
                        "variable": "air",
                        "description": "Air Temperature",
                        "identifier": "air",
                        "nilvalue":"-9.96921e+36f"
                    }],
                    "axes": {
                        "ansi": {
                            "statements": "from datetime import datetime, timedelta",
                             "min": "(datetime(1900,1,1,0,0,0) + timedelta(hours=${netcdf:variable:time:min})).strftime(\"%Y-%m-%dT%H:%M\")",
                             "max": "(datetime(1900,1,1,0,0,0) + timedelta(hours=${netcdf:variable:time:max})).strftime(\"%Y-%m-%dT%H:%M\")",
                            "directPositions": "[(datetime(1900,1,1,0,0,0) + timedelta(hours=x)).strftime(\"%Y-%m-%dT%H:%M\") for x in ${netcdf:variable:time}]",
                            "gridOrder": 0,
                            "type": "ansidate",
                            "resolution": 1,
                            "irregular": true
                        },
                        "Long": {
                            "min": "${netcdf:variable:lon:min}",
                            "max": "${netcdf:variable:lon:max}",
                            "gridOrder": 2,
                            "resolution": "${netcdf:variable:lon:resolution}"
                        },
                        "Lat": {
                            "min": "${netcdf:variable:lat:min}",
                            "max": "${netcdf:variable:lat:max}",
                            "gridOrder": 1,
                            "resolution": "-${netcdf:variable:lat:resolution}"
                        }
                    }
                }
            },
            "tiling": "ALIGNED [0:0, 0:359, 0:719]" 
        }
    }
}
```
### Output [```241.82``` MB has expanded to ```1.43``` GB after successful ingestion in ```16.03``` seconds]
#### Output in terminal

```
$ wcst_import.sh /home/arkaghosh/Downloads/RASDAMAN_FINALE/AIR_TEMP_RAS_X.json
```
```
wcst_import.sh: rasdaman v10.0.5 build gf81f9b82
Collected first 1 files: ['/home/arkaghosh/Downloads/RAS_DATA/air.mon.mean.v401.nc']...
The recipe has been validated and is ready to run.
Recipe: general_coverage
Coverage: AIR_TEMP_X
WCS Service: http://localhost:8080/rasdaman/ows
Operation: INSERT
Subset Correction: False
Mocked: False
WMS Import: True
Import mode: Blocking
Analyzing file (1/1): /home/arkaghosh/Downloads/RAS_DATA/air.mon.mean.v401.nc ...
Elapsed time: 0.081 s.
All files have been analyzed. Please verify that the axis subsets of the first 1 files above are correct.
Slice 1: {Axis Subset: ansi("1900-01-01T00:00:00+00:00","2014-12-01T00:00:00+00:00") Lat(-90.00,90.00) Long(0.000,360.000) 
Data Provider: file:///home/arkaghosh/Downloads/RAS_DATA/air.mon.mean.v401.nc}

Progress: [------------------------------] 0/1 0.00% 
[2022-11-22 13:41:03] coverage 'AIR_TEMP_X' - 1/1 - file 'air.mon.mean.v401.nc' - grid domains [0:1379,0:359,0:719] of size 241.82 MB; Total time to ingest file 16.03 s @ 15.09 MB/s.
Progress: [##############################] 1/1 100.00% Done.

```
#### **Output Screenshot**
![Screenshot from 2022-11-22 13-49-12](https://user-images.githubusercontent.com/71174892/203321589-6abc0681-6488-4e83-a42c-96dd689cba33.png)



### 3.2.2 GeoTIFF Format
**Data**: [MOD11A1.006 Terra Land Surface Temperature and Emissivity Daily Global 1km](https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD11A1#bands)
Here I have ingested 3 MODIS Daily LST geotiff file each of size 334 MB. Each image has a spatial dimention of 43099 X 20757.

#### **Ingredient File (general_coverage_gdal_LST_Timeseries.json)**
```{
  "config": {
    "service_url": "http://localhost:8080/rasdaman/ows",
    "tmp_directory": "/tmp/",
    "crs_resolver": "http://localhost:8080/def/",
    "default_crs": "http://www.opengis.net/def/crs/EPSG/0/4326",
    "mock": false,
    "automated": true
  },
  "input": {
    "coverage_id": "LST_03_GeoTIFF",
    "paths": [
      "/home/arkaghosh/Downloads/RAS_DATA/MODIS/*.tif"
    ]
  },
  "recipe": {
    "name": "time_series_irregular",
    "options": {
      "time_parameter": {
        "filename": {
          "__comment__": "The regex has to contain groups of tokens, separated by parentheses. The group parameter specifies which regex group to use for retrieving the time value",
          "regex": "(.*)_(.*)_doy(.+?)_(.*)",
          "group": "3"
        },
        "datetime_format": "YYYYMMDD"
      },
      "time_crs": "http://localhost:8080/def/crs/OGC/0/AnsiDate",
      "tiling": "ALIGNED [0:*,0:43098, 0:20756]"
    }
  }
}

```
### Output [```1``` GB has expanded to ```10``` GB after successful ingestion in ```143.03``` seconds]
#### Output in terminal
```
$ wcst_import.sh /home/arkaghosh/Downloads/RASDAMAN_FINALE/general_coverage_gdal_LST_Timeseries.json
```
```
wcst_import.sh: rasdaman v10.1.3 build g47ad85de
Collected first 3 files: ['/home/arkaghosh/Downloads/RAS_DATA/MODIS/MOD11A1.006_LST_Night_1km_doy20170101_aid0001.tif', '/home/arkaghosh/Downloads/RAS_DATA/MODIS/MOD11A1.006_LST_Night_1km_doy20170115_aid0001.tif', '/home/arkaghosh/Downloads/RAS_DATA/MODIS/MOD11A1.006_LST_Night_1km_doy20170126_aid0001.tif']...
The recipe has been validated and is ready to run.
Recipe: time_series_irregular
Coverage: LST_03_GeoTIFF
WCS Service: http://localhost:8080/rasdaman/ows
Operation: INSERT
Subset Correction: False
Mocked: False
WMS Import: True
Import mode: Blocking
Track files: True
Analyzing file (1/3): /home/arkaghosh/Downloads/RAS_DATA/MODIS/MOD11A1.006_LST_Night_1km_doy20170101_aid0001.tif ...
Elapsed time: 0.001 s.
Analyzing file (2/3): /home/arkaghosh/Downloads/RAS_DATA/MODIS/MOD11A1.006_LST_Night_1km_doy20170115_aid0001.tif ...
Elapsed time: 0.001 s.
Analyzing file (3/3): /home/arkaghosh/Downloads/RAS_DATA/MODIS/MOD11A1.006_LST_Night_1km_doy20170126_aid0001.tif ...
Elapsed time: 0.001 s.
All files have been analyzed. Please verify that the axis subsets of the first 3 files above are correct.
Slice 1: {Axis Subset: ansi("2017-01-01T00:00:00+00:00") Lat(-84.658333325730799103,88.31666665873561) Lon(-179.15833331724446,179.999999983835549921) 
Data Provider: file:///home/arkaghosh/Downloads/RAS_DATA/MODIS/MOD11A1.006_LST_Night_1km_doy20170101_aid0001.tif}

Slice 2: {Axis Subset: ansi("2017-01-15T00:00:00+00:00") Lat(-84.658333325730799103,88.31666665873561) Lon(-179.15833331724446,179.999999983835549921) 
Data Provider: file:///home/arkaghosh/Downloads/RAS_DATA/MODIS/MOD11A1.006_LST_Night_1km_doy20170115_aid0001.tif}

Slice 3: {Axis Subset: ansi("2017-01-26T00:00:00+00:00") Lat(-84.658333325730799103,88.31666665873561) Lon(-179.15833331724446,179.999999983835549921) 
Data Provider: file:///home/arkaghosh/Downloads/RAS_DATA/MODIS/MOD11A1.006_LST_Night_1km_doy20170126_aid0001.tif}

Progress: [------------------------------] 0/1 0.00% 
[2023-02-17 21:24:43] coverage 'LST_03_GeoTIFF' - 1/3 - file 'MOD11A1.006_LST_Night_1km_doy20170101_aid0001.tif' - grid domains [0,0:20756,0:43098] of size 338.81 MB; Total time to ingest file 34.84 s @ 9.72 MB/s.
Progress: [------------------------------] 0/1 0.00% 
[2023-02-17 21:25:18] coverage 'LST_03_GeoTIFF' - 2/3 - file 'MOD11A1.006_LST_Night_1km_doy20170115_aid0001.tif' - grid domains [0,0:20756,0:43098] of size 361.2 MB; Total time to ingest file 35.31 s @ 10.23 MB/s.
Progress: [------------------------------] 0/1 0.00% 
[2023-02-17 21:25:53] coverage 'LST_03_GeoTIFF' - 3/3 - file 'MOD11A1.006_LST_Night_1km_doy20170126_aid0001.tif' - grid domains [0,0:20756,0:43098] of size 307.71 MB; Total time to ingest file 34.19 s @ 9.0 MB/s.
Progress: [##############################] 1/1 100.00% Done.
Recipe executed successfully
```
#### Output Screenshot
![image](https://user-images.githubusercontent.com/71174892/219706205-8a217e48-0afe-4cdc-aa3f-ca03e2d07bd4.png)

#### Output Endpoint
![image](https://user-images.githubusercontent.com/71174892/219706500-7e78936a-13b8-4085-b120-c1659db55962.png)


### 3.2 Mappings
```
[PrefixDeclaration]
:		http://www.semanticweb.org/arkaghosh/OntoRaster/
geo:		http://www.opengis.net/ont/geosparql#
owl:		http://www.w3.org/2002/07/owl#
rdf:		http://www.w3.org/1999/02/22-rdf-syntax-ns#
xml:		http://www.w3.org/XML/1998/namespace
xsd:		http://www.w3.org/2001/XMLSchema#
obda:		https://w3id.org/obda/vocabulary#
rdfs:		http://www.w3.org/2000/01/rdf-schema#
sosa:		http://www.w3.org/ns/sosa/
rasdb:		http://www.semanticweb.org/RasterDataCube/

[MappingDeclaration] @collection [[
mappingId	mapping_region_class
target		:region/{gid} a :region .
source		select gid from region_bavaria;

mappingId	mapping_region_name
target		:region/{gid} rdfs:label {region_name}^^xsd:string .
source		select gid, name_2 as region_name from region_bavaria;

mappingId	mapping_region_geometry
target		:region/{gid} geo:asWKT {geometry}^^geo:wktLiteral .
source		select gid, st_astext((st_dump(geom)).geom) as geometry from region_bavaria

mappingId	mapping_rastername
target		:raster/{raster_id} rasdb:hasRasterName {raster_name}^^xsd:string .
source		select raster_id, raster_name from petascopedb01;

mappingId	mapping_datetime
target		:raster/{raster_id} rasdb:hasStartTime {dom_lower_bound}^^xsd:integer ; rasdb:hasEndTime {dom_upper_bound}^^xsd:integer .
source		select raster_id, dom_lower_bound, dom_upper_bound from petascopedb01;

mappingId	mapping_scale_factor
target		:raster/{raster_id} rasdb:hasScaleFactor {scale_factor}^^xsd:double .
source		select raster_id, scale_factor from petascopedb01;
]]

```
### 3.2 Ontologies

## 4. Query Answering
We are using **GeoSPARQL** for vector data and **rasSPARQL** for raster data.
### 4.1 Simple Queries
### 4.2 Aggregated Queries

#### 4.2.1 SPATIAL AVERAGE
* **INPUT -** "FILTER (?region_name = `'Deggendorf'`\n)" and `rasdb:rasSpatialAverage(100, ?ras_sf, ?region, ?raster_name)`
* **OUTPUT -** `"277.08"^^xsd:double`
```
    "PREFIX :\t<http://www.semanticweb.org/arkaghosh/OntoRaster/>\n"
    "PREFIX rdfs:\t<http://www.w3.org/2000/01/rdf-schema#>\n"
    "PREFIX geo:\t<http://www.opengis.net/ont/geosparql#>\n"
    "PREFIX rasdb:\t<http://www.semanticweb.org/RasterDataCube/>\n"
               
    + "SELECT ?v {\n"
    + "?r rdfs:label ?region_name .\n"
    + "?x rasdb:hasRasterName ?raster_name .\n"
    + "?x rasdb:hasScaleFactor ?ras_sf .\n"
    + "?r geo:asWKT ?region .\n" 
    + "FILTER (?region_name = 'Deggendorf'\n)" // Regen Erding Kelheim
    + "BIND (`rasdb:rasSpatialAverage`(100, ?ras_sf, ?region, ?raster_name) AS ?v)"
    + "}\n";
```
* **Expected Output :** `"274.998"^^xsd:double`

#### 4.2.2 SPATIAL Maximum
* **INPUT -** "FILTER (?region_name = `'Deggendorf'`\n)" and `rasdb:rasSpatialMaximum(100, ?ras_sf, ?region, ?raster_name)`
* **OUTPUT -** `"277.08"^^xsd:double`
```
    "PREFIX :\t<http://www.semanticweb.org/arkaghosh/OntoRaster/>\n"
    "PREFIX rdfs:\t<http://www.w3.org/2000/01/rdf-schema#>\n"
    "PREFIX geo:\t<http://www.opengis.net/ont/geosparql#>\n"
    "PREFIX rasdb:\t<http://www.semanticweb.org/RasterDataCube/>\n"
               
    + "SELECT ?v {\n"
    + "?r rdfs:label ?region_name .\n"
    + "?x rasdb:hasRasterName ?raster_name .\n"
    + "?x rasdb:hasScaleFactor ?ras_sf .\n"
    + "?r geo:asWKT ?region .\n" 
    + "FILTER (?region_name = 'Deggendorf'\n)" // Regen Erding Kelheim
    + "BIND (rasdb:rasSpatialMaximum(100, ?ras_sf, ?region, ?raster_name) AS ?v)"
    + "}\n";
```


#### 4.2.3 SPATIAL Minimum
* **INPUT -** "FILTER (?region_name = `'Deggendorf'`\n)" and `rasdb:rasSpatialMinimum(100, ?ras_sf, ?region, ?raster_name)`
* **OUTPUT -** `"272.88"^^xsd:double`
```
     "PREFIX :\t<http://www.semanticweb.org/arkaghosh/OntoRaster/>\n"
     + "PREFIX rdfs:\t<http://www.w3.org/2000/01/rdf-schema#>\n"
     + "PREFIX geo:\t<http://www.opengis.net/ont/geosparql#>\n"
     + "PREFIX rasdb:\t<http://www.semanticweb.org/RasterDataCube/>\n"
     + "SELECT ?v {\n"
     + "?r rdfs:label ?region_name .\n"
     + "?x rasdb:hasRasterName ?raster_name .\n"
     + "?x rasdb:hasScaleFactor ?ras_sf .\n"
     + "?r geo:asWKT ?region .\n"
     + "FILTER (?region_name = 'Deggendorf'\n)"
     + "BIND (rasdb:rasSpatialMinimum(100, ?ras_sf, ?region, ?raster_name) AS ?v)"
     + "}\n";
```





