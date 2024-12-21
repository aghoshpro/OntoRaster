# Technical Issues and how to fix them

## Install Java and set `JAVA_HOME` in Ubuntu [1,2,3,4]

```sh
$ apt search openjdk

$ sudo apt install openjdk-21-jdk openjdk-21

$ sudo apt-get update

$ export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64 && export PATH=$PATH:$JAVA_HOME/bin
```

```
$ java -version

> openjdk version "11.0.25" 2024-10-15
> OpenJDK Runtime Environment (build 11.0.25+9-post-Ubuntu-1ubuntu120.04)
> OpenJDK 64-Bit Server VM (build 11.0.25+9-post-Ubuntu-1ubuntu120.04, mixed mode, sharing)

```

```
$ echo $JAVA_HOME

echo $JAVA_HOME
usr/lib/jvm/java-11-openjdk-amd64
```

|  ID | Dataset Name                  | Dataset ID | Parameter              | Min Value | Scale Factor | Min Longitude | Max Longitude | Lon Units | Lon Points | Lon Res | Min Latitude | Max Latitude | Lat Units | Lat Points | Lat Res | Start Date | End Date   | Status | Days | Version |
| --: | :---------------------------- | :--------- | :--------------------- | --------: | -----------: | ------------: | ------------: | --------: | ---------: | ------: | -----------: | -----------: | --------: | ---------: | ------: | :--------- | :--------- | -----: | ---: | ------: |
|  64 | Munich_MODIS_Temperature_1km  | 82         | LandSurfaceTemperature |         0 |         0.02 |     11.358333 |     11.725000 |         0 |         43 |    0.01 |    48.058333 |    48.250000 |         0 |         22 |    0.01 | 2022-01-01 | 2024-11-07 |      0 | 1028 |       1 |
|  41 | Munich_SRTM_NC_Elevation      | 59         | DEM                    |    -32768 |            1 |     11.360694 |     11.723194 |         0 |       1304 |       0 |    48.061528 |    48.248194 |         0 |        671 |       0 | 2000-02-11 | 2000-02-11 |      0 |    0 |       1 |
| 110 | Munich_MODIS_SnowCover        | 128        | SnowCover              |       200 |            1 |     11.358333 |     11.725000 |         0 |         87 |       0 |    48.058333 |    48.250000 |         0 |         45 |       0 | 2023-12-01 | 2024-11-30 |      0 |  365 |       1 |
|  18 | Bavaria_Temperature_MODIS_1km | 36         | LST_Night_1km          |         0 |            1 |      8.975000 |     13.841667 |         0 |        583 |    0.01 |    47.266667 |    50.566667 |         0 |        395 |    0.01 | 2023-01-01 | 2023-10-31 |      0 |  303 |       1 |
|  87 | Munich_MODIS_NDVI             | 105        | NDVI                   |     -3000 |       0.0001 |     11.360417 |     11.725000 |         0 |        174 |       0 |    48.060417 |    48.250000 |         0 |         90 |       0 | 2021-12-19 | 2024-10-15 |      0 |   65 |       1 |

# StackOverflow

1. https://askubuntu.com/questions/277806/how-to-set-java-home/1385764#1385764
2. https://stackoverflow.com/questions/60065441/java-home-variable-issues
3. https://stackoverflow.com/questions/14788345/how-to-install-the-jdk-on-ubuntu-linux
4. https://stackoverflow.com/questions/21343529/all-my-java-applications-now-throw-a-java-awt-headlessexception
