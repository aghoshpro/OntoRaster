from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import TomlLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import re

def validate_sparql_query(query):
    """Basic validation of SPARQL query structure"""
    # Check for basic SPARQL components
    has_prefix = bool(re.search(r'PREFIX\s+\w+:', query, re.IGNORECASE))
    has_select = bool(re.search(r'SELECT\s+', query, re.IGNORECASE))
    has_where = bool(re.search(r'WHERE\s*{', query, re.IGNORECASE))
    
    return all([has_prefix, has_select, has_where])

def format_sparql_query(query):
    """Format and clean up the SPARQL query"""
    # Remove any markdown code block indicators
    query = re.sub(r'```sparql|```', '', query)
    # Remove extra whitespace
    query = ' '.join(query.split())
    return query.strip()

persist_directory = 'chroma/chroma3/'
embeddings = OllamaEmbeddings(model="mxbai-embed-large")
LLM = ChatOllama(model="llama3.2", temperature=0.2)  # Lower temperature for more consistent output

loader = TomlLoader('OntoRaster.toml')
docs = loader.load()

all_page_text = [p.page_content for p in docs]
joined_page_text = " ".join(all_page_text)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
splits = text_splitter.split_text(joined_page_text)

vectordb = Chroma.from_texts(
    texts=splits,
    embedding=embeddings,
    persist_directory=persist_directory,
    collection_name="ontorasterX3"
)

# Enhanced prompt template for better SPARQL generation
template = """You are a SPARQL query expert. Your task is to convert natural language questions into valid SPARQL queries.

Context information about the ontology and data structure:
{context}

Question: {question}

Requirements for the SPARQL query:
1. Always include necessary PREFIX declarations
2. Use proper SPARQL syntax and structure
3. Include appropriate FILTER conditions when needed
4. Use proper variable naming (e.g., ?x, ?y)
5. Include proper WHERE clause with graph patterns
6. Make the query as efficient as possible

Generate a valid SPARQL query that answers the question. If you're unsure about any part of the query, explain your uncertainty.
SPARQL Query:"""

QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)

qa_chain = RetrievalQA.from_chain_type(
    LLM,
    retriever=vectordb.as_retriever(search_kwargs={"k": 5}),  # Increased context retrieval
    return_source_documents=True,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

def generate_sparql(question):
    """Generate and validate SPARQL query from natural language question"""
    try:
        result = qa_chain.invoke({"query": question})
        generated_query = result["result"]
        
        # Format the query
        formatted_query = format_sparql_query(generated_query)
        
        # Validate the query
        if validate_sparql_query(formatted_query):
            print("Generated SPARQL Query:")
            print(formatted_query)
            print("\nSource documents used:")
            for doc in result["source_documents"]:
                print(f"- {doc.page_content[:200]}...")
        else:
            print("Warning: Generated query may not be valid SPARQL. Please review:")
            print(formatted_query)
            
    except Exception as e:
        print(f"Error generating SPARQL query: {str(e)}")

# Example usage
question = "Find all subdistricts of Munich where elevation is more than 480 meters"
generate_sparql(question)

# Now you can use the function with any natural language question
# generate_sparql("your natural language question here")