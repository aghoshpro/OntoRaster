# Issues and Fixes

### Java Installation in Ubuntu [1,2,3,4]

```sh
apt search openjdk

sudo apt install openjdk-21-jdk openjdk-21

sudo apt-get update

export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64 && export PATH=$PATH:$JAVA_HOME/bin
```

```sh
$ java -version

> openjdk version "11.0.25" 2024-10-15
> OpenJDK Runtime Environment (build 11.0.25+9-post-Ubuntu-1ubuntu120.04)
> OpenJDK 64-Bit Server VM (build 11.0.25+9-post-Ubuntu-1ubuntu120.04, mixed mode, sharing)

```

```sh
$ echo $JAVA_HOME

echo $JAVA_HOME
usr/lib/jvm/java-11-openjdk-amd64
```

## References

### Books

1. <https://www.theoinf.uni-bayreuth.de/en/news/2021/Book-on-Database-Theory-in-the-works/index.html>
2. <https://kgbook.org/>
3. <http://webdam.inria.fr/Alice/>

### Web GIS Tools

1. <https://mapshaper.org/>
2. <https://simplemaps.com/gis/country/in#admin1>
3. <https://9revolution9.com/tools/geo/shp_geojson/>
4. <https://ogre.adc4gis.com/>
5. <https://python-charts.com/spatial/interactive-maps-folium/>
6. <https://leaflet-extras.github.io/leaflet-providers/preview/>
7. <https://en-us.topographic-map.com/>
8. <https://mapscaping.com/bounding-box-calculator/>

### Vector Data

1. <https://postgis.net/documentation/tips/lon-lat-or-lat-lon/>
2. <https://stackoverflow.com/questions/18636564/lat-long-or-long-lat>
3. <https://www.w3.org/2015/spatial/wiki/Coordinate_Reference_Systems>
4. <https://postgis.net/workshops/postgis-intro/geometries.html>
5. <https://www.ibm.com/docs/en/db2/11.5.x?topic=formats-geojson-format>
6. <https://gis.stackexchange.com/questions/13585/is-there-an-open-source-gis-to-view-and-edit-citygml-models>
7. <https://postgis.net/docs/ST_FlipCoordinates.html>
8. <https://www.reddit.com/r/gis/comments/1bu2c1h/crs84_epgs4326_wgs84/>
9. <https://macwright.com/lonlat/>
10. <https://spatialreference.org/>

### Raster Data

1. <https://sentiwiki.copernicus.eu/web/sentiwiki>
2. <https://dwtkns.com/srtm30m/>
3. <https://www.earthdata.nasa.gov/data/instruments/srtm>

### KG Construction

1. <https://schema.org/>
2. <https://w3c-cg.github.io/rdfsurfaces/>
3. <https://protegeproject.github.io/protege/views/class-description/>
4. <https://protegeproject.github.io/protege/views/class-hierarchy/#display-relationships>
5. <https://protegeproject.github.io/protege/class-expression-syntax/>
6. <https://training.parthenos-project.eu/sample-page/intro-to-ri/interoperability/what-are-knowledge-representation-systems-and-ontologies/#1547722765459-cd21269e-3130>
7. <https://python.langchain.com/v0.1/docs/use_cases/graph/constructing/#llm-graph-transformer>

### Latex

1. <https://www.overleaf.com/learn/latex/Articles/Unicode%2C_UTF-8_and_multilingual_text%3A_An_introduction>
2. <https://tex.stackexchange.com/questions/156964/guide-to-draw-charts-basic-pie-bar-from-data>

### StackOverflow

1. <https://askubuntu.com/questions/277806/how-to-set-java-home/1385764#1385764>
2. <https://stackoverflow.com/questions/60065441/java-home-variable-issues>
3. <https://stackoverflow.com/questions/14788345/how-to-install-the-jdk-on-ubuntu-linux>
4. <https://stackoverflow.com/questions/21343529/all-my-java-applications-now-throw-a-java-awt-headlessexception>
5. <https://stackoverflow.com/questions/42045767/how-can-i-change-the-x-axis-so-there-is-no-white-space/42045987#42045987>
6. <https://stackoverflow.com/questions/69886690/remove-empty-space-from-matplotlib-bar-plot>
7. <https://stackoverflow.com/questions/65104927/add-text-to-folium-map-using-an-absolute-position>
8. <https://stackoverflow.com/questions/3346396/in-semantic-web-are-owl-el-rl-ql-all-instances-of-dl-what-is-the-difference>
9. <https://stackoverflow.com/questions/24817607/why-must-rdfdatatype-subclass-rdfclass-in-rdf>
10. <https://github.com/RDFLib/sparqlwrapper/issues/124>
11. <https://sparqlwrapper.readthedocs.io/en/latest/main.html> <!-- ### SPARQLWrapper QueryBadFormed Error for long SELECT query [10, 11] -->
12. <https://gis.stackexchange.com/questions/222662/why-is-pgraster-much-slower>
13. <https://graphdb.ontotext.com/documentation/10.7/sql-access-over-jdbc.html>
14. <https://github.com/perrygeo/bbox-cheatsheet/tree/master>
15. <https://stackoverflow.com/questions/37738731/require-packages-in-my-script>
