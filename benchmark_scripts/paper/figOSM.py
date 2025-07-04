import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
import matplotlib.colors as mcolors

XTICKS_BIN = 1000
STEPS = 100

# bm1 = pd.read_csv('./benchmark_scripts/paper/fig1/ELVx_10000points_5km_uf5.csv')
# bm2 = pd.read_csv('./benchmark_scripts/paper/fig1/ELVx_10000points_25km_uf5.csv')
# bm3 = pd.read_csv('./benchmark_scripts/paper/fig1/ELVx_10000points_50km_uf5.csv')
# bm4 = pd.read_csv('./benchmark_scripts/paper/fig1/ELVx_10000points_100km_uf5.csv')
# bm5 = pd.read_csv('./benchmark_scripts/paper/fig1/ELVx_10000points_250km_uf5.csv')
# bm6 = pd.read_csv('./benchmark_scripts/paper/fig1/ELV_10000points_500km_uf5.csv')

# bm1 = pd.read_csv('./benchmark_scripts/paper/fig1/Snow_10000points_5km_uf5.csv')
# bm2 = pd.read_csv('./benchmark_scripts/paper/fig1/Snow_10000points_25km_uf5.csv')
# bm3 = pd.read_csv('./benchmark_scripts/paper/fig1/Snow_10000points_50km_uf5.csv')
# bm4 = pd.read_csv('./benchmark_scripts/paper/fig1/Snow_10000points_100km_uf5.csv')
# bm5 = pd.read_csv('./benchmark_scripts/paper/fig1/Snow_10000points_250km_uf5.csv')
# bm6 = pd.read_csv('./benchmark_scripts/paper/fig1/Snow_10000points_500km_uf5.csv')

bm1 = pd.read_csv('./benchmark_scripts/paper/figOSM/Temp_10000points_5km_uf5_OSM.csv')
bm2 = pd.read_csv('./benchmark_scripts/paper/figOSM/Temp_10000points_25km_uf5_OSM.csv')
bm3 = pd.read_csv('./benchmark_scripts/paper/figOSM/Temp_10000points_50km_uf5_OSM.csv')
bm4 = pd.read_csv('./benchmark_scripts/paper/figOSM/Temp_10000points_100km_uf5_OSM.csv')
bm5 = pd.read_csv('./benchmark_scripts/paper/figOSM/Temp_10000points_250km_uf5_OSMx.csv')
bm6 = pd.read_csv('./benchmark_scripts/paper/figOSM/Temp_10000points_500km_uf5_OSM.csv')



# Data
dataframes = [bm1, bm2, bm3, bm4, bm5, bm6]
titles = ['5 km² (R4)', '25 km² (R4)', '50 km² (R4)', '100 km² (R4)', '250 km² (R4)', '500 km² (R4)']

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
# norm = mcolors.LogNorm(vmin=ymin, vmax=ymax)
cmap = cm.Spectral_r # BuPu, YlGnBu, viridis_r, YlOrRd, RdYlBu_r

for i, (df, title) in enumerate(zip(dataframes, titles)):
    if i < len(axes):
        df_sorted = df.sort_values("Points")
        colors = cmap(norm(df_sorted["Processing_Time"]))

        # Bar plot with gradient color
        axes[i].bar(df_sorted["Points"], df_sorted["Processing_Time"], 
                    color=colors, alpha=0.9, width=STEPS)

        # Labels and titles
        axes[i].set_title(title, fontsize=21, fontweight='bold')
        # axes[i].set_yscale('log')
        axes[i].set_ylim(ymin, ymax)
        axes[i].margins(x=0)
        axes[i].tick_params(axis='x', rotation=45)
        # axes[i].set_xlabel('Points', fontsize=15, fontweight='bold')
        # axes[i].set_ylabel('Time (s)', fontsize=15, fontweight='bold')
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
cbar.ax.tick_params(labelsize=20)


# Global title and layout
# fig.suptitle('Different AOI - Munich (urban) vs Bavaria (state) vs Sweden (country) ', fontsize=25, fontweight='bold')
plt.tight_layout(rect=[0, 0.09, 1, 0.35])   # Adjust left, bottom, right, top
plt.savefig('./benchmark_scripts/paper/figGeoNames/fig7_200dpi_OSM.png', dpi=200)
plt.show()
