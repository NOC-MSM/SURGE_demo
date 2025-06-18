# -------------------------------------------------
# creare_AMM12_bathymetry.py
#
# Script to create a bathymetry file for the AMM12
# configuration in NEMO.
#
# -------------------------------------------------
# -- Import required libraries -- #
import xarray as xr
import os 

path_data = "/".join(os.getcwd().split('/')[:-2]) + "/data/"

# -- Open domain_cfg file -- #
domain_fpath = path_data + "AMM_R12_sco_domcfg.nc"
ds_domain = xr.open_dataset(domain_fpath)

# re-creates the tmask file from the bottom level array
tmask = ds_domain.e3t_0 * 0
for j in range(ds_domain.sizes["y"]):
    for i in range(ds_domain.sizes["x"]):
        i_bot = ds_domain.bottom_level.isel(y=j, x=i).values
        tmask[:i_bot, j ,i] = 1

# Masks the thickness of ground cell before summing the cells thicknesses
e3t = ds_domain.e3t_0 * tmask
bathy_meter = e3t.sum(dim='z')

# -- Create bathymetry dataset -- #
ds_bathy = xr.Dataset({
    'Bathymetry': (['y', 'x'], bathy_meter.data),
    'nav_lat': (['y', 'x'], ds_domain.gphit.squeeze().data),
    'nav_lon': (['y', 'x'], ds_domain.glamt.squeeze().data)
})

output_fpath = path_data + "bathy_meter_AMM12.nc"
ds_bathy.to_netcdf(output_fpath, unlimited_dims='time_counter')