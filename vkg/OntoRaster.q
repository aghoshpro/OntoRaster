[QueryItem="check_rasdaman_conn"]
PREFIX : <http://www.semanticweb.org/arkaghosh/OntoRaster/>

select * {
?x rdfs:label ?output .
}


[QueryItem="Raster Spatial Average Based Vector Polygon geometry_wkt"]
PREFIX :	<http://www.semanticweb.org/arkaghosh/OntoRaster/>
PREFIX rdfs:	<http://www.w3.org/2000/01/rdf-schema#>
PREFIX geo:	<http://www.opengis.net/ont/geosparql#>
PREFIX rasdb:	<http://www.semanticweb.org/RasterDataCube/>

SELECT ?v {
?vector rdfs:label ?vector_region_name .
?vector geo:asWKT ?vector_region_wkt .
?raster rasdb:hasRasterName ?raster_name .
FILTER (?vector_region_name = 'München'
)FILTER (CONTAINS(?raster_name, 'Bavaria')
)BIND ('2023-07-24T00:00:00+00:00' AS ?timestamp
)BIND (rasdb:rasSpatialAverageFINAL(?timestamp, ?vector_region_wkt, ?raster_name) AS ?v)
}

[QueryItem="Raster Spatial Average Based Vector Multi-Polygon geometry_wkt"]
PREFIX :	<http://www.semanticweb.org/arkaghosh/OntoRaster/>
PREFIX rdfs:	<http://www.w3.org/2000/01/rdf-schema#>
PREFIX geo:	<http://www.opengis.net/ont/geosparql#>
PREFIX rasdb:	<http://www.semanticweb.org/RasterDataCube/>

SELECT ?v {
?vector rdfs:label ?vector_region_name .
?vector geo:asWKT ?vector_region_wkt .
?raster rasdb:hasRasterName ?raster_name .
FILTER (?vector_region_name = 'Göteborg  '
)FILTER (CONTAINS(?raster_name, 'Sweden')
)BIND ('2022-08-24T00:00:00+00:00' AS ?timestamp
)BIND (rasdb:rasSpatialAverageFINAL(?timestamp, ?vector_region_wkt, ?raster_name) AS ?v)
}


[QueryItem="Clip Raster Spatial Based Vector Polygon geometry_wkt"]
PREFIX :	<http://www.semanticweb.org/arkaghosh/OntoRaster/>
PREFIX rdfs:	<http://www.w3.org/2000/01/rdf-schema#>
PREFIX geo:	<http://www.opengis.net/ont/geosparql#>
PREFIX rasdb:	<http://www.semanticweb.org/RasterDataCube/>

SELECT ?v {
?vector rdfs:label ?vector_region_name .
?vector geo:asWKT ?vector_region_wkt .
?raster rasdb:hasRasterName ?raster_name .
FILTER (?vector_region_name = 'Castelrotto'
)FILTER (CONTAINS(?raster_name, 'Tyrol')
)BIND ('2023-09-24T00:00:00+00:00' AS ?timestamp
)BIND (rasdb:rasClipRaster(?timestamp, ?vector_region_wkt, ?raster_name) AS ?v)
}
