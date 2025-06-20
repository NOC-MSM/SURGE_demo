# -------------------------------------------------
# create_AMM12_surge_idealised_forcing.py
#
# Script to idealised extratropical cyclone atm.
# forcing for the AMM12 SURGE configuration in NEMO.
#
# -------------------------------------------------
# -- Import required libraries -- #
import os 
import glob
import pandas as pd
import xarray as xr
import numpy as np
from paratc.tc_models import Holland1980 as h80

def main(run_dir: str) -> None:
    """
    Main function to create idealised atmospheric forcing files
    for the AMM12 SURGE configuration in NEMO.

    This function generates synthetic storm data using the Holland (1980)
    model and exports the zonal wind stress, meridional wind stress,
    and atmospheric pressure fields to NETCDF files.

    Parameters:
    ----------
    run_dir : str
        The directory where the AMM12 SURGE configuration run directory
        is located.
    """
    # -- Import AMM12 SURGE domain -- #
    domain_fpath = f"{run_dir}/AMM12_SURGE_domcfg.nc"
    ds_domain = xr.open_dataset(domain_fpath)

    # -- Import Existing SETTE AMM12 Atmospheric Forcing File -- #
    forcing_fpath = f"{run_dir}/fluxes/amm12_utau_y2012m01d*.nc"
    # Open existing atm. forcing files:
    ds_atm = xr.open_mfdataset(forcing_fpath)

    # -- Create synthetic storm track -- #
    # Synthetic storm moving zonally across model domain:
    dx_dt = 33/120
    lon_start = (((ds_domain.nav_lon.isel(y=50, x=0) + 180) % 360) - 180).values
    lon = lon_start + (np.arange(120) * dx_dt)
    # Update final longitude for storm to exit domain:
    lon[-1] = 14

    # Define storm parameters:
    lat = np.repeat(50, len(lon))
    pcen = np.repeat(985, len(lon)) # Central pressure in hPa
    penv = np.repeat(1010, len(lon)) # Background pressure in hPa
    rmw = np.repeat(60, len(lon)) # Radius of maximum wind in km
    time = ds_atm['t'].values[120:] # Last 5-days

    # Create a DataFrame with storm parameters:
    df = pd.DataFrame({
        'lon': lon,
        'lat': lat,
        'pcen': pcen,
        'penv': penv,
        'rmw': rmw,
        'time': time
    })

    # -- Generate synthetic storm wind + pressure fields using Holland (1980) model -- #
    # Define idealised storm using Holland (1980) model:
    storm = h80(df,
                (((ds_domain.nav_lon + 180) % 360) - 180).values,
                ds_domain.nav_lat.values,
                B_model='vickery00'
                )

    # Calculate wind stress using Large Pond (1982) drag coefficient model:
    storm.make_wind_stress(cd_model = 'large_pond82', cd_max = 3e-3)

    # -- Export synthetic atmospheric forcing to NETCDF Files -- #

    # === Zonal Wind Stress === #
    print("In Progress: Exporting synthetic storm zonal wind stress (N/m2) to NETCDF files...")
    # Collect first 10-days of SETTE AMM12 atm. forcing filenames:
    fnames = sorted(glob.glob(f"{run_dir}/fluxes/amm12_utau_y2012m01d*.nc"))

    # Define output filenames:
    out_fnames = [f.replace('amm12_', 'amm12_surge_') for f in fnames]

    # Iterate over 10-days of existing files and create idealised atm. forcing files:
    for n, f in enumerate(fnames):
        # Construct dataset from synthetic storm data:
        if n < 5:
            utau = storm.data.isel(time=slice(0, 24)).stress_u.data * 0.0  # Set to 0 N m-2 for first 5 days.
        else:
            utau = storm.data.isel(time=slice((n - 5)*24, (n - 5)*24 + 24)).stress_u.data

        ds_n = xr.Dataset(data_vars={"utau": (['t', 'y', 'x'], utau)},
                        coords={"nav_lat": (['y', 'x'], ds_domain.nav_lat.squeeze().data),
                                "nav_lon": (['y', 'x'], ds_domain.nav_lon.squeeze().data),
                                "t": ds_atm["t"].isel(t=slice(n*24, n*24 + 24)).data
                                })

        # Write to NETCDF file:
        ds_n.to_netcdf(out_fnames[n], mode='w', unlimited_dims="t")
        print(f"Completed: Write time slice {n} to file: {out_fnames[n]}")

    # === Meridional Wind Stress === #
    print("In Progress: Exporting synthetic storm meridional wind stress (N/m2) to NETCDF files...")
    # Collect 10-days of SETTE AMM12 atm. forcing filenames:
    fnames = sorted(glob.glob(f"{run_dir}/fluxes/amm12_vtau_y2012m01d*.nc"))

    # Define output filenames:
    out_fnames = [f.replace('amm12_', 'amm12_surge_') for f in fnames]

    # Iterate over 10-days of existing files and create idealised atm. forcing files:
    for n, f in enumerate(fnames):
        # Construct dataset from synthetic storm data:
        if n < 5:
            vtau = storm.data.isel(time=slice(0, 24)).stress_v.data * 0.0  # Set to 0 N m-2 for first 5 days.
        else:
            vtau = storm.data.isel(time=slice((n - 5)*24, (n - 5)*24 + 24)).stress_v.data

        ds_n = xr.Dataset(data_vars={"vtau": (['t', 'y', 'x'], vtau)},
                        coords={"nav_lat": (['y', 'x'], ds_domain.nav_lat.squeeze().data),
                                "nav_lon": (['y', 'x'], ds_domain.nav_lon.squeeze().data),
                                "t": ds_atm["t"].isel(t=slice(n*24, n*24 + 24)).data
                                })

        # Write to NETCDF file:
        ds_n.to_netcdf(out_fnames[n], mode='w', unlimited_dims="t")
        print(f"Completed: Write time slice {n} to file: {out_fnames[n]}")

    # === Atmospheric Pressure === #
    # Define output filenames:
    out_fnames = [f.replace('amm12_', 'amm12_surge_').replace('vtau', 'somslpre') for f in fnames]

    # Iterate over 10-days of existing files and create idealised atm. forcing files:
    print("In Progress: Exporting synthetic storm atmospheric pressure (Pa) to NETCDF files...")
    for n, f in enumerate(fnames):
        # Construct dataset from synthetic storm data:
        if n < 5:
            somslpre = storm.data.isel(time=slice(0, 24)).pressure.data * 0.0  # Set to 0 Pa for first 5 days.
        else:
            # Calulate sea-level pressure from storm data:
            somslpre = storm.data.isel(time=slice((n - 5)*24, (n - 5)*24 + 24)).pressure.data * 100  # Convert hPa to Pa

        ds_n = xr.Dataset(data_vars={"somslpre": (['t', 'y', 'x'], somslpre)},
                        coords={"nav_lat": (['y', 'x'], ds_domain.nav_lat.squeeze().data),
                                "nav_lon": (['y', 'x'], ds_domain.nav_lon.squeeze().data),
                                "t": ds_atm["t"].isel(t=slice(n*24, n*24 + 24)).data
                                })

        # Write to NETCDF file:
        ds_n.to_netcdf(out_fnames[n], mode='w', unlimited_dims="t")
        print(f"Completed: Write time slice {n} to file: {out_fnames[n]}")

# Entry point for the script:
if __name__ == "__main__":
    # Define NEMO AMM12_SURGE run directory path:
    run_dir = f"{'/'.join(os.getcwd().split('/')[:-2])}/nemo_5.0.1/cfgs/AMM12_SURGE/EXP00"

    # Create idealised atmospheric forcing files:
    main(run_dir=run_dir)