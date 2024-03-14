# %%
import pandas as pd
import xarray as xr
import glob

# Rain data: V:\projects\p00659_dec_glo_phase3\00_collection\Precip\Harvey
# Data directory contains netCDF files each file representing 1 hour of precip.
# Open each file an append to a single xarray dataset.

# GLO Harvey data_dir
# data_dir = '/mnt/v/projects/p00659_dec_glo_phase3/00_collection/Precip/Harvey'

# LWI Laura data_dir
data_dir = '/mnt/v/projects/p00832_ocd_2023_latz_hr/01_processing/Precipitation_AORC/nc_files/AORC_APCP_4KM_LMRFC_202008-09'

# get a list of all the netcdf files in the data directory using glob.
files = glob.glob(data_dir + '/*.nc4')
files.sort()
files

# %%
# open the first file to create the dataset
ds = xr.open_dataset(files[0])
# concatenate the remaining files to the dataset
for f in files[1:]:
    ds = xr.concat([ds, xr.open_dataset(f)], dim='time')

ds
# %%
# get first and last time
ds['time'].isel(time=0).values, ds['time'].isel(time=-1).values
# %%
# plot the rainfall for the 100th time step
import matplotlib.pyplot as plt
ds['APCP_surface'].isel(time=100).plot()

# %%
# For Laura, this AORC data starts at 2020-08-01 00:00:00 and ends at 2020-09-30 23:00:00 and has a 1Hour interval.
# The Laura Wind data starts at 2020-08-18 00:20:00 and ends at 2020-09-10 00:00:00 and has a 20Minute interval.
# Subset Laura Precip data to match the time range of the wind data.
ds = ds.sel(time=slice('2020-08-18 00:00:00', '2020-09-10 00:00:00'))
# get first and last time
ds['time'].isel(time=0).values, ds['time'].isel(time=-1).values
# %%
# The frame rate of the rain should equal to: [the wind framerate * (interval wind/interval rain)] => 21fps * .3hr/1hr = 7fps
fps = 7
#%%
# GLO
# map_coords={"llcrnrlat":28,
#             "urcrnrlat":30.5,
#             "llcrnrlon":96.33,
#             "urcrnrlon":-92.5}
# LWI
map_coords={"llcrnrlat":28,
            "urcrnrlat":33.5,
            "llcrnrlon":-95.5,
            "urcrnrlon":-87}

# %%
# clip the diemnsion of latitude and longitude to the GLO bounds: lat [28,30.5], lon[-96.33,-92.5].
# min_lon = -96.33 
# min_lat = 28 
# max_lon = -92.5
# max_lat = 30.5

# clip the diemnsion of latitude and longitude to the LWI bounds: lat [28,30.5], lon[-96.33,-92.5].
min_lon = -95.5
min_lat = 28 
max_lon = -87
max_lat = 33.5
ds = ds.where((ds['longitude'] > min_lon) & (ds['longitude'] < max_lon) & (ds['latitude'] > min_lat) & (ds['latitude'] < max_lat), drop=True)
ds['APCP_surface'].isel(time=200).plot()

# %%
# plot using a matplotlib basemap of the continenets
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib

lon,lat = np.meshgrid(ds["longitude"],ds["latitude"], sparse=False)


m = Basemap(projection='merc',llcrnrlat=map_coords["llcrnrlat"],urcrnrlat=map_coords["urcrnrlat"],\
          llcrnrlon=map_coords["llcrnrlon"],urcrnrlon=map_coords["urcrnrlon"],lat_ts=10,resolution='i')
lons, lats = m(lon,lat)

# %%
# Get the time value at which the maximum wind speed occurs.
precip_max = ds["APCP_surface"].max().values
ds_max = ds["APCP_surface"].compute().where(ds["APCP_surface"].compute() == precip_max, drop=True)
precip_max = ds_max.values[0][0][0]
precip_max_time = ds_max['time'].values[0]
precip_max_time # i = 225


# %%
fig, ax = plt.subplots()
color = np.ma.masked_array(ds["APCP_surface"].sel(time=precip_max_time), ds["APCP_surface"].sel(time=precip_max_time) < .1)
color = np.ma.masked_invalid(color) 
m.fillcontinents(color='#cc9955', zorder = 0)
m.pcolormesh(lons, lats, color, cmap=matplotlib.cm.CMRmap, alpha=0.5)
plt.colorbar()
titleTime = pd.to_datetime(str(precip_max_time)).strftime('%Y-%m-%d %H:%M')
plt.title(f'Precipitation (mm) {titleTime}')
plt.show()

# %%
plt.rcParams["figure.figsize"] = [7.00, 5.50]
plt.rcParams["figure.autolayout"] = True
fig, ax = plt.subplots()
lon,lat = np.meshgrid(ds["longitude"],ds["latitude"], sparse=False)
# cax = ax.pcolormesh(lon, lat, color, cmap=matplotlib.cm.CMRmap, alpha=0.5)
m = Basemap(projection='merc',llcrnrlat=map_coords["llcrnrlat"],urcrnrlat=map_coords["urcrnrlat"],\
          llcrnrlon=map_coords["llcrnrlon"],urcrnrlon=map_coords["urcrnrlon"],lat_ts=10,resolution='i')
lons, lats = m(lon,lat)
m.fillcontinents(color='#cc9955', zorder = 0)
cax = m.pcolormesh(lons, lats, color, cmap=matplotlib.cm.CMRmap, alpha=0.5)
fig.colorbar(cax)
# plt.title(f'Precipitation (mm)')
plt.show()

# %%
import matplotlib.animation as animation

def animate(i):
    z = np.ma.masked_array(ds["APCP_surface"].isel(time=i), ds["APCP_surface"].isel(time=i) < .01)
    z = np.ma.masked_invalid(z) 
    cax.set_array(ds["APCP_surface"].isel(time=i))
    t = pd.to_datetime(str(ds["time"].isel(time=i).values)).strftime('%Y-%m-%d %H:%M')
    fig.suptitle(f'Precipitation (mm) {t}')

anim = animation.FuncAnimation(fig, animate, interval=50, frames=range(0, len(ds["time"])))
anim.save('rain_laura.mp4', writer='ffmpeg', fps=fps)
plt.show()
# %%
