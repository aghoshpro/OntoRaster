# Natural Language to SPARQL Fine-tuning Pipeline

## Complete Step-by-Step Guide

### Prerequisites

1. **Hardware Requirements:**
   - GPU with at least 8GB VRAM (recommended: RTX 3080/4080 or better)
   - 32GB+ RAM
   - 50GB+ free disk space

2. **Software Requirements:**
   - Python 3.8+
   - CUDA 11.8+ (for GPU acceleration)
   - Git

### Step 1: Environment Setup

```bash
# Clone/create project directory
mkdir nl2sparql-pipeline
cd nl2sparql-pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Install Ollama (for model serving)
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 2: Directory Structure Setup

```bash
# Create required directories
mkdir -p {ontologies,data,results,ollama_models}

# Project structure:
# nl2sparql-pipeline/
# ├── ontologies/          # Place your .owl, .ttl, .rdf files here
# ├── data/               # Training data and configurations
# ├── results/            # Fine-tuned model output
# ├── ollama_models/      # Ollama model files
# ├── nl2sparql_pipeline.py
# ├── data_preparation.py
# ├── ollama_integration.py
# └── requirements.txt
```

### Step 3: Prepare Your Data

1. **Add Ontology Files:**
   ```bash
   # Copy your ontology files to the ontologies directory
   cp /path/to/your/ontologies/*.owl ontologies/
   cp /path/to/your/ontologies/*.ttl ontologies/
   ```

2. **Create SPARQL Query Dataset:**
   ```bash
   # Create sample training data or use your existing queries
   python data_preparation.py
   ```

3. **Manual Training Data Creation (Optional):**
   Create `data/sparql_queries.json` with your domain-specific queries:
   ```json
   [
     {
       "natural_language": "Find all geographic features in Germany",
       "sparql": "PREFIX geo: <http://example.org/geo#>\nSELECT ?feature WHERE {\n  ?feature a geo:Feature .\n  ?feature geo:locatedIn <http://example.org/Germany> .\n}"
     }
   ]
   ```

### Step 4: Configure Training Parameters

Edit the `Config` class in `nl2sparql_pipeline.py`:

```python
@dataclass
class Config:
    # Model settings
    base_model: str = "meta-llama/Llama-3.2-3B"  # or "llama3.2:3b" for Ollama
    max_length: int = 2048
    
    # Training settings - adjust based on your hardware
    num_train_epochs: int = 3
    per_device_train_batch_size: int = 2  # Reduce if OOM
    learning_rate: float = 2e-4
    
    # LoRA settings for efficient fine-tuning
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.1
```

### Step 5: Run the Complete Pipeline

```bash
# Execute the main pipeline
python nl2sparql_pipeline.py
```

This will:
1. Load and process your ontologies
2. Generate/augment training data
3. Fine-tune the Llama model with LoRA
4. Save the fine-tuned model

### Step 6: Convert and Serve with Ollama

```bash
# Convert fine-tuned model to Ollama format
python ollama_integration.py

# Or manually:
# 1. Start Ollama service
ollama serve

# 2. Create custom model
ollama create nl2sparql -f ollama_models/nl2sparql.Modelfile

# 3. Test the model
ollama run nl2sparql "Find all cities in Germany"
```

### Step 7: Deploy Web Interface

```bash
# Option 1: Gradio Interface (included in ollama_integration.py)
python ollama_integration.py

# Option 2: FastAPI REST API
pip install fastapi uvicorn
uvicorn ollama_integration:app --host 0.0.0.0 --port 8000
```

## Advanced Configuration

### Custom Ontology Integration

To integrate your specific ontologies:

1. **Place ontology files** in the `ontologies/` directory
2. **Update namespace mappings** in the training data generation
3. **Add domain-specific prefixes** to SPARQL templates

Example ontology integration:
```python
# In data_preparation.py, modify the SPARQLTemplateGenerator
def _generate_domain_specific_patterns(self, graph: Graph) -> List[Dict]:
    """Generate patterns specific to your domain"""
    patterns = []
    
    # Example for GeoSPARQL
    if "geosparql" in str(graph.identifier):
        patterns.append({
            "natural_language": "Find geometries within 10km of Berlin",
            "sparql": """
            PREFIX geo: <http://www.opengis.net/ont/geosparql#>
            PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
            SELECT ?geom WHERE {
                ?berlin geo:hasGeometry ?berlinGeom .
                ?geom geo:hasGeometry ?geometry .
                FILTER(geof:distance(?berlinGeom, ?geometry, <http://www.opengis.net/def/uom/OGC/1.0/kilometre>) < 10)
            }
            """
        })
    
    return patterns
```

### Performance Optimization

For better performance:

1. **Reduce batch size** if encountering OOM errors
2. **Use gradient checkpointing** for memory efficiency
3. **Implement data streaming** for large datasets
4. **Use mixed precision training**

```python
# Add to TrainingArguments
training_args = TrainingArguments(
    # ... other args
    fp16=True,  # Enable mixed precision
    gradient_checkpointing=True,  # Save memory
    dataloader_pin_memory=False,  # Reduce memory usage
    per_device_train_batch_size=1,  # Reduce if needed
)
```

### Model Evaluation

Implement evaluation metrics:

```python
def evaluate_sparql_generation(model, test_data):
    """Evaluate model performance"""
    metrics = {
        "syntax_accuracy": 0,
        "semantic_accuracy": 0,
        "execution_success": 0
    }
    
    for item in test_data:
        generated = model.generate_sparql(item['question'])
        
        # Check syntax
        if validate_sparql_syntax(generated):
            metrics["syntax_accuracy"] += 1
        
        # Check semantic correctness (if ground truth available)
        if compare_query_results(generated, item['expected_sparql']):
            metrics["semantic_accuracy"] += 1
    
    return {k: v/len(test_data) for k, v in metrics.items()}
```

## Production Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "ollama_integration:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nl2sparql-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nl2sparql
  template:
    metadata:
      labels:
        app: nl2sparql
    spec:
      containers:
      - name: nl2sparql
        image: nl2sparql:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
```

## Troubleshooting

### Common Issues

1. **CUDA Out of Memory:**
   - Reduce batch size
   - Enable gradient checkpointing
   - Use smaller model variant

2. **Slow Training:**
   - Ensure GPU is being used
   - Check CUDA installation
   - Monitor GPU utilization

3. **Poor SPARQL Quality:**
   - Increase training data diversity
   - Add more domain-specific examples
   - Tune hyperparameters

4. **Ollama Integration Issues:**
   - Ensure Ollama service is running
   - Check model conversion process
   - Verify Modelfile syntax

### Monitoring and Logging

```python
import wandb  # Optional: for experiment tracking

# Initialize wandb (optional)
wandb.init(project="nl2sparql-finetuning")

# Add logging to training
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Monitor training progress
def log_training_metrics(epoch, loss, accuracy):
    logger.info(f"Epoch {epoch}: Loss={loss:.4f}, Accuracy={accuracy:.4f}")
    wandb.log({"epoch": epoch, "loss": loss, "accuracy": accuracy})
```

## Next Steps

1. **Expand Training Data:** Add more diverse SPARQL queries and natural language variations
2. **Domain Adaptation:** Fine-tune further on domain-specific data
3. **Multi-turn Conversations:** Extend to handle follow-up questions
4. **Query Optimization:** Add SPARQL query optimization capabilities
5. **Error Handling:** Implement robust error detection and correction

This pipeline provides a solid foundation for building production-ready Natural Language to SPARQL systems. Customize the components based on your specific ontologies and use cases.