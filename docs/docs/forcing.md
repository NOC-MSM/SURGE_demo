# **Atmospheric Forcing Creation**

!!! abstract

    In this third tutorial of the NEMO SURGE demonstrator, we cover the creation of synthetic atmospheric forcing and initial conditions for the `AMM12_SURGE` configuration.

**Initial Conditions Preparation**
We initialised the 1-layer `AMM12_SURGE` configuration from the constant reference temperature (T = 10$^{\circ}$C) and salinity (S = 35 PSU) values included in the simplified Equation of State in NEMO.

To generate the file containing the initial temperature and salinity fields, we run the `create_AMM12_SURGE_init_state.py` Python script using our `env_surge_demo` virtual environment:

```sh
conda activate env_surge_demo

cd SURGE_demo/src/scripts

python3 create_AMM12_SURGE_init_state.py
```

The script creates constant temperature and salinity fields and writes them to a new file `init_state_AMM12_SURGE_y2012.nc` in this directory.

**Synthetic Atmospheric Forcing Preparation**

Instead of forcing our `AMM12_SURGE` configuration with the fields provided in `flux/` directory (SETTE input files), we will generate wind stress and sea level pressure fields for a synthetic storm moving zonally (west to east) across the model domain.

To do this, we will use the `ParaTC` Python package installed in our virtual environment in **Getting Started**. The ParaTC: Parametric Tropical Cyclones package allows us to create 2-dimensional sea level pressure and wind stress fields by specifying a synthetic storm track, defined by the location & pressure at the storm's centre and the radius of maximum winds. 

We use the Holland (1980) analytical model of wind and pressure profiles in tropical cyclones and the Vickery et al. (2000) method to calculate the Holland B parameter.

The key parameters for the synthetic storm track are as follows:

| Parameter      | Value [Unit]                          |
| ----------- | ------------------------------------ |
| `lat`      | 50 [degrees N]  |
| `translation_speed`      | 6.6 [degrees E / day]  |
| `central_pressure`      | 985 [hPa]  |
| `ambient_pressure`      | 1010 [hPa]  |
| `radius_max_winds`      | 50 [km]  |

To calculate the zonal and meridional wind stress from the synthetic wind field, we use the Large and Pond (1982) formulation.

To run the `create_AMM12_SURGE_idealised_forcing.py` Python script using our `env_surge_demo` virtual environment:

```sh
python3 create_AMM12_SURGE_idealised_forcing.py
```

The script generates separate daily files containing 1-hourly forcing data for zonal wind stress, meridional wind stress and sea level pressure with the following naming convention:

| Parameter      | Filename                         |
| ----------- | ------------------------------------ |
| `utau`      | amm12_surge_utau_y2012m01d{01-05}.nc  |
| `vtau`      | amm12_surge_utau_y2012m01d{01-05}.nc  |
| `somslpre`      | amm12_surge_somslpre_y2012m01d{01-05}.nc  |

---
**References**

Holland, G. J., 1980: An analytical model of the wind and pressure profiles in hurricanes. Mon. Wea. Rev., 108 , 1212–1218.

Large, W. G., and S. Pond, 1982: Sensible and Latent Heat Flux Measurements over the Ocean. J. Phys. Oceanogr., 12, 464–482.

Vickery, P. J., P. F. Skerlj, A. C. Steckley, and L. A. Twisdale, 2000: Hurricane wind field model for use in hurricane simulations. J. Struct. Eng., 126 , 1203–1221.
