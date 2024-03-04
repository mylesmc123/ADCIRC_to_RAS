# %%
import matplotlib.pyplot as plt

# Open a csv using pandas
import pandas as pd
df = pd.read_csv('surgeData/Harvey_Gulf.csv', delimiter='\t', header=0, names=['time', 'surge'])
df
# %%
# Convert the time column to a datetime object.
df['time'] = pd.to_datetime(df['time'])
# Remove rows beyond the end time of the wind data = 31-08-2017 00:00
df = df[df['time'] <= '31-08-2017 00:00']
df

# %%
# Plot df
fig, ax = plt.subplots()
ax.plot(df['time'], df['surge'])
# make x-axis labels not overlap
plt.xticks(rotation=45)
# Make x-axis labels more sparse.
ax.xaxis.set_major_locator(plt.MaxNLocator(5))
# Move the y-axis to the right side
ax.yaxis.tick_right()
ax.set_title('Surge (m)')
plt.show()
# %%
# Use matplotlib to animate a time series where the animation draws the plot across the x-axis through time.
# animate
import matplotlib.animation as animation
import numpy as np

# line plot animation
fig, ax = plt.subplots(1, 1, figsize = (6, 6))
ax.set_xlim(df['time'].iat[0], df['time'].iat[-1])
ax.set_ylim([1.1*np.min(df['surge']), 1.1*np.max(df['surge'])])
ax.yaxis.tick_right()
plt.xticks(rotation=45)
# Make x-axis labels more sparse.
ax.xaxis.set_major_locator(plt.MaxNLocator(5))
# Set title
ax.set_title('Surge (m)')


# Turn off x-axis label
# ax.set_xticklabels([])

def animate(i):
    ax.cla() # clear the previous image
    ax.plot(df['time'].iloc[:i], df['surge'].iloc[:i]) # plot the line
    ax.set_xlim(df['time'].iat[0], df['time'].iat[-1]) # fix the x axis
    ax.set_ylim([1.1*np.min(df['surge']), 1.1*np.max(df['surge'])]) # fix the y axis
    ax.set_title(f"Surge (m) {str(df['time'].iat[i])}")
    # Make x-axis labels more sparse.
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    # Rotate x-axis labels
    plt.xticks(rotation=45)

anim = animation.FuncAnimation(fig, animate, frames = len(df['time']), interval = 50, blit = False)
plt.show()

# %%
# save anim
anim.save('surge.mp4', writer='ffmpeg', fps=20)

# %%
# Create a geodataframe from a csv file containing columns with latitude and longitude

import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point, LineString, shape

df = pd.read_csv('surgeData/coordBoundaryGulf.csv', header=None, names=['lon', 'lat'])
df
# %%
# convert to geopandas dataframe as a line
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))
gdf

# %%
# Using row 200 as selected in: "V:\projects\p00659_dec_glo_phase3\01_processing\ADCIRC_forRAS\extract_wl_bc\extend\Harvey_extend.xlsx"
# Plot point 201 representing this position
x,y = gdf.iloc[201].geometry.x, gdf.iloc[201].geometry.y

# %%
ls = LineString( df[['lon','lat']].to_numpy() )
line_gdf = gpd.GeoDataFrame( [['Gulf']],crs='epsg:4326', geometry=[ls] )
line_gdf

# %%
# Plot the lineString in red
ax1 = line_gdf.plot(color="red", figsize=[4,10]);

# %%
# Plot with a basemap
import contextily as cx
ax = line_gdf.plot(figsize=(10, 10), edgecolor="k")
cx.add_basemap(ax, zoom=1)
ax

# %%
map = folium.Map(location=[30, -95], tiles="CartoDB Positron", zoom_start=8)
map
# %%
geo_j = line_gdf.to_json()
geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {"fillColor": "orange"})
# geo_j.add_to(map)
map

# %%
# add a marker for the selected point
folium.Marker([y, x], popup='Gulf', color="red").add_to(map)
map

# %% 
# Save to png
import io
from PIL import Image
img_data = map._to_png(5)
img = Image.open(io.BytesIO(img_data))
img.save('surge line.png')
# %%
