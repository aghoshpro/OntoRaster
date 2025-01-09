# Ontologies (**_O_**)

### 4.1. Raster Ontology

We have provided **Raster Ontology** ontology that describe meta-level information of $n-dimensional$ generic raster data or coverage based on the [OGC Coverage Implementation Schema (CIS)](https://docs.ogc.org/is/09-146r8/09-146r8.html) and the paper [Andrejev et al., 2015](https://www2.it.uu.se/research/group/udbl/publ/DSDIS2015.pdf). As of now it only describes only regular gridded coverage or geospatial raster data. The _RegularGridDomain_ and _RangeType_ classes capture all the information about the domains and ranges of a grid coverage.

<img src="diagrams/RasterOntology.png"/>

### 4.2. GeoSPARQL v1.1

For vector data we are using [GeoSPARQL v1.1 Ontology](https://opengeospatial.github.io/ogc-geosparql/geosparql11/index.html) introduces classes likes features, geometries, and their representation using Geography Markup Language (GML) and Well-Known Text (WKT) literals, and includes topological relationship vocabularies. GeoSPARQL also provides an extension of the standard SPARQL query interface, supporting a set of topological functions for quantitative reasoning.

### 4.3. CityGML v2.0

We are also using [CityGML v2.0 Ontology](https://cui.unige.ch/isi/ke/ontologies) developed by the University of Geneva for the ontology component of the KG construction phase and further modified by [Ding et al., 2024](https://doi.org/10.1080/10095020.2024.2337360) by adding further classes on addresses (including xAL) and removing object properties with the same IRI as data properties.

### 4.4. Quantities, Units, Dimensions and Types (QUDT)

The [QUDT](https://qudt.org) provides set of vocabularies representing the base classes properties, and restrictions used for modeling physical quantities, measurement units, and their dimensions in various measurement systems originally developed for the NASA Exploration Initiatives Ontology Models ([NExIOM](https://step.nasa.gov/pde2009/slides/20090506145822/PDE2009-NExIOM-TQ_v2.0-aRH-sFINAL.pdf)) project and now it forms the basis of the [NASA QUDT Handbook](http://ontolog.cim3.net/file/work/OntologyBasedStandards/2013-10-10_Case-for-QUOMOS/NASA-QUDT-Handbook-v10--RalphHodgson_20131010.pdf). QUDT aims to improve interoperability of data and the specification of information structures through industry standards for `Units of Measure (UoM)`, Quantity Kinds, Dimensions and Data Types as pointed out by [Ray et al., 2011](https://doi.org/10.25504/FAIRsharing.d3pqw7). This OWL schema is a foundation for a basic treatment of units which is considered for `Unit of Measurement (UoM)` in this work.

### 4.5. Open Street Map (OSM) ontology

- Defines classes of objects appearing on maps: roads, railways, water ways, amenities, emergency infrastructure, public transport, shops, tourist attractions, etc. This extensive ontology comprises over 660 classes, delineated according to the established set of OSM tags and their corresponding values. It was developed by Ontology Engineering Group ([link](https://smartcity.linkeddata.es/ontologies/mapserv.kt.agh.edu.plontologiesosm.owl.html)).

- **OSMonto**: An ontology of OpenStreetMap tags, created with the purpose to ease maintenance and overview of existing tags and to allow enriching the semantics of tags by relating them to other ontologies. It has been developed as a research paper [Mihai et al 2011](https://www.inf.unibz.it/~okutz/resources/osmonto.pdf) at University Bremen and DFKI Bremen and was presented at State of the Map Europe [SotM-EU'2011](https://stateofthemap.eu/index.html) and . An [.owl](https://raw.githubusercontent.com/doroam/planning-do-roam/master/Ontology/tags.owl) file containing the OSMonto ontology can be viewed in Protégé.

- [Open Street Map integration](https://documentation.researchspace.org/resource/Help:OpenStreetMap) : This integration creates a simple lookup service to federate against the Open Street Maps (OSM) API, allowing users to reference place names in their ResearchSpace instances. Users can lookup a street address, a city, a country etc. and be able to reference this in their data.
