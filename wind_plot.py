# %%
from time import strftime, strptime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import xarray as xr
from mpl_toolkits.basemap import Basemap
import matplotlib.animation as animation

# %%
# open netcdf file in to xarray dataset
ds = xr.open_dataset("windData/CTXCS_TP_0011_HIS_Tides_1_SLC_0_RFC_0_WAV_1_GCP_S2G03BE01_fort.74_5.nc", chunks={"node": 1000})
ds

# %%
# compute the wind speed from the wind_u and wind_v variables.
# wind speed = sqrt(wind_u^2 + wind_v^2)
ds["windspeed"] = np.sqrt(ds["wind_u"]**2 + ds["wind_v"]**2)
   
lon,lat = np.meshgrid(ds["lon"],ds["lat"], sparse=False)


m = Basemap(projection='merc',llcrnrlat=28,urcrnrlat=30.5,\
          llcrnrlon=-96.33,urcrnrlon=-92.5,lat_ts=10,resolution='i')
lons, lats = m(lon,lat)

# %%
# Get the time value at which the maximum wind speed occurs.
windspeed_max = ds["windspeed"].max().values
ds_max = ds["windspeed"].compute().where(ds["windspeed"].compute() == windspeed_max, drop=True)
windspeed_max_time = ds_max['time'].values[0]

# Get wx and wy at the time of maximum wind speed
wx_max = ds["wind_u"].sel(time=windspeed_max_time)
wy_max = ds["wind_v"].sel(time=windspeed_max_time)
n=0
color = ds["windspeed"].sel(time=windspeed_max_time)
norm = matplotlib.colors.Normalize()
norm.autoscale(color)
sm = matplotlib.cm.ScalarMappable(cmap=matplotlib.cm.CMRmap, norm=norm)
sm.set_array([])

# init wx and wy
wx = ds["wind_u"].isel(time=0)
wy = ds["wind_v"].isel(time=0)

# %%
# Create an animation of the wind speed and direction
fig, ax = plt.subplots()
q = m.quiver(lons[0,:],lats[:,0],wx, wy, color, scale=100)
m.fillcontinents(color='#cc9955', zorder = 0)
plt.colorbar(q)
t = pd.to_datetime(str(ds["time"].isel(time=0).values)).strftime('%Y-%m-%d %H:%M')
plt.title(f'Wind velocity (m/s) and direction {t}')

def update_quiver(num, q, ax):
    """updates the horizontal and vertical vector components by a
    fixed increment on each frame
    """
    wx = ds["wind_u"].isel(time=num)
    wy = ds["wind_v"].isel(time=num)
    color = ds["windspeed"].isel(time=num)
    norm = matplotlib.colors.Normalize()
    norm.autoscale(color)
    sm = matplotlib.cm.ScalarMappable(cmap=matplotlib.cm.CMRmap, norm=norm)
    sm.set_array([])
    q.set_UVC(wx, wy, color)
    # update the title of the plot
    t = pd.to_datetime(str(ds["time"].isel(time=num).values)).strftime('%Y-%m-%d %H:%M')
    ax.set_title(f'Wind (m/s) {t}')
    return q,

ani = animation.FuncAnimation(fig, update_quiver, fargs=(q, ax), frames=range(0, len(ds["time"])), interval=50)
ani.save('wind.mp4', writer='ffmpeg', fps=20)
# %%
