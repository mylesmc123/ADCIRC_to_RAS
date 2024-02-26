# %%
import xarray as xr
adcirc_fort63_file = r"/mnt/v/projects/p00659_dec_glo_phase3/00_collection/ADCIRC_CTXCS_S2G_CSTORM/CTXCS_TP_0011_HIS_Tides_1_SLC_0_RFC_0_WAV_1_GCP_S2G03BE01_fort.63"
# adcirc_fort63_file = "Z:/SLaMM_Mar2022/ADCIRC winds and water levels/wind/Ida/Idafort.74.nc"
# adcirc_fort63_file = r"/mnt/z/SLaMM_Mar2022/ADCIRC winds and water levels/wind/Ida/Idafort.74.nc"
ds = xr.open_dataset(adcirc_fort63_file, drop_variables=['neta','nvel'], chunks={"node": 1000})
ds
# %%
