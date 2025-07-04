import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
import matplotlib.colors as mcolors

XTICKS_BIN = 1000
STEPS = 100
# plt.rcParams['figure.dpi']=100

bmEnv1 = pd.read_csv('./benchmark_scripts/paper/fig1/ELVx_10000points_5km_uf5.csv')
bmEnv2 = pd.read_csv('./benchmark_scripts/paper/fig1/ELVx_10000points_25km_uf5.csv')
bmEnv3 = pd.read_csv('./benchmark_scripts/paper/fig1/ELVx_10000points_50km_uf5.csv')
bmEnv4 = pd.read_csv('./benchmark_scripts/paper/fig1/ELVx_10000points_100km_uf5.csv')
bmEnv5 = pd.read_csv('./benchmark_scripts/paper/fig1/ELV_10000points_250km_uf5.csv')
bmEnv6 = pd.read_csv('./benchmark_scripts/paper/fig1/ELV_10000points_500km_uf5.csv')

bmSnow1 = pd.read_csv('./benchmark_scripts/paper/fig1/Snow_10000points_5km_uf5.csv')
bmSnow2 = pd.read_csv('./benchmark_scripts/paper/fig1/Snow_10000points_25km_uf5.csv')
bmSnow3 = pd.read_csv('./benchmark_scripts/paper/fig1/Snow_10000points_50km_uf5.csv')
bmSnow4 = pd.read_csv('./benchmark_scripts/paper/fig1/Snow_10000points_100km_uf5.csv')
bmSnow5 = pd.read_csv('./benchmark_scripts/paper/fig1/Snow_10000points_250km_uf5.csv')
bmSnow6 = pd.read_csv('./benchmark_scripts/paper/fig1/Snow_10000points_500km_uf5.csv')

bmNdvi1 = pd.read_csv('./benchmark_scripts/paper/fig1/NDVI_10000points_5km_uf5.csv')
bmNdvi2 = pd.read_csv('./benchmark_scripts/paper/fig1/NDVI_10000points_25km_uf5.csv')
bmNdvi3 = pd.read_csv('./benchmark_scripts/paper/fig1/NDVI_10000points_50km_uf5.csv')
bmNdvi4 = pd.read_csv('./benchmark_scripts/paper/fig1/NDVI_10000points_100km_uf5.csv')
bmNdvi5 = pd.read_csv('./benchmark_scripts/paper/fig1/NDVI_10000points_250km_uf5.csv')
bmNdvi6 = pd.read_csv('./benchmark_scripts/paper/fig1/NDVI_10000points_500km_uf5.csv')

bmTemp1 = pd.read_csv('./benchmark_scripts/paper/fig1/TempX_10000points_5km_uf5.csv')
bmTemp2 = pd.read_csv('./benchmark_scripts/paper/fig1/TempX_10000points_25km_uf5.csv')
bmTemp3 = pd.read_csv('./benchmark_scripts/paper/fig1/Temp_10000points_50km_uf5.csv')
bmTemp4 = pd.read_csv('./benchmark_scripts/paper/fig1/Temp_10000points_100km_uf5.csv')
bmTemp5 = pd.read_csv('./benchmark_scripts/paper/fig1/Temp_10000points_250km_uf5.csv')
bmTemp6 = pd.read_csv('./benchmark_scripts/paper/fig1/Temp_10000points_500km_uf5.csv')

# Data
dataframes = [bmEnv1, bmEnv2, bmEnv3, bmEnv4, bmEnv5, bmEnv6, bmSnow1, bmSnow2, bmSnow3, bmSnow4, bmSnow5, bmSnow6, bmNdvi1, bmNdvi2, bmNdvi3, bmNdvi4, bmNdvi5, bmNdvi6, bmTemp1, bmTemp2, bmTemp3, bmTemp4, bmTemp5, bmTemp6]
# titles = ['5 km² (R1)', '25 km² (R1)', '50 km² (R1)', '100 km² (R1)', '250 km² (R1)', '500 km² (R1)', '5 km² (R2)', '25 km² (R2)', '50 km² (R2)', '100 km² (R2)', '250 km² (R2)', '500 km² (R2)', '5 km² (R3)', '25 km² (R3)', '50 km² (R3)', '100 km² (R3)', '250 km² (R3)', '500 km² (R3)', '5 km² (R4)', '25 km² (R4)', '50 km² (R4)', '100 km² (R4)', '250 km² (R4)', '500 km² (R4)']   

# Axis scaling
ymin = min(df['Processing_Time'].min() for df in dataframes)
ymax = max(df['Processing_Time'].max() for df in dataframes)

# Grid dimensions
# n = len(dataframes)
# cols = int(np.ceil(np.sqrt(n)))
# rows = int(np.ceil(n / cols))

# n = len(dataframes)
# cols = 6
# rows = int(np.ceil(n / cols))

# # Create figure
# fig, axes = plt.subplots(rows, cols, figsize=(22, 12))
# axes = axes.flatten()

# # Normalize across all dataframes for a consistent color map
# norm = mcolors.Normalize(vmin=ymin, vmax=ymax)
# cmap = cm.Spectral_r # BuPu, YlGnBu, viridis_r, YlOrRd, RdYlBu_r

# for i, (df, title) in enumerate(zip(dataframes, titles)):
#     if i < len(axes):
#         df_sorted = df.sort_values("Points")
#         colors = cmap(norm(df_sorted["Processing_Time"]))

#         # Bar plot with gradient color
#         axes[i].bar(df_sorted["Points"], df_sorted["Processing_Time"], 
#                     color=colors, alpha=0.9, width=STEPS)

#         # Labels and titles
#         axes[i].set_title(title, fontsize=21, fontweight='bold')
#         axes[i].set_ylim(ymin, ymax)
#         axes[i].margins(x=0)
#         axes[i].tick_params(axis='x', rotation=45)
#         # axes[i].set_xlabel('Points', fontsize=13, fontweight='bold')
#         # axes[i].set_ylabel('Time (s)', fontsize=13, fontweight='bold')
#         # Optional: Custom xticks if needed
#         axes[i].set_xticks(range(df_sorted["Points"].min(), df_sorted["Points"].max() + 1, XTICKS_BIN))
#         axes[i].tick_params(labelsize=16)

# # Hide unused subplots
# for j in range(i + 1, len(axes)):
#     axes[j].set_visible(False)

# # Add a shared horizontal colorbar below
# sm = cm.ScalarMappable(cmap=cmap, norm=norm)
# sm.set_array([])
# # Custom axes for the colorbar: [left, bottom, width, height]
# cbar_ax = fig.add_axes([0.25, 0.05, 0.5, 0.02]) 
# cbar = fig.colorbar(sm, cax=cbar_ax, orientation='horizontal', fraction=0.05, pad=0.1)
# cbar.set_label('Time (s)', fontsize=15, fontweight='bold')
# cbar.ax.tick_params(labelsize=20)


# # Global title and layout
# # fig.suptitle('Polygon vs Raster R2: Temp (1000m) (SPATIAL and TEMPORAL)', fontsize=25, fontweight='bold')
# plt.tight_layout(rect=[0, 0.06, 1, 0.99])   # Adjust bottom, left, right, top
# plt.savefig('./benchmark_scripts/paper/fig1/fig2_200dpi.png', dpi=200)
# plt.show()

group1 = [bmEnv1, bmEnv2,bmEnv3,bmEnv4,bmEnv5,bmEnv6]
group2 = [bmSnow1,bmSnow2,bmSnow3,bmSnow4,bmSnow5,bmSnow6]
group3 = [bmNdvi1, bmNdvi2, bmNdvi3, bmNdvi4, bmNdvi5, bmNdvi6]
group4 = [bmTemp1, bmTemp2, bmTemp3, bmTemp4, bmTemp5, bmTemp6] 

# # Function to aggregate (e.g., mean) by 'Points'
# def average_group(group):
#     combined = pd.concat(group)
#     return combined.groupby('Points', as_index=False)['Processing_Time'].mean()

# # Calculate mean for each group
# avg1 = average_group(group1)
# avg2 = average_group(group2)
# avg3 = average_group(group3)
# avg4 = average_group(group4)

# # Plotting
# plt.figure(figsize=(12, 6))

# # Group 1 - Red line
# plt.plot(avg1['Points'], avg1['Processing_Time'], color='red', label='DEM (30m X 30m)', linewidth=2)

# # Group 2 - Blue line
# plt.plot(avg2['Points'], avg2['Processing_Time'], color='blue', label='Snow (500m X 500m)', linewidth=2)

# # Group 3 - Green line
# plt.plot(avg3['Points'], avg3['Processing_Time'], color='green', label='NDVI (250m X 250m)', linewidth=2)

# # Group 4 - Orange line
# plt.plot(avg4['Points'], avg4['Processing_Time'], color='orange', label='Temperature (1000m X 1000m)', linewidth=2)


# # Enhancements
# plt.xlabel('Points', fontsize=14, fontweight='bold')
# plt.ylabel('Processing Time', fontsize=14, fontweight='bold')
# plt.title('Processing Time Comparison by Groups', fontsize=16, fontweight='bold')
# plt.xticks(rotation=45, fontsize=15, fontweight='bold')
# plt.grid(True, linestyle='--', alpha=0.6)
# plt.legend(loc='upper left', fontsize=12)
# plt.tight_layout()
# plt.show()

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
x3, y3, std3, min3, max3 = aggregate_group(group3)
x4, y4, std4, min4, max4 = aggregate_group(group4)

# Plot
plt.figure(figsize=(12, 6))

# Group 1: Red line with shaded std
plt.plot(x1, y1, color='red', label='DEM (30m X 30m)', linewidth=2, marker='o')
# plt.fill_between(x1, y1 - std1, y1 + std1, color='red', alpha=0.2)

# Group 3: Green line with shaded std
plt.plot(x3, y3, color='green', label='NDVI (250m X 250m)', linewidth=2, marker='s')
# plt.fill_between(x3, y3 - std3, y3 + std3, color='green', alpha=0.2)

# Group 2: Blue line with shaded std
plt.plot(x2, y2, color='blue', label='Snow (500m X 500m)', linewidth=2, marker='d')
# plt.fill_between(x2, y2 - std2, y2 + std2, color='blue', alpha=0.2)

# Group 4: Orange line with shaded std
plt.plot(x4, y4, color='orange', label='Temperature (1000m X 1000m)', linewidth=2, marker='^')
# plt.fill_between(x4, y4 - std4, y4 + std4, color='orange', alpha=0.2)

# Custom xticks
xtick_step = 1000  # Change this based on your Points spacing
xticks = np.arange(min(x1.min(), x2.min()), max(x1.max(), x2.max()) + 1, xtick_step)
plt.xticks(xticks, rotation=45, fontsize=16, fontweight='bold')
plt.yticks(fontsize=16, fontweight='bold')
# Labels and Legend
plt.xlabel('Points', fontsize=17, fontweight='bold')
plt.ylabel('Time (s)', fontsize=17, fontweight='bold')
plt.title('Aggregated Time vs Different Raster Resolutions', fontsize=25, fontweight='bold')
plt.legend(loc='upper left', fontsize=17)
plt.tight_layout()
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('./benchmark_scripts/paper/fig1/fig4_200dpi.png', dpi=200)
plt.show()
