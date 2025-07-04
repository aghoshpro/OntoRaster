import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Apply Seaborn style
sns.set(style="whitegrid", font_scale=1.2)

# Group DataFrames
group1 = [df1, df2]
group2 = [df3, df4]

# Function to compute mean and std by Points
def aggregate_group(group):
    combined = pd.concat(group)
    grouped = combined.groupby("Points")["Processing_Time"]
    mean = grouped.mean()
    std = grouped.std()
    min_ = grouped.min()
    max_ = grouped.max()
    return mean.index, mean.values, std.values, min_.values, max_.values

# Aggregate
x1, y1, std1, min1, max1 = aggregate_group(group1)
x2, y2, std2, min2, max2 = aggregate_group(group2)

# Plot
plt.figure(figsize=(12, 6))

# Group 1: Red line with shaded std
plt.plot(x1, y1, color='red', label='Group 1: [df1, df2]', linewidth=2)
plt.fill_between(x1, y1 - std1, y1 + std1, color='red', alpha=0.2)

# Group 2: Blue line with shaded std
plt.plot(x2, y2, color='blue', label='Group 2: [df3, df4]', linewidth=2)
plt.fill_between(x2, y2 - std2, y2 + std2, color='blue', alpha=0.2)

# Custom xticks
xtick_step = 1000  # Change this based on your Points spacing
xticks = np.arange(min(x1.min(), x2.min()), max(x1.max(), x2.max()) + 1, xtick_step)
plt.xticks(xticks, rotation=45)

# Labels and Legend
plt.xlabel('Points', fontsize=14, fontweight='bold')
plt.ylabel('Processing Time', fontsize=14, fontweight='bold')
plt.title('Processing Time Comparison by Groups with Variability', fontsize=16, fontweight='bold')
plt.legend(loc='upper left', fontsize=12)
plt.tight_layout()
plt.grid(True, linestyle='--', alpha=0.6)

plt.show()
