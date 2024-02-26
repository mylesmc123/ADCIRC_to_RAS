# %%
import numpy as np

# %%
# Open numpy pickle file
u = np.load("wind_u_result_nstep0", allow_pickle=True)
u.max
# %%
v = np.load("wind_v_result_nstep0", allow_pickle=True)
v

# %%
w = np.load("wind_data", allow_pickle=True)
w

# %%
wind_u_raw = w[0]
wind_v_raw = w[1]
wind_u_raw
# %%
wind_v_raw
# %%
wind_u_raw.max()

# %%
wind_v_raw.max()
# %%
wind_u_raw.min()
# %%
wind_v_raw.min()

# %%
w[0].head(10)
# %%
