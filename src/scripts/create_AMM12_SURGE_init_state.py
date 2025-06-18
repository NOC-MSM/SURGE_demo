# -------------------------------------------------
# creare_init_state.py
#
# Script to create an homogeneous init state for the AMM12 SURGE
# configuration in NEMO.
#
# -------------------------------------------------
# -- Import required libraries -- #
import xarray as xr
import os 

# Define path to data directory:
path_data = "/".join(os.getcwd().split('/')[:-2]) + "/data/"

# -- AMMM12 SURGE Open domain_cfg file -- #
domain_fpath = f"{path_data}AMMM12_SURGE_domcfg.nc"
ds_domain = xr.open_dataset(domain_fpath)

# Create dummy temperature and salinity fields:
# Use reference rn_T0 and rn_S0 in nameos (ln_seos=.true.).
T_dat = ds_domain.e3t_0.isel(time_counter=0) * 0 + 10.
S_dat = ds_domain.e3t_0.isel(time_counter=0) * 0 + 35.

# -- Create bathymetry dataset -- #
ds_init = xr.Dataset({
    'votemper': (['z', 'y', 'x'], T_dat.data),
    'vosaline': (['z', 'y', 'x'], S_dat.data),
    'nav_lat': (['y', 'x'], ds_domain.gphit.squeeze().data),
    'nav_lon': (['y', 'x'], ds_domain.glamt.squeeze().data)
})

output_fpath = f"{path_data}/init_state_AMM12_SURGE.nc"
ds_init.to_netcdf(output_fpath, unlimited_dims='time_counter')