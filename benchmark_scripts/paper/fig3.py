import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
import matplotlib.colors as mcolors

XTICKS_BIN = 1000
STEPS = 100
plt.rcParams['figure.dpi']=100

bmEnv1 = pd.read_csv('./benchmark_scripts/paper/fig2/ELV_10000points_5km_uf5_1hole.csv')
bmEnv2 = pd.read_csv('./benchmark_scripts/paper/fig2/ELV_10000points_25km_uf5_1hole.csv')
bmEnv3 = pd.read_csv('./benchmark_scripts/paper/fig2/ELV_10000points_50km_uf5_1hole.csv')
bmEnv4 = pd.read_csv('./benchmark_scripts/paper/fig2/ELV_10000points_100km_uf5_1hole.csv')
bmEnv5 = pd.read_csv('./benchmark_scripts/paper/fig2/ELV_10000points_250km_uf5_1hole.csv')
# bmEnv6 = pd.read_csv('./benchmark_scripts/paper/fig2/ELV_10000points_500km_uf5.csv')

bmSnow1 = pd.read_csv('./benchmark_scripts/paper/fig2/Snow_10000points_5km_uf5_1hole.csv')
bmSnow2 = pd.read_csv('./benchmark_scripts/paper/fig2/Snow_10000points_25km_uf5_1hole.csv')
bmSnow3 = pd.read_csv('./benchmark_scripts/paper/fig2/Snow_10000points_50km_uf5_1hole.csv')
bmSnow4 = pd.read_csv('./benchmark_scripts/paper/fig2/Snow_10000points_100km_uf5_1hole.csv')
bmSnow5 = pd.read_csv('./benchmark_scripts/paper/fig2/Snow_10000points_250km_uf5_1hole.csv')
bmSnow6 = pd.read_csv('./benchmark_scripts/paper/fig2/Snow_10000points_500km_uf5_1hole.csv')

# bmNdvi1 = pd.read_csv('./benchmark_scripts/paper/fig2/NDVI_10000points_5km_uf5_1hole.csv')
bmNdvi2 = pd.read_csv('./benchmark_scripts/paper/fig2/NDVI_10000points_25km_uf5_1hole.csv')
bmNdvi3 = pd.read_csv('./benchmark_scripts/paper/fig2/NDVI_10000points_50km_uf5_1hole.csv')
bmNdvi4 = pd.read_csv('./benchmark_scripts/paper/fig2/NDVI_10000points_100km_uf5_1hole.csv')
bmNdvi5 = pd.read_csv('./benchmark_scripts/paper/fig2/NDVI_10000points_250km_uf5_1hole.csv')
bmNdvi6 = pd.read_csv('./benchmark_scripts/paper/fig2/NDVI_10000points_500km_uf5_1hole.csv')

bmTemp1 = pd.read_csv('./benchmark_scripts/paper/fig2/Temp_10000points_5km_uf5_1hole.csv')
# bmTemp2 = pd.read_csv('./benchmark_scripts/paper/fig2/Temp_10000points_25km_uf5.csv')
# bmTemp3 = pd.read_csv('./benchmark_scripts/paper/fig2/Temp_10000points_50km_uf5.csv')
# bmTemp4 = pd.read_csv('./benchmark_scripts/paper/fig2/Temp_10000points_100km_uf5.csv')
# bmTemp5 = pd.read_csv('./benchmark_scripts/paper/fig2/Temp_10000points_250km_uf5.csv')
# bmTemp6 = pd.read_csv('./benchmark_scripts/paper/fig2/Temp_10000points_500km_uf5.csv')

# Data
# dataframes = [bmEnv1, bmEnv2, bmEnv3, bmEnv4, bmEnv5, bmEnv6, bmSnow1, bmSnow2, bmSnow3, bmSnow4, bmSnow5, bmSnow6, bmNdvi1, bmNdvi2, bmNdvi3, bmNdvi4, bmNdvi5, bmNdvi6, bmTemp1, bmTemp2, bmTemp3, bmTemp4, bmTemp5, bmTemp6]
dataframes = [bmEnv1, bmEnv2, bmEnv3, bmEnv4, bmEnv5, bmSnow1, bmSnow2, bmSnow3, bmSnow4, bmSnow5, bmSnow6, bmNdvi2, bmNdvi3, bmNdvi4, bmNdvi5, bmNdvi6, bmTemp1]
titles = ['5 km² (R1)', '25 km² (R1)', '50 km² (R1)', '100 km² (R1)', '250 km² (R1)', '500 km² (R1)', '5 km² (R2)', '25 km² (R2)', '50 km² (R2)', '100 km² (R2)', '250 km² (R2)', '500 km² (R2)', '5 km² (R3)', '25 km² (R3)', '50 km² (R3)', '100 km² (R3)', '250 km² (R3)', '500 km² (R3)', '5 km² (R4)', '25 km² (R4)', '50 km² (R4)', '100 km² (R4)', '250 km² (R4)', '500 km² (R4)']   

# Axis scaling
ymin = min(df['Processing_Time'].min() for df in dataframes)
ymax = max(df['Processing_Time'].max() for df in dataframes)

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
        axes[i].set_title(title, fontsize=15, fontweight='bold')
        axes[i].set_ylim(ymin, ymax)
        axes[i].margins(x=0)
        axes[i].tick_params(axis='x', rotation=45)
        # axes[i].set_xlabel('Points', fontsize=13, fontweight='bold')
        # axes[i].set_ylabel('Time (s)', fontsize=13, fontweight='bold')
        # Optional: Custom xticks if needed
        axes[i].set_xticks(range(df_sorted["Points"].min(), df_sorted["Points"].max() + 1, XTICKS_BIN))
        axes[i].tick_params(labelsize=18)

# Hide unused subplots
for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)

# Add a shared horizontal colorbar below
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
# Custom axes for the colorbar: [left, bottom, width, height]
cbar_ax = fig.add_axes([0.25, 0.05, 0.5, 0.02]) 
cbar = fig.colorbar(sm, cax=cbar_ax, orientation='horizontal', fraction=0.05, pad=0.1)
cbar.set_label('Time (s)', fontsize=15, fontweight='bold')
cbar.ax.tick_params(labelsize=20)


# Global title and layout
# fig.suptitle('Polygon vs Raster R2: Temp (1000m) (SPATIAL and TEMPORAL)', fontsize=25, fontweight='bold')
plt.tight_layout(rect=[0, 0.06, 1, 0.95])   # Adjust bottom, left, right, top
plt.show()
