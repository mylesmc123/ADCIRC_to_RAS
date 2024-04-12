# %%
from pydsstools.heclib.dss import HecDss
from pydsstools.core import TimeSeriesContainer
import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point, LineString, shape
import contextily as cx
import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt

# %%
# Open dss file
dss_file = "/mnt/v/projects/p00832_ocd_2023_latz_hr/01_processing/ADCIRC2RAS/Laura/Downstream_WSE_DSS/Segment_79.dss"
ds = HecDss.Open(dss_file)
pathnames = ds.getPathnameList('*')
pathnames
# %%
# split pathnames by "/"
pathnames = [p.split("/") for p in pathnames]
# remove the Dpart at split index [4].
pathnames = [p[:4] + p[5:] for p in pathnames]
# put the split items back together as a string delimited by "/" 
pathnames = ["/".join(p) for p in pathnames]
# find the 4th instance of the character "/" and insert a "/" after it.
pathnames = [p[:p.find("/", p.find("/", p.find("/", p.find("/")+1)+1)+1)+1] + "/" + p[p.find("/", p.find("/", p.find("/", p.find("/")+1)+1)+1)+1:] for p in pathnames]
#remove duplicates
pathnames = list(set(pathnames))
pathnames
# %%
# use the first pathname and get the data as a pandas dataframe
pathname = pathnames[0]
ts = ds.read_ts(pathname)
ts.times
# %%
# ts contained ts.values and ts.times, convert to a pandas dataframe
df = pd.DataFrame({"time":np.array(ts.pytimes), "surge":ts.values})
df
# %%
# the Laura surge data is 20 minute interval, starts at: 2020-08-17 19:20:00 and ends at 2020-09-09 19:00:00
# The Laura Wind data starts at 2020-08-18 00:20:00 and ends at 2020-09-10 00:00:00 and has a 20Minute interval.
# Subset Laura surge data to match the start time of the wind data.
df = df[df['time'] >= '2020-08-18 00:20:00']
df
# %%
# the frame rate of the wind is 21fps, the frame rate of the surge should equal to: [the wind framerate * (interval wind/interval surge)] => 21fps * .3hr/.3hr = 21fps.
fps = 21
# Plot df
fig, ax = plt.subplots()
ax.plot(df['time'], df['surge'])
# make x-axis labels not overlap
plt.xticks(rotation=45)
# Make x-axis labels more sparse.
ax.xaxis.set_major_locator(plt.MaxNLocator(5))
# Move the y-axis to the right side
ax.yaxis.tick_right()
ax.set_title('Surge (ft)')
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
anim.save('surge_laura.mp4', writer='ffmpeg', fps=fps)

# %%
# Using coordinates from DS boundary csv: V:\projects\p00832_ocd_2023_latz_hr\01_processing\GIS\Coastal_Segments
# Plot point 201 representing this position
x,y = -93.5044479397585,29.7656381397321
map = folium.Map(location=[30, -95], tiles="CartoDB Positron", zoom_start=8)
# add a marker for the selected point
folium.Marker([y, x], popup='Segment 79', color="red").add_to(map)
map
# %%
# save map to html
map.save('Laura Segment 79.html')