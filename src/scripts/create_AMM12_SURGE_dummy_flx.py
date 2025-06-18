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

# Creates a dummy 2-dimensional field:
dummy_dat = ds_domain.e2t.isel(time_counter=0) * 0

# -- Create dummy surface flux dataset -- #
ds_flux = xr.Dataset({
    'sonsfldo': (['y', 'x'], dummy_dat.data),
    'soshfldo': (['y', 'x'], dummy_dat.data),
    'sowafldo': (['y', 'x'], dummy_dat.data),
    'nav_lat': (['y', 'x'], ds_domain.gphit.squeeze().data),
    'nav_lon': (['y', 'x'], ds_domain.glamt.squeeze().data)
})

output_fpath = f"{path_data}/AMM12_SURGE_dummy_flx.nc"
ds_flux.to_netcdf(output_fpath, unlimited_dims='time_counter')