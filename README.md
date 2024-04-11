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

#### Open terminal in Ubuntu 20.04 LTS 

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

#### Check if rasql is installed and set in path or not 
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

#### 3. Check that petascope is initialized properly at [OGC Web Coverage Service Endpoint](http://localhost:8080/rasdaman/ows) 


#### 4. Updating
```
sudo apt-get update
sudo service rasdaman stop
sudo apt-get install rasdaman
```
#### 5. Status
```
service rasdaman start
service rasdaman stop
service rasdaman status
```



