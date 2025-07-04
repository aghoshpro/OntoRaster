# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np
# from typing import List, Tuple

# def get_global_min_max(dfs: List[pd.DataFrame]) -> Tuple[float, float]:
#     """Calculate global min and max from the 'value' column across multiple DataFrames."""
#     all_values = pd.concat([df['Processing_Time'] for df in dfs], ignore_index=True)
#     return all_values.min(), all_values.max()

# XTICKS_BIN = 500
# STEPS = 100

# bm1 = pd.read_csv('./benchmark_scripts/paper/fig1/ELVx_10000points_5km_uf5.csv')
# bm2 = pd.read_csv('./benchmark_scripts/paper/fig1/ELVx_10000points_25km_uf5.csv')
# bm3 = pd.read_csv('./benchmark_scripts/paper/fig1/ELVx_10000points_50km_uf5.csv')
# bm4 = pd.read_csv('./benchmark_scripts/paper/fig1/ELVx_10000points_100km_uf5.csv')
# bm5 = pd.read_csv('./benchmark_scripts/paper/fig1/ELVx_10000points_250km_uf5.csv')
# bm6 = pd.read_csv('./benchmark_scripts/paper/fig1/ELV_10000points_500km_uf5.csv')

# # bm7 = pd.read_csv('./benchmark_scripts/paper/fig2/Temperature_10000points_5km_uf5_1hole.csv')
# # bm8 = pd.read_csv('./benchmark_scripts/paper/fig2/Temperature_10000points_25km_uf5_1hole.csv')
# # bm9 = pd.read_csv('./benchmark_scripts/paper/fig2/Temperature_10000points_50km_uf5_1hole.csv')
# # bm10 = pd.read_csv('./benchmark_scripts/paper/fig2/Temperature_10000points_100km_uf5_1hole.csv')
# # bm11 = pd.read_csv('./benchmark_scripts/paper/fig2/Temperature_10000points_250km_uf5_1hole.csv')
# # bm12 = pd.read_csv('./benchmark_scripts/paper/fig2/Temperature_10000points_500km_uf5_1hole.csv')



# #y_min = np.min(np.array[np.array([bm500['Processing_Time'].min, bm1['Processing_Time'].min, bm11['Processing_Time'].min, bm111['Processing_Time'].min, bm1111['Processing_Time'].min, bm11111['Processing_Time'].min])])
# # y_max = max(bm500['Processing_Time'].max, bm1['Processing_Time'].max, bm11['Processing_Time'].max, bm111['Processing_Time'].max, bm1111['Processing_Time'].max, bm11111['Processing_Time'].max)

# # List of all dataframes you want to plot
# # dataframes = [bm1, bm2, bm3, bm4, bm5, bm6] #, bm500_2, bm12, bm112, bm1112, bm11112, bm111112, bm500_5, bm15, bm115, bm1115, bm11115, bm111115] #, bm500_2, bm12, bm112, bm1112, bm11112, bm111112, bm500_3, bm13, bm113, bm1113, bm11113, bm111113, bm500_4, bm14, bm114, bm1114, bm11114, bm111114]
# # titles = ['500 km² (R1)', '250 km² (R1)', '100 km² (R1)', '50 km² (R1)', '25 km² (R1)', '5 km² (R1)', '500 km² (R2)', '250 km² (R2)', '100 km² (R2)', '50 km² (R2)', '25 km² (R2)', '5 km² (R2)', '500 km² (R3)', '250 km² (R3)', '100 km² (R3)', '50 km² (R3)', '25 km² (R3)', '5 km² (R3)', '500 km² (R4)', '250 km² (R4)', '100 km² (R4)', '50 km² (R4)', '25 km² (R4)', '5 km² (R4)']

# dataframes = [bm1, bm2, bm3, bm4, bm5, bm6]
# # dataframes = [bm7, bm8, bm9, bm10, bm11, bm12]
# titles = ['5 km² (R2)', '20 km² (R2)', '50 km² (R2)', '100 km² (R2)', '250 km² (R2)', '500 km² (R2)']#, '500 km² (R3)', '250 km² (R3)', '100 km² (R3)', '50 km² (R3)', '25 km² (R3)', '5 km² (R3)', '500 km² (R4)', '250 km² (R4)', '100 km² (R4)', '50 km² (R4)', '25 km² (R4)', '5 km² (R4)']


# ymin = min(df['Processing_Time'].min() for df in dataframes)
# ymax = max(df['Processing_Time'].max() for df in dataframes)

# # ymin, ymax = get_global_min_max(dataframes)

# # Calculate the grid dimensions
# # n = len(dataframes)
# # cols = 6
# # rows = int(np.ceil(n / cols))

# n = len(dataframes)
# cols = int(np.ceil(np.sqrt(n)))
# rows = int(np.ceil(n / cols))

# # Create figure and subplots
# fig, axes = plt.subplots(rows, cols, figsize=(20, 10))
# axes = axes.flatten()  # Flatten to easily iterate through axes

# # Plot each dataframe as a bar plot in its respective subplot
# for i, (df, title) in enumerate(zip(dataframes, titles)):
#     if i < len(axes):  # Make sure we don't exceed the number of available subplots
#         colors = ['green' if t == df['Processing_Time'].min() else 'red' if t == df['Processing_Time'].max() else 'deepskyblue' for t in df['Processing_Time']]
#         # df.plot(kind='bar', ax=axes[i])
#         # axes[i].bar(df['Points'], df['Processing_Time'], color=colors, alpha=0.7)
#         axes[i].bar(df['Points'], df['Processing_Time'],color=colors, alpha=0.7,  width=STEPS)
#         axes[i].set_title(title, fontsize=15, fontweight='bold')
#         axes[i].set_xticks(range(df['Points'].min(), df['Points'].max() + 1, XTICKS_BIN), fontsize=15, fontweight='bold', rotation = 45)
#         # axes[i].set_yticks(df['Processing_Time'], fontsize=15)
#         axes[i].set_yticks(np.arange(df['Processing_Time'].min(), df['Processing_Time'].max(), 1),  fontsize=15, fontweight='bold')
#         # axes[i].set_xlabel('Points', fontsize=15, fontweight='bold')
#         # axes[i].set_ylabel('Time (seconds)', fontsize=15, fontweight='bold')
#         # axes[i].legend(loc='upper right')
#         # axes[i].grid(True, axis='y', linestyle='--', alpha=0.7)
#         axes[i].margins(x=0)
#         # axes[i].set_ylim(ymin, ymax)
#         # axes[i].set_xlim(3, 5003)
#         # axes[i].set_yscale('log')
# # Hide any empty subplots
# for j in range(i + 1, len(axes)):
#     axes[j].set_visible(False)

# # plt.tight_layout(rect=[0, 0, 0, 0]) 
# plt.tight_layout(rect=[0.0, 0.03, 0.98, 0.922])  # Adjust bottom, left, right, top
# fig.suptitle('Polygon vs Raster R2: Temp (1000m) (SPATIAL and TEMPORAL)', fontsize=20, fontweight='bold')
# # fig.suptitle('Polygon vs Raster R1: DEM (30m) | R2: TEMP (1km) | R3: NDVI (250m) | R4: Snow (500m)', fontsize=20, fontweight='bold')


# # del fig
# # del axes

# # y_min_log = min(min(np.log10(df['Processing_Time'])) for df in dataframes)
# # y_max_log = max(max(np.log10(df['Processing_Time'])) for df in dataframes)


# # fig, axes = plt.subplots(rows, cols, figsize=(20, 10))
# # axes = axes.flatten()  # Flatten to easily iterate through axes

# # # Plot each dataframe as a bar plot in its respective subplot
# # for i, (df, title) in enumerate(zip(dataframes, titles)):
# #     if i < len(axes):  # Make sure we don't exceed the number of available subplots
# #         # Log-transform the y-values
# #         log_y = np.log10(df['Processing_Time'])
# #         x = df['Points']
# #         m, b = np.polyfit(x, log_y, 1)
# #         trend_log_y = m * x + b
# #         trend_y = 10 ** trend_log_y  

# #         colors = ['green' if t == df['Processing_Time'].min() else 'red' if t == df['Processing_Time'].max() else 'deepskyblue' for t in df['Processing_Time']]
# #         axes[i].bar(x, trend_y,color=colors, alpha=0.7,  width=STEPS)
# #         axes[i].set_title(title, fontsize=15, fontweight='bold')
# #         axes[i].set_xticks(range(df['Points'].min(), df['Points'].max() + 1, XTICKS_BIN), fontsize=15, fontweight='bold', rotation = 35)
# #         axes[i].set_yticks(np.arange(np.min(trend_y), np. max(trend_y), 0.5),  fontsize=15, fontweight='bold')
# #         # axes[i].set_xlabel('Points', fontsize=15, fontweight='bold')
# #         # axes[i].set_ylabel('Time (seconds)', fontsize=15, fontweight='bold')
# #         axes[i].grid(True, axis='y', linestyle='--', alpha=0.7)
# #         axes[i].margins(x=0)
# #         axes[i].set_xlim(3, 5003)
# #         axes[i].set_ylim(0.0, 5.0)
# #         # print(y_min_log, y_max_log)
# # # Hide any empty subplots
# # for j in range(i + 1, len(axes)):
# #     axes[j].set_visible(False)

# # plt.tight_layout(rect=[0, 0, 0, 0.05])  # Adjust bottom, left, right, top
# # fig.suptitle('POLYGON ( 100 points | 0.9 uniformity)', fontsize=20, fontweight='bold')
# # plt.yscale('log')
# plt.show()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
import matplotlib.colors as mcolors

XTICKS_BIN = 1000
STEPS = 100


# bm1 = pd.read_csv('./benchmark_scripts/paper/fig1/TempX_10000points_5km_uf5.csv')
# bm2 = pd.read_csv('./benchmark_scripts/paper/fig1/TempX_10000points_25km_uf5.csv')
# bm3 = pd.read_csv('./benchmark_scripts/paper/fig1/Temp_10000points_50km_uf5.csv')
# bm4 = pd.read_csv('./benchmark_scripts/paper/fig1/Temp_10000points_100km_uf5.csv')
# bm5 = pd.read_csv('./benchmark_scripts/paper/fig1/Temp_10000points_250km_uf5.csv')
# bm6 = pd.read_csv('./benchmark_scripts/paper/fig1/Temp_10000points_500km_uf5.csv')


# Data
dataframes = [bm1, bm2, bm3, bm4, bm5, bm6] #, bmTempBav1, bmTempBav2, bmTempBav3, bmTempBav4, bmTempBav5, bmTempBav6, bmTempSwe1, bmTempSwe2, bmTempSwe3, bmTempSwe4, bmTempSwe5, bmTempSwe6]
titles = ['5 km² (R4)', '25 km² (R4)', '50 km² (R4)', '100 km² (R4)', '250 km² (R4)', '500 km² (R4)']#, '5 km² (R4) Bavaria', '25 km² (R4) Bavaria', '50 km² (R4) Bavaria', '100 km² (R4) Bavaria', '250 km² (R4) Bavaria', '500 km² (R4) Bavaria', '5 km² (R4) Sweden', '25 km² (R4) Sweden', '50 km² (R4) Sweden', '100 km² (R4) Sweden', '250 km² (R4) Sweden', '500 km² (R4) Sweden']

# Axis scaling
ymin = min(df['Processing_Time'].min() for df in dataframes)
ymax = max(df['Processing_Time'].max() for df in dataframes)

print(ymin)
print(ymax)
# Grid dimensions
# n = len(dataframes)
# cols = int(np.ceil(np.sqrt(n)))
# rows = int(np.ceil(n / cols))

n = len(dataframes)
cols = 6
rows = int(np.ceil(n / cols))


# Create figure
fig, axes = plt.subplots(rows, cols, figsize=(22, 12))
axes = axes.flatten()

# Normalize across all dataframes for a consistent color map
norm = mcolors.Normalize(vmin=ymin, vmax=ymax)
cmap = cm.Spectral_r # BuPu, YlGnBu, viridis_r, YlOrRd, RdYlBu_r

for i, (df, title) in enumerate(zip(dataframes, titles)):
    if i < len(axes):
        df_sorted = df.sort_values("Points")
        colors = cmap(norm(df_sorted["Processing_Time"]))

        # Bar plot with gradient color
        axes[i].bar(df_sorted["Points"], df_sorted["Processing_Time"], 
                    color=colors, alpha=0.9, width=STEPS)

        # Labels and titles
        axes[i].set_title(title, fontsize=20, fontweight='bold')
        axes[i].set_ylim(ymin, ymax)
        axes[i].margins(x=0)
        axes[i].tick_params(axis='x', rotation=45)
        axes[i].set_xlabel('Points', fontsize=15, fontweight='bold')
        axes[i].set_ylabel('Time (s)', fontsize=15, fontweight='bold')
        # Optional: Custom xticks if needed
        axes[i].set_xticks(range(df_sorted["Points"].min(), df_sorted["Points"].max() + 1, XTICKS_BIN))
        axes[i].tick_params(labelsize=16)

# Hide unused subplots
for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)

# Add a shared horizontal colorbar below
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
# Custom axes for the colorbar: [left, bottom, width, height]
cbar_ax = fig.add_axes([0.25, 0.08, 0.5, 0.02]) 
cbar = fig.colorbar(sm, cax=cbar_ax, orientation='horizontal', fraction=0.05, pad=0.1)
cbar.set_label('Time (s)', fontsize=15, fontweight='bold')
cbar.ax.tick_params(labelsize=25)


# Global title and layout
# fig.supylabel('Munich (urban) vs Bavaria (state) vs Sweden (country)', fontsize=15, fontweight='bold')
fig.suptitle('Polygon vs Raster Data R4 (1000m x 1000m) ', fontsize=25, fontweight='bold')
plt.tight_layout(rect=[0, 0.1, 1, 0.42])   # Adjust left, bottom right, top
plt.savefig('./benchmark_scripts/paper/fig1/figR4_200dpi_AOI.png', dpi=200)
plt.show()