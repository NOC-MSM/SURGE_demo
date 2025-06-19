# -------------------------------------------------
# create_AMM12_SURGE_init_state.py
#
# Script to create an homogeneous init state for the
# AMM12 SURGE configuration in NEMO.
#
# -------------------------------------------------
# -- Import required libraries -- #
import os 
import xarray as xr

def main(run_dir: str) -> None:
    """
    Main function to create the dummy flux file for the AMM12 SURGE configuration.
    
    Parameters:
    ----------
    run_dir : str
        The directory where the AMM12 SURGE configuration run directory is located.
    """
    # -- AMMM12 SURGE Open domain_cfg file -- #
    domain_fpath = f"{run_dir}/AMM12_SURGE_domcfg.nc"
    ds_domain = xr.open_dataset(domain_fpath)

    # Create dummy temperature and salinity fields:
    # Use reference rn_T0 and rn_S0 in nameos (ln_seos=.true.).
    T_dat = (ds_domain.e3t_0.squeeze() * 0) + 10.
    S_dat = (ds_domain.e3t_0.squeeze() * 0) + 35.

    # -- Create bathymetry dataset -- #
    ds_init = xr.Dataset({
        'votemper': (['z', 'y', 'x'], T_dat.data),
        'vosaline': (['z', 'y', 'x'], S_dat.data),
        'nav_lat': (['y', 'x'], ds_domain.gphit.squeeze().data),
        'nav_lon': (['y', 'x'], ds_domain.glamt.squeeze().data)
    })

    output_fpath = f"{run_dir}/init_state_AMM12_SURGE_y2012.nc"
    ds_init.to_netcdf(output_fpath, unlimited_dims='time_counter')

# Entry point for the script:
if __name__ == "__main__":
    # Define NEMO AMM12_SURGE run directory path:
    run_dir = f"{'/'.join(os.getcwd().split('/')[:-2])}/nemo_5.0.1/cfgs/AMM12_SURGE/EXP00"

    # Create idealised atmospheric forcing files:
    main(run_dir=run_dir)
