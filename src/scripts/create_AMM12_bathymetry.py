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
ds_domain = ds_domain.rename({'z': 'nav_lev'})

# -- Open mesh_mask file -- #
mesh_mask_fpath = "/dssgfs01/scratch/otooth/NEMO_Hackathon/SURGE_demo/nemo_5.0.1/cfgs/AMM12_SURGE/EXP00/AMM_R12_sco_mesh_mask.nc"
ds_mesh_mask = xr.open_dataset(mesh_mask_fpath)

# Define masked bathymetry:
bathymetry = ds_domain.e3t_0.squeeze().where(ds_mesh_mask.tmask.squeeze() == 1).sum(dim='nav_lev')
bathy_meter = xr.where(ds_domain.top_level.squeeze() == 1, bathymetry, 0)

# -- Create bathymetry dataset -- #
ds_bathy = xr.Dataset({
    'Bathymetry': (['y', 'x'], bathy_meter.data),
    'nav_lat': (['y', 'x'], ds_domain.gphit.squeeze().data),
    'nav_lon': (['y', 'x'], ds_domain.glamt.squeeze().data)
})

output_fpath = "bathy_meter_AMM12.nc"
ds_bathy.to_netcdf(output_fpath, unlimited_dims='time_counter')