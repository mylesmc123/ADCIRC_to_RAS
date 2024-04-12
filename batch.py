# %%

# variables needed

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
# clip the diemnsion of latitude and longitude to the LWI bounds: lat [28,30.5], lon[-96.33,-92.5].
min_lon = -95.5
min_lat = 28 
max_lon = -87
max_lat = 33.5


# get events, regions, and adcirc data location.


# wind variables needed
# wind dataset
ds = xr.open_dataset("/mnt/v/projects/p00832_ocd_2023_latz_hr/01_processing/ADCIRC2RAS/Laura/ras_wind_laura_refTime_20200731_0000.nc", chunks={"node": 1000})
# wind vid ouput name


# rain variables needed
# LWI Laura data_dir
data_dir = '/mnt/v/projects/p00832_ocd_2023_latz_hr/01_processing/Precipitation_AORC/nc_files/AORC_APCP_4KM_LMRFC_202008-09'
# Subset Laura Precip data to match the time range of the wind data.
ds = ds.sel(time=slice('2020-08-18 00:00:00', '2020-09-10 00:00:00'))


# surge variables needed
# get segment from region
dss_file = "/mnt/v/projects/p00832_ocd_2023_latz_hr/01_processing/ADCIRC2RAS/Laura/Downstream_WSE_DSS/Segment_79.dss"
# the Laura surge data is 20 minute interval, starts at: 2020-08-17 19:20:00 and ends at 2020-09-09 19:00:00
# The Laura Wind data starts at 2020-08-18 00:20:00 and ends at 2020-09-10 00:00:00 and has a 20Minute interval.
# Subset Laura surge data to match the start time of the wind data.
df = df[df['time'] >= '2020-08-18 00:20:00']
# Using coordinates from DS boundary csv: V:\projects\p00832_ocd_2023_latz_hr\01_processing\GIS\Coastal_Segments
# Plot point 201 representing this position
x,y = -93.5044479397585,29.7656381397321