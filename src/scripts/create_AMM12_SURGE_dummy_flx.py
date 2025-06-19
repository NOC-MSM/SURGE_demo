# -------------------------------------------------
# create_AMM12_SURGE_dummy_flx.py
#
# Script to create dummy surface flux files for the
# AMM12 SURGE configuration in NEMO.
#
# -------------------------------------------------
# -- Import required libraries -- #
import os 
import xarray as xr

def main(run_dir: str) -> None:
    """
    Main function to create a dummy surface flux file for the AMM12
    configuration in NEMO.

    This function reads the domain configuration file, creates a dummy
    surface flux dataset, and saves it into a new NETCDF file.

    Parameters:
    ----------
    run_dir : str
        The directory where the AMM12 SURGE configuration run directory
        is located.
    """
    # -- AMMM12 SURGE Open domain_cfg file -- #
    domain_fpath = f"{run_dir}/AMM12_SURGE_domcfg.nc"
    ds_domain = xr.open_dataset(domain_fpath)   

    # Creates a dummy 2-dimensional field:
    dummy_dat = ds_domain.e2t.squeeze() * 0

    # -- Create dummy surface flux dataset -- #
    ds_flux = xr.Dataset({
        'sonsfldo': (['y', 'x'], dummy_dat.data),
        'soshfldo': (['y', 'x'], dummy_dat.data),
        'sowafldo': (['y', 'x'], dummy_dat.data),
        'nav_lat': (['y', 'x'], ds_domain.gphit.squeeze().data),
        'nav_lon': (['y', 'x'], ds_domain.glamt.squeeze().data)
    })

    output_fpath = f"{run_dir}/fluxes/AMM12_SURGE_dummy_flx.nc"
    ds_flux.to_netcdf(output_fpath, unlimited_dims='time_counter')

# Entry point for the script:
if __name__ == "__main__":
    # Define NEMO AMM12 SURGE run directory path:
    run_dir = f"{'/'.join(os.getcwd().split('/')[:-2])}/nemo_5.0.1/cfgs/AMM12_SURGE/EXP00"

    # Create idealised atmospheric forcing files:
    main(run_dir=run_dir)