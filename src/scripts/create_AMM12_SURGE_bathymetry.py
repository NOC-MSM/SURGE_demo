# -------------------------------------------------
# create_AMM12_SURGE_bathymetry.py
#
# Script to create a bathymetry file for the AMM12
# configuration in NEMO.
#
# -------------------------------------------------
# -- Import required libraries -- #
import os
import xarray as xr

def main(run_dir: str) -> None:
    """
    Main function to create a bathymetry file for the AMM12
    configuration in NEMO.

    This function reads the domain configuration file, computes
    the bathymetry from the bottom level array, and saves the
    bathymetry data along with latitude and longitude coordinates
    into a new NETCDF file.

    Parameters:
    ----------
    run_dir : str
        The directory where the AMM12 SURGE configuration run directory
        is located.
    """
    # -- Open domain_cfg file -- #
    domain_fpath = f"{run_dir}/AMM_R12_sco_domcfg.nc"
    ds_domain = xr.open_dataset(domain_fpath)

    # Re-create tmask from the bottom level array:
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

    output_fpath = f"{run_dir}/bathy_meter_AMM12.nc"
    ds_bathy.to_netcdf(output_fpath, unlimited_dims='time_counter')

# Entry point for the script:
if __name__ == "__main__":
    # Define NEMO AMM12 SURGE run directory path:
    run_dir = f"{'/'.join(os.getcwd().split('/')[:-2])}/nemo_5.0.1/cfgs/AMM12_SURGE/EXP00"

    # Create idealised atmospheric forcing files:
    main(run_dir=run_dir)