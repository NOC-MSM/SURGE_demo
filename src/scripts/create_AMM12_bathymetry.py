# -------------------------------------------------
# creare_AMM12_bathymetry.py
#
# Script to create a bathymetry file for the AMM12
# configuration in NEMO.
#
# -------------------------------------------------
# -- Import required libraries -- #
import xarray as xr

# -- Open domain_cfg file -- #
domain_fpath = "/dssgfs01/scratch/otooth/NEMO_Hackathon/SURGE_demo/nemo_5.0.1/cfgs/AMM12_SURGE/EXP00/AMM_R12_sco_domcfg.nc"
ds_domain = xr.open_dataset(domain_fpath)

# -- Create bathymetry dataset -- #
ds_bathy = xr.Dataset({
    'Bathymetry': (['y', 'x'], ds_domain.e3t_0.isel(z=slice(15, 30)).sum(dim='z').data),
    'nav_lat': (['y', 'x'], ds_domain.gphit.squeeze().data),
    'nav_lon': (['y', 'x'], ds_domain.glamt.squeeze().data)
})

output_fpath = "/dssgfs01/scratch/otooth/NEMO_Hackathon/SURGE_demo/nemo_5.0.1/cfgs/AMM12_SURGE/EXP00/bathy_meter_AMM12.nc"
ds_bathy.to_netcdf(output_fpath,unlimited_dims='time_counter')