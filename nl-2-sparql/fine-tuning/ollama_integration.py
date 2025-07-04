#!/usr/bin/env python3
"""
Ollama Integration for serving fine-tuned models
- Convert fine-tuned model to GGUF format
- Create Ollama Modelfile
- Serve model via Ollama
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Optional
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import requests

class OllamaModelConverter:
    """Convert fine-tuned model to Ollama-compatible format"""
    
    def __init__(self, model_path: str, output_dir: str = "./ollama_models"):
        self.model_path = Path(model_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def create_modelfile(self, model_name: str = "nl2sparql") -> str:
        """Create Ollama Modelfile"""
        modelfile_content = f"""
FROM {self.model_path}/pytorch_model.bin

TEMPLATE \"\"\"
Convert the following natural language question to a SPARQL query:

Question: {{{{ .Prompt }}}}

SPARQL Query:
\"\"\"

PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER num_ctx 2048

SYSTEM \"\"\"
You are an expert at converting natural language questions into SPARQL queries. 
You have knowledge of RDF, OWL ontologies, and semantic web technologies.
Always generate syntactically correct SPARQL queries with proper prefixes.
\"\"\"
"""
        
        modelfile_path = self.output_dir / f"{model_name}.Modelfile"
        with open(modelfile_path, 'w') as f:
            f.write(modelfile_content)
        
        return str(modelfile_path)
    
    def build_ollama_model(self, model_name: str = "nl2sparql") -> bool:
        """Build model in Ollama"""
        try:
            modelfile_path = self.create_modelfile(model_name)
            
            # Build model using Ollama CLI
            cmd = f"ollama create {model_name} -f {modelfile_path}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Successfully built Ollama model: {model_name}")
                return True
            else:
                print(f"Error building model: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error: {e}")
            return False

class SPARQLQueryService:
    """Service for generating SPARQL queries using Ollama"""
    
    def __init__(self, model_name: str = "nl2sparql", ollama_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.ollama_url = ollama_url
        
    def generate_sparql(self, natural_language: str, schema_context: str = "") -> str:
        """Generate SPARQL query from natural language"""
        
        prompt = natural_language
        if schema_context:
            prompt = f"Given the ontology schema:\n{schema_context}\n\nQuestion: {natural_language}"
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "top_p": 0.9,
                        "num_ctx": 2048
                    }
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error connecting to Ollama: {e}"
    
    def test_model(self, test_questions: list = None):
        """Test the model with sample questions"""
        if test_questions is None:
            test_questions = [
                "Find all cities in Germany",
                "What is the population of Berlin?",
                "List countries with their capitals",
                "How many geographic features are there?",
                "Find places with elevation above 1000 meters"
            ]
        
        print(f"Testing model: {self.model_name}")
        print("=" * 50)
        
        for question in test_questions:
            print(f"\nQuestion: {question}")
            sparql = self.generate_sparql(question)
            print(f"Generated SPARQL:\n{sparql}")
            print("-" * 30)

class WebInterface:
    """Simple web interface for the NL2SPARQL service"""
    
    def __init__(self, service: SPARQLQueryService):
        self.service = service
    
    def create_gradio_interface(self):
        """Create Gradio web interface"""
        try:
            import gradio as gr
        except ImportError:
            print("Gradio not installed. Install with: pip install gradio")
            return None
        
        def generate_query(question, schema_context=""):
            """Generate SPARQL query from natural language"""
            return self.service.generate_sparql(question, schema_context)
        
        # Create interface
        interface = gr.Interface(
            fn=generate_query,
            inputs=[
                gr.Textbox(
                    label="Natural Language Question",
                    placeholder="e.g., Find all cities in Germany",
                    lines=2
                ),
                gr.Textbox(
                    label="Schema Context (Optional)",
                    placeholder="Ontology classes and properties...",
                    lines=5
                )
            ],
            outputs=gr.Code(
                label="Generated SPARQL Query",
                language="sparql"
            ),
            title="Natural Language to SPARQL Converter",
            description="Convert natural language questions to SPARQL queries using fine-tuned LLM",
            examples=[
                ["Find all cities in Germany", ""],
                ["What is the population of Berlin?", ""],
                ["List countries with their capitals", ""],
                ["How many geographic features are there?", ""]
            ]
        )
        
        return interface

class FastAPIService:
    """FastAPI service for REST API"""
    
    def __init__(self, service: SPARQLQueryService):
        self.service = service
    
    def create_api(self):
        """Create FastAPI application"""
        try:
            from fastapi import FastAPI, HTTPException
            from pydantic import BaseModel
        except ImportError:
            print("FastAPI not installed. Install with: pip install fastapi uvicorn")
            return None
        
        app = FastAPI(title="NL2SPARQL API", version="1.0.0")
        
        class QueryRequest(BaseModel):
            question: str
            schema_context: str = ""
        
        class QueryResponse(BaseModel):
            question: str
            sparql_query: str
            success: bool
        
        @app.post("/generate", response_model=QueryResponse)
        async def generate_sparql(request: QueryRequest):
            try:
                sparql = self.service.generate_sparql(
                    request.question, 
                    request.schema_context
                )
                return QueryResponse(
                    question=request.question,
                    sparql_query=sparql,
                    success=True
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.get("/health")
        async def health_check():
            return {"status": "healthy", "model": self.service.model_name}
        
        return app

def setup_ollama_environment():
    """Setup Ollama environment and dependencies"""
    print("Setting up Ollama environment...")
    
    # Check if Ollama is installed
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Ollama version: {result.stdout.strip()}")
        else:
            print("Ollama not found. Please install from https://ollama.ai")
            return False
    except FileNotFoundError:
        print("Ollama not found. Please install from https://ollama.ai")
        return False
    
    # Start Ollama service
    print("Starting Ollama service...")
    try:
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Ollama service started")
    except Exception as e:
        print(f"Error starting Ollama: {e}")
    
    return True

def main():
    """Main function to demonstrate the complete pipeline"""
    
    # Setup Ollama
    if not setup_ollama_environment():
        return
    
    # Model configuration
    model_path = "./results"  # Path to fine-tuned model
    model_name = "nl2sparql"
    
    # Convert and build model in Ollama
    converter = OllamaModelConverter(model_path)
    success = converter.build_ollama_model(model_name)
    
    if not success:
        print("Failed to build Ollama model")
        return
    
    # Create service
    service = SPARQLQueryService(model_name)
    
    # Test the model
    service.test_model()
    
    # Create web interface
    web_interface = WebInterface(service)
    gradio_app = web_interface.create_gradio_interface()
    
    if gradio_app:
        print("\nStarting web interface...")
        gradio_app.launch(server_name="0.0.0.0", server_port=7860)
    
    # Create API service
    api_service = FastAPIService(service)
    fastapi_app = api_service.create_api()
    
    if fastapi_app:
        print("\nTo start API service, run:")
        print("uvicorn ollama_integration:app --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    main()