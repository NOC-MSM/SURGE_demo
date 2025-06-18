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

path_data = "/".join(os.getcwd().split('/')[:-2]) + "/data/"

# -- AMMM12 SURGE Open domain_cfg file -- #
domain_fpath = f"{path_data}AMMM12_SURGE_domcfg.nc"
ds_domain = xr.open_dataset(domain_fpath)

# Creates a zero field
dummy_dat = ds_domain.e2t.isel(time_counter=0) * 0

# -- Create bathymetry dataset -- #
ds_bathy = xr.Dataset({
    'qtot': (['y', 'x'], dummy_dat.data),
    'qsr': (['y', 'x'], dummy_dat.data),
    'emp': (['y', 'x'], dummy_dat.data),
    'nav_lat': (['y', 'x'], ds_domain.gphit.squeeze().data),
    'nav_lon': (['y', 'x'], ds_domain.glamt.squeeze().data)
})

output_fpath = path_data + "AMM12_SURGE_dummy_flx.nc"
ds_bathy.to_netcdf(output_fpath, unlimited_dims='time_counter')