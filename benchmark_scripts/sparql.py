from SPARQLWrapper import SPARQLWrapper, JSON, CSV, POST
import time
import pandas as pd
import matplotlib.pyplot as plt

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

def benchmark(limit):
    """
    Records the query processing time for a SPARQL query with different LIMIT values.
    
    Args:
        limit: The LIMIT value for the SPARQL query
        
    Returns:
        float: The time taken to execute the query in seconds
    """
    # Set the query with proper limit value substitution
    query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX sdo: <https://schema.org/>

        CONSTRUCT {{
        ?lang a sdo:Language ;
        sdo:alternateName ?iso6391Code .
        }}
        WHERE {{
        ?lang a dbo:Language ;
        dbo:iso6391Code ?iso6391Code .
        FILTER (STRLEN(?iso6391Code)=2) # to filter out non-valid values
        }}
        LIMIT {limit}
    """
    
    sparql.setQuery(query)
    sparql.setMethod(POST)
    sparql.setReturnFormat(JSON)
    
    # Measure the query execution time
    start_time = time.time()
    results = sparql.query()
    end_time = time.time()
    
    # Calculate the processing time
    processing_time = end_time - start_time
    
    return processing_time

# Create a list to store benchmark results
benchmark_data = []

# Run benchmarks with increasing LIMIT values
limit_values = list(range(10, 110, 10))  # 10, 20, 30, ... 100

for limit in limit_values:
    try:
        time_taken = benchmark(limit)
        benchmark_data.append({'x': limit, 'Processing_Time': time_taken})
        print(f"x {limit}: {time_taken:.4f} seconds")
    except Exception as e:
        print(f"Error with x {limit}: {e}")

# Create a pandas DataFrame from the benchmark data
df = pd.DataFrame(benchmark_data)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(df['x'], df['Processing_Time'], marker='o', linestyle='-')
plt.title('SPARQL Query Performance Benchmark')
plt.xlabel('x Value')
plt.ylabel('Processing Time (seconds)')
plt.grid(True)
plt.savefig('./benchmark_scripts/sparql_benchmark.png')
plt.show()

# Save the benchmark data to a CSV file
df.to_csv('./benchmark_scripts/sparql_benchmark_results.csv', index=False)
print("Benchmark completed and saved to CSV and PNG files.")

# def benchmark():
#     """
#     Records the query processing time for a SPARQL query with different LIMIT values.
    
#     Args:
#         limit: The LIMIT value for the SPARQL query
        
#     Returns:
#         float: The time taken to execute the query in seconds
#     """
#     # Set the query with proper limit value substitution
#     query = f"""
#         PREFIX dbo: <http://dbpedia.org/ontology/>
#         PREFIX sdo: <https://schema.org/>

#         CONSTRUCT {{
#         ?lang a sdo:Language ;
#         sdo:alternateName ?iso6391Code .
#         }}
#         WHERE {{
#         ?lang a dbo:Language ;
#         dbo:iso6391Code ?iso6391Code .
#         FILTER (STRLEN(?iso6391Code)=2) # to filter out non-valid values
#         }}
#     """
    
#     sparql.setQuery(query)
#     sparql.setReturnFormat(JSON)
    
#     # Measure the query execution time
#     start_time = time.time()
#     results = sparql.query()
#     end_time = time.time()
    
#     # Calculate the processing time
#     processing_time = end_time - start_time
    
#     return processing_time


# time_taken = benchmark()
# print(time_taken)

