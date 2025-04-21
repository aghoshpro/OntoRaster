from SPARQLWrapper import SPARQLWrapper, JSON
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import numpy as np
import threading

# Initialize SPARQLWrapper
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

# Create global variables for animation
fig, ax = plt.figure(figsize=(12, 7)), plt.subplot(111)
limit_values = list(range(10, 110, 10))  # 10, 20, 30, ... 100
processing_times = []
benchmark_data = []
is_running = False
current_index = 0
bars = None

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
    sparql.setReturnFormat(JSON)
    
    # Measure the query execution time
    start_time = time.time()
    results = sparql.query()
    end_time = time.time()
    
    # Calculate the processing time
    processing_time = end_time - start_time
    
    return processing_time

def init_animation():
    """Initialize the animation with empty bars."""
    ax.set_xlim(-0.5, len(limit_values) - 0.5)
    ax.set_ylim(0, 0.1)  # Will auto-adjust as data comes in
    ax.set_title('SPARQL Query Performance Benchmark (Live)', fontsize=14)
    ax.set_xlabel('LIMIT Value', fontsize=12)
    ax.set_ylabel('Processing Time (seconds)', fontsize=12)
    ax.set_xticks(range(len(limit_values)))
    ax.set_xticklabels(limit_values)
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Create empty bars
    empty_bars = ax.bar(range(len(limit_values)), 
                        [0] * len(limit_values),
                        color='skyblue', 
                        edgecolor='navy',
                        alpha=0.8)
    
    return empty_bars

def run_benchmark_async():
    """Run the benchmark in a separate thread to avoid blocking the UI."""
    global is_running, current_index
    is_running = True
    
    while current_index < len(limit_values) and is_running:
        limit = limit_values[current_index]
        try:
            time_taken = benchmark(limit)
            processing_times.append(time_taken)
            benchmark_data.append({'LIMIT': limit, 'Processing_Time': time_taken})
            print(f"LIMIT {limit}: {time_taken:.4f} seconds")
            current_index += 1
        except Exception as e:
            print(f"Error with LIMIT {limit}: {e}")
            processing_times.append(0)  # Add zero for failed queries
            current_index += 1
    
    # Save results when done
    if current_index >= len(limit_values):
        df = pd.DataFrame(benchmark_data)
        df.to_csv('sparql_benchmark_results.csv', index=False)
        plt.savefig('sparql_benchmark.png')
        print("Benchmark completed and saved to CSV and PNG files.")
    
    is_running = False

def animate(i):
    """Update the bar heights for each frame."""
    if not processing_times:
        return ax.bar(range(len(limit_values)), [0] * len(limit_values))
    
    # Fill in the data we have, leave the rest as zeros
    y_data = processing_times + [0] * (len(limit_values) - len(processing_times))
    
    # Update the bars
    bars = ax.bar(range(len(limit_values)), 
                  y_data, 
                  color='skyblue', 
                  edgecolor='navy',
                  alpha=0.8)
    
    # Color the current bar differently
    if current_index < len(limit_values) and current_index > 0:
        bars[current_index-1].set_color('orange')
        bars[current_index-1].set_edgecolor('darkred')
    
    # Add value labels above each bar
    for j, bar in enumerate(bars):
        if j < len(processing_times):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., 
                    height + 0.002,
                    f'{processing_times[j]:.3f}s', 
                    ha='center', va='bottom', 
                    rotation=0,
                    fontsize=9)
    
    # Adjust y-axis limit if needed
    if processing_times:
        max_y = max(processing_times) * 1.2  # Add 20% margin
        ax.set_ylim(0, max(0.1, max_y))
    
    return bars

def start_benchmark(event):
    """Start the benchmark when the button is clicked."""
    global current_index
    if not is_running:
        # Clear previous data if needed
        if processing_times:
            processing_times.clear()
            benchmark_data.clear()
            current_index = 0
            ax.texts.clear()  # Clear text annotations
        
        # Start the benchmark in a separate thread
        threading.Thread(target=run_benchmark_async).start()

def stop_benchmark(event):
    """Stop the benchmark when the button is clicked."""
    global is_running
    is_running = False
    print("Benchmark stopped.")

# Setup the figure with buttons
plt.subplots_adjust(bottom=0.2)
ax_start = plt.axes([0.7, 0.05, 0.1, 0.075])
ax_stop = plt.axes([0.81, 0.05, 0.1, 0.075])
btn_start = Button(ax_start, 'Start')
btn_stop = Button(ax_stop, 'Stop')
btn_start.on_clicked(start_benchmark)
btn_stop.on_clicked(stop_benchmark)

# Create the animation
ani = animation.FuncAnimation(
    fig, animate, init_func=init_animation, 
    frames=200, interval=500, blit=False
)

# Display the plot
# plt.title("SPARQL Query Performance Benchmark", fontsize=16, pad=20)
plt.tight_layout(rect=[0, 0.1, 1, 0.95])  # Adjust layout to make room for title
plt.show()

# If you're running this in a script, you might need to keep the main thread alive
try:
    plt.pause(3600)  # Keep the plot open for an hour max
except:
    pass