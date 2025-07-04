#!/usr/bin/env python3
"""
End-to-End Pipeline for Fine-tuning LLM for Natural Language to SPARQL Query Generation
Author: Claude
Description: Complete pipeline for training Llama models on ontology data to generate SPARQL queries
"""

import os
import json
import torch
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import rdflib
from rdflib import Graph, Namespace
import pandas as pd
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import Dataset
from peft import LoraConfig, get_peft_model, TaskType
import yaml
from tqdm import tqdm

from huggingface_hub import login
token = os.environ['HF_TOKEN']
# print(token)
# login('')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Config:
    """Configuration class for the pipeline"""
    # Model settings
    base_model: str = "mistralai/Mistral-7B-Instruct-v0.2"
    max_length: int = 2048
    temperature: float = 0.1
    
    # Training settings
    output_dir: str = "./results"
    num_train_epochs: int = 3
    per_device_train_batch_size: int = 2
    per_device_eval_batch_size: int = 2
    warmup_steps: int = 100
    learning_rate: float = 0.02
    
    # LoRA settings
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.1
    
    # Data paths
    ontology_dir: str = "./ontologies/"
    sparql_queries_file: str = "./data/sparql_queries.json"
    training_data_file: str = "./data/training_data.json"


class OntologyProcessor:
    """Process ontology files and extract relevant information"""
    
    def __init__(self, ontology_dir: str):
        self.ontology_dir = Path(ontology_dir)
        self.graphs = {}
        
    def load_ontologies(self) -> Dict[str, Graph]:
        """Load all ontology files from directory"""
        ontology_files = list(self.ontology_dir.glob("*.owl")) + \
                        list(self.ontology_dir.glob("*.ttl")) + \
                        list(self.ontology_dir.glob("*.rdf"))
        
        for file_path in ontology_files:
            try:
                g = Graph()
                if file_path.suffix == '.owl':
                    g.parse(file_path, format='application/rdf+xml')
                elif file_path.suffix == '.ttl':
                    g.parse(file_path, format='turtle')
                elif file_path.suffix == '.rdf':
                    g.parse(file_path, format='application/rdf+xml')
                
                self.graphs[file_path.stem] = g
                logger.info(f"Loaded ontology: {file_path.stem} with {len(g)} triples")
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
        
        return self.graphs
    
    def extract_schema_info(self) -> Dict[str, List[str]]:
        """Extract classes, properties, and relationships from ontologies"""
        schema_info = {
            'classes': [],
            'object_properties': [],
            'data_properties': [],
            'individuals': []
        }
        
        for name, graph in self.graphs.items():
            # Extract classes
            for subj, pred, obj in graph.triples((None, rdflib.RDF.type, rdflib.OWL.Class)):
                if isinstance(subj, rdflib.URIRef):
                    schema_info['classes'].append(str(subj))
            
            # Extract object properties
            for subj, pred, obj in graph.triples((None, rdflib.RDF.type, rdflib.OWL.ObjectProperty)):
                if isinstance(subj, rdflib.URIRef):
                    schema_info['object_properties'].append(str(subj))
            
            # Extract data properties
            for subj, pred, obj in graph.triples((None, rdflib.RDF.type, rdflib.OWL.DatatypeProperty)):
                if isinstance(subj, rdflib.URIRef):
                    schema_info['data_properties'].append(str(subj))
        
        return schema_info

class TrainingDataGenerator:
    """Generate training data from ontologies and SPARQL queries"""
    
    def __init__(self, schema_info: Dict[str, List[str]]):
        self.schema_info = schema_info
        
    def load_sparql_queries(self, queries_file: str) -> List[Dict]:
        """Load SPARQL queries from file"""
        if Path(queries_file).exists():
            with open(queries_file, 'r') as f:
                return json.load(f)
        else:
            # Create sample queries if file doesn't exist
            return self.create_sample_queries()
    
    def create_sample_queries(self) -> List[Dict]:
        """Create sample training data"""
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
            FILTER(?ndvi > 0.35) # NDVI Scale [0.1 (Desert) to >= 1.0 (Forest)]
            } 
            """
        }
        ]
        return sample_data
    
    def format_training_data(self, queries: List[Dict]) -> List[Dict]:
        """Format data for training with proper prompts"""
        formatted_data = []
        
        # Create schema context
        schema_context = self.create_schema_context()
        
        for item in queries:
            prompt = f"""Given the following ontology schema:
{schema_context}

Convert the following natural language question to a SPARQL query:
Question: {item['natural_language']}

SPARQL Query:"""
            
            response = item['sparql'].strip()
            
            formatted_data.append({
                'input': prompt,
                'output': response,
                'text': f"{prompt}\n{response}<|endoftext|>"
            })
        
        return formatted_data
    
    def create_schema_context(self) -> str:
        """Create a context string describing the ontology schema"""
        context = "Classes: " + ", ".join(self.schema_info['classes'][:10]) + "\n"
        context += "Object Properties: " + ", ".join(self.schema_info['object_properties'][:10]) + "\n"
        context += "Data Properties: " + ", ".join(self.schema_info['data_properties'][:10])
        return context

class ModelFineTuner:
    """Fine-tune the LLM model using LoRA"""
    
    def __init__(self, config: Config):
        self.config = config
        self.tokenizer = None
        self.model = None
        
    def setup_model_and_tokenizer(self):
        """Initialize model and tokenizer"""
        logger.info(f"Loading model: {self.config.base_model}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.base_model)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.config.base_model,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        
        # Configure LoRA
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=self.config.lora_r,
            lora_alpha=self.config.lora_alpha,
            lora_dropout=self.config.lora_dropout,
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj"]
        )
        
        self.model = get_peft_model(self.model, lora_config)
        self.model.print_trainable_parameters()
    
    def prepare_dataset(self, training_data: List[Dict]) -> Dataset:
        """Prepare dataset for training"""
        def tokenize_function(examples):
            return self.tokenizer(
                examples['text'],
                truncation=True,
                padding=True,
                max_length=self.config.max_length,
                return_tensors="pt"
            )
        
        dataset = Dataset.from_list(training_data)
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        return tokenized_dataset
    
    def train(self, training_data: List[Dict]):
        """Train the model"""
        logger.info("Preparing dataset...")
        train_dataset = self.prepare_dataset(training_data)
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=self.config.output_dir,
            num_train_epochs=self.config.num_train_epochs,
            per_device_train_batch_size=self.config.per_device_train_batch_size,
            per_device_eval_batch_size=self.config.per_device_eval_batch_size,
            warmup_steps=self.config.warmup_steps,
            learning_rate=self.config.learning_rate,
            logging_steps=10,
            save_steps=500,
            evaluation_strategy="steps",
            eval_steps=500,
            save_total_limit=2,
            load_best_model_at_end=True,
            report_to=None,  # Disable wandb
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,
        )
        
        # Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=train_dataset,  # Using same dataset for simplicity
            data_collator=data_collator,
        )
        
        logger.info("Starting training...")
        trainer.train()
        
        # Save the model
        trainer.save_model()
        self.tokenizer.save_pretrained(self.config.output_dir)

class SPARQLGenerator:
    """Generate SPARQL queries from natural language using fine-tuned model"""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )
    
    def generate_sparql(self, natural_language: str, schema_context: str = "") -> str:
        """Generate SPARQL query from natural language"""
        prompt = f"""Given the following ontology schema:
{schema_context}

Convert the following natural language question to a SPARQL query:
Question: {natural_language}

SPARQL Query:"""
        
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=256,
                temperature=0.1,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        sparql_query = generated_text[len(prompt):].strip()
        
        return sparql_query

def main():
    """Main pipeline execution"""
    config = Config()
    
    # Step 1: Process Ontologies
    logger.info("\nStep 1: Processing ontologies...")
    ontology_processor = OntologyProcessor(config.ontology_dir)
    graphs = ontology_processor.load_ontologies()
    schema_info = ontology_processor.extract_schema_info()
    
    # Step 2: Generate Training Data
    logger.info("\nStep 2: Generating training data...")
    data_generator = TrainingDataGenerator(schema_info)
    queries = data_generator.load_sparql_queries(config.sparql_queries_file)
    training_data = data_generator.format_training_data(queries)
    
    # Save training data
    with open(config.training_data_file, 'w') as f:
        json.dump(training_data, f, indent=2)
    
    # Step 3: Fine-tune Model
    logger.info("\nStep 3: Fine-tuning model...")
    fine_tuner = ModelFineTuner(config)
    fine_tuner.setup_model_and_tokenizer()
    fine_tuner.train(training_data)
    
    # Step 4: Test the model
    logger.info("\nStep 4: Testing the model...")
    generator = SPARQLGenerator(config.output_dir)
    
    test_questions = [
        "Find all sub-districts of Munich where elevation is above 490 meters",
        "Find all districts and schools of Munich where elevation is above 490 meters",
        "List all the churches in Munich where elevation is less than 520 meters"
    ]
    
    schema_context = data_generator.create_schema_context()
    
    for question in test_questions:
        sparql = generator.generate_sparql(question, schema_context)
        print(f"\nQuestion: {question}")
        print(f"\nGenerated SPARQL:\n{sparql}")
        print("-" * 50)

if __name__ == "__main__":
    # Ensure required directories exist
    os.makedirs("./ontologies", exist_ok=True)
    os.makedirs("./data", exist_ok=True)
    os.makedirs("./results", exist_ok=True)
    
    main()