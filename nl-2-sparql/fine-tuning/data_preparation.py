#!/usr/bin/env python3
"""
Enhanced Data Preparation Scripts
- SPARQL query templates generation
- Data augmentation
- Validation utilities
"""
import os
import json
import random
from typing import List, Dict
from pathlib import Path
import rdflib
from rdflib import Graph, Namespace, URIRef, Literal

class SPARQLTemplateGenerator:
    """Generate SPARQL query templates from ontology structure"""
    
    def __init__(self, graphs: Dict[str, Graph]):
        self.graphs = graphs
        self.templates = []
        
    def extract_common_patterns(self) -> List[Dict]:
        """Extract common SPARQL patterns from ontology"""
        patterns = []
        
        for name, graph in self.graphs.items():
            # Basic SELECT patterns
            patterns.extend(self._generate_basic_select_patterns(graph))
            # Filter patterns
            patterns.extend(self._generate_filter_patterns(graph))
            # Count patterns
            patterns.extend(self._generate_count_patterns(graph))
            # Optional patterns
            patterns.extend(self._generate_optional_patterns(graph))
            
        return patterns
    
    def _generate_basic_select_patterns(self, graph: Graph) -> List[Dict]:
        """Generate basic SELECT query patterns"""
        patterns = []
        
        # Find all classes
        classes = set()
        for subj, pred, obj in graph.triples((None, rdflib.RDF.type, rdflib.OWL.Class)):
            if isinstance(subj, URIRef):
                class_name = str(subj).split('/')[-1].split('#')[-1]
                classes.add(class_name)
        
        for class_name in list(classes)[:5]:  # Limit for demo
            patterns.append({
                "natural_language": f"Find all {class_name.lower()}s",
                "sparql": f"""
                SELECT ?item WHERE {{
                    ?item rdf:type ex:{class_name} .
                }}
                """,
                "pattern_type": "basic_select",
                "entity": class_name
            })
            
            patterns.append({
                "natural_language": f"What are the properties of {class_name.lower()}s?",
                "sparql": f"""
                SELECT ?item ?property ?value WHERE {{
                    ?item rdf:type ex:{class_name} .
                    ?item ?property ?value .
                }}
                """,
                "pattern_type": "property_exploration",
                "entity": class_name
            })
        
        return patterns
    
    def _generate_filter_patterns(self, graph: Graph) -> List[Dict]:
        """Generate FILTER query patterns"""
        patterns = []
        
        # Numeric filter examples
        patterns.append({
            "natural_language": "Find items with value greater than 100",
            "sparql": """
            SELECT ?item ?value WHERE {
                ?item ex:hasValue ?value .
                FILTER(?value > 100)
            }
            """,
            "pattern_type": "numeric_filter"
        })
        
        # String filter examples
        patterns.append({
            "natural_language": "Find items containing 'geo' in their label",
            "sparql": """
            SELECT ?item ?label WHERE {
                ?item rdfs:label ?label .
                FILTER(CONTAINS(LCASE(?label), "geo"))
            }
            """,
            "pattern_type": "string_filter"
        })
        
        return patterns
    
    def _generate_count_patterns(self, graph: Graph) -> List[Dict]:
        """Generate COUNT query patterns"""
        patterns = []
        
        classes = set()
        for subj, pred, obj in graph.triples((None, rdflib.RDF.type, rdflib.OWL.Class)):
            if isinstance(subj, URIRef):
                class_name = str(subj).split('/')[-1].split('#')[-1]
                classes.add(class_name)
        
        for class_name in list(classes)[:3]:
            patterns.append({
                "natural_language": f"How many {class_name.lower()}s are there?",
                "sparql": f"""
                SELECT (COUNT(?item) AS ?count) WHERE {{
                    ?item rdf:type ex:{class_name} .
                }}
                """,
                "pattern_type": "count",
                "entity": class_name
            })
        
        return patterns
    
    def _generate_optional_patterns(self, graph: Graph) -> List[Dict]:
        """Generate OPTIONAL query patterns"""
        patterns = []
        
        patterns.append({
            "natural_language": "Find all items and their optional descriptions",
            "sparql": """
            SELECT ?item ?description WHERE {
                ?item rdf:type ?type .
                OPTIONAL { ?item rdfs:comment ?description }
            }
            """,
            "pattern_type": "optional"
        })
        
        return patterns

class DataAugmentor:
    """Augment training data with variations"""
    
    def __init__(self):
        self.question_variations = {
            "find": ["find", "get", "retrieve", "show", "list", "display"],
            "what": ["what", "which", "tell me"],
            "how many": ["how many", "count", "number of"],
            "all": ["all", "every", "each"]
        }
    
    def augment_data(self, original_data: List[Dict]) -> List[Dict]:
        """Create variations of training data"""
        augmented = []
        
        for item in original_data:
            # Add original
            augmented.append(item)
            
            # Create variations
            variations = self._create_question_variations(item['natural_language'])
            for variation in variations:
                augmented.append({
                    "natural_language": variation,
                    "sparql": item['sparql'],
                    "original": False
                })
        
        return augmented
    
    def _create_question_variations(self, question: str) -> List[str]:
        """Create variations of a question"""
        variations = []
        question_lower = question.lower()
        
        # Simple word substitutions
        for key, alternatives in self.question_variations.items():
            if key in question_lower:
                for alt in alternatives:
                    if alt != key:
                        new_question = question_lower.replace(key, alt)
                        variations.append(new_question.capitalize())
        
        return variations[:2]  # Limit variations

class SPARQLValidator:
    """Validate SPARQL queries for syntax and executability"""
    
    def __init__(self, graph: Graph):
        self.graph = graph
    
    def validate_sparql(self, sparql_query: str) -> Dict[str, bool]:
        """Validate SPARQL query"""
        result = {
            "syntax_valid": False,
            "executable": False,
            "has_results": False,
            "error_message": ""
        }
        
        try:
            # Parse query
            parsed = self.graph.query(sparql_query)
            result["syntax_valid"] = True
            result["executable"] = True
            
            # Check if query returns results
            results = list(parsed)
            result["has_results"] = len(results) > 0
            
        except Exception as e:
            result["error_message"] = str(e)
        
        return result
    
    def validate_training_data(self, training_data: List[Dict]) -> List[Dict]:
        """Validate all SPARQL queries in training data"""
        validated_data = []
        
        for item in training_data:
            validation = self.validate_sparql(item['sparql'])
            item['validation'] = validation
            
            # Only include syntactically valid queries
            if validation['syntax_valid']:
                validated_data.append(item)
        
        return validated_data

def create_enhanced_training_data():
    """Create comprehensive training dataset"""
    
    # Load sample ontology (you would replace this with your actual ontologies)
    sample_data = [
        {
            "natural_language": "Find the dimension of a Raster dataset",
            "sparql": """
            PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
            PREFIX rasdb:	<https://github.com/aghoshpro/RasterDataCube/>

            SELECT ?rasterName ?dimension {
            ?gridCoverage a :Raster .
            ?gridCoverage rasdb:rasterName ?rasterName .
            FILTER (CONTAINS(?rasterName, ''))
            BIND (rasdb:rasDimension(?rasterName) AS ?dimension)
            }
            """
        },
        {
            "natural_language": "Find all districts of Munich where elevation is more than 515 meters",
            "sparql": """
            PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX geo:	 <http://www.opengis.net/ont/geosparql#>
            PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
            PREFIX lgdo: <http://linkedgeodata.org/ontology/>
            PREFIX rasdb: <https://github.com/aghoshpro/RasterDataCube/>

            SELECT ?distName ?elevation {
            ?region a :District ; rdfs:label ?distName ; geo:asWKT ?distWkt .
            ?gridCoverage a :Raster ; rasdb:rasterName ?rasterName .
            FILTER (CONTAINS(?rasterName, 'Elevation'))
            BIND ('2000-02-11T00:00:00+00:00'^^xsd:dateTime AS ?timeStamp)
            BIND (rasdb:rasSpatialAverage(?timeStamp, ?distWkt, ?rasterName) AS ?elevation)
            FILTER(?elevation > 515)
            } 
            """
        },
        {
            "natural_language": "Find all sub-districts of Munich where elevation is between 510-520 meters",
            "sparql": """
            PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX geo:	 <http://www.opengis.net/ont/geosparql#>
            PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
            PREFIX lgdo: <http://linkedgeodata.org/ontology/>
            PREFIX rasdb: <https://github.com/aghoshpro/RasterDataCube/>

            SELECT ?distName ?elevation {
            ?region a :SubDistrict ; rdfs:label ?distName ; geo:asWKT ?distWkt .
            ?gridCoverage a :Raster ; rasdb:rasterName ?rasterName .
            FILTER (CONTAINS(?rasterName, 'Elevation'))
            BIND ('2000-02-11T00:00:00+00:00'^^xsd:dateTime AS ?timeStamp)
            BIND (rasdb:rasSpatialAverage(?timeStamp, ?distWkt, ?rasterName) AS ?elevation)
            FILTER(?elevation > 510 && ?elevation < 520)
            }
            """
        },
        {
            "natural_language": " List locations of all the schools in Munich where average temperature is more than 275 Kelvin",
            "sparql": """
            PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX geo:	 <http://www.opengis.net/ont/geosparql#>
            PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
            PREFIX lgdo: <http://linkedgeodata.org/ontology/>
            PREFIX rasdb: <https://github.com/aghoshpro/RasterDataCube/>

            SELECT ?distName ?temp ?distWkt ?distWktColor ?distWktLabel ?bldgWkt ?bldgWktColor { # bldgName
            ?region a :District .
            ?region rdfs:label ?distName .
            ?region geo:asWKT ?distWkt .
            BIND(?distName AS ?distWktLabel)
            BIND('#008AFF5C' AS ?distWktColor)
            ?building a lgdo:School .
            #?building rdfs:label ?bldgName . ## ISSUE - if included some OSM null values are omitted 
            ?building geo:asWKT ?bldgWkt .
            BIND('red' AS ?bldgWktColor)
            FILTER (geof:sfWithin(?bldgWkt, ?distWkt))
            ?gridCoverage a :Raster .
            ?gridCoverage rasdb:rasterName ?rasterName .
            FILTER (CONTAINS(?rasterName, 'Munich_MODIS_Temperature_1km')) 
            BIND ('2022-01-01T00:00:00+00:00'^^xsd:dateTime AS ?timeStamp)
            BIND (rasdb:rasSpatialAverage(?timeStamp, ?distWkt, ?rasterName) AS ?temp)
            FILTER(?temp > 275) 
            } 
            """
        },
        {
            "natural_language": "List all the schools and districts in Munich where grass (or vegetation) is more green",
            "sparql": """
            PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX geo:	 <http://www.opengis.net/ont/geosparql#>
            PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
            PREFIX lgdo: <http://linkedgeodata.org/ontology/>
            PREFIX rasdb: <https://github.com/aghoshpro/RasterDataCube/>

            SELECT ?bldgName ?distName ?ndvi ?distWkt ?distWktColor ?bldgWkt ?bldgWktColor { # ?bldgLat ?bldgLon
            ?region a :District ; rdfs:label ?distName ; geo:asWKT ?distWkt . 
            ?building a lgdo:School ; rdfs:label ?bldgName ; geo:asWKT ?bldgWkt . # Churches, Parking, Hospital, Hotel
            BIND('#008AFF5C' AS ?distWktColor)
            BIND('red' AS ?bldgWktColor)
            #BIND(geof:latitude("?bldgWkt"^^geo:wktLiteral) AS ?bldgLat)
            #BIND(geof:longitude("?bldgWkt"^^geo:wktLiteral) AS ?bldgLon)
            FILTER (geof:sfWithin(?bldgWkt, ?distWkt))
            ?gridCoverage a :Raster ; rasdb:rasterName ?rasterName .
            FILTER (CONTAINS(?rasterName, 'NDVI')) 
            BIND ('2022-01-01T00:00:00+00:00'^^xsd:dateTime AS ?timeStamp) 
            BIND (rasdb:rasSpatialAverage(?timeStamp, ?distWkt, ?rasterName) AS ?ndvi)
            FILTER(?ndvi > 0.35)
            } 
            """
        }
    ]
    
    # Augment data
    augmentor = DataAugmentor()
    augmented_data = augmentor.augment_data(sample_data)
    
    # Format for training
    formatted_data = []
    for item in augmented_data:
        formatted_data.append({
            "input": f"Convert this natural language question to SPARQL: {item['natural_language']}",
            "output": item['sparql'].strip(),
            "text": f"Convert this natural language question to SPARQL: {item['natural_language']}\n\n{item['sparql'].strip()}<|endoftext|>"
        })
    
    return formatted_data

if __name__ == "__main__":
    # Create enhanced training data
    training_data = create_enhanced_training_data()
    
    # Save to file
    output_file = "./natual2sparql/data/prepped_training_data.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(training_data, f, indent=2)
    
    print(f"Created {len(training_data)} training examples")
    print(f"Saved to {output_file}")