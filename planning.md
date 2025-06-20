# NEMO SURGE Plan:

* Adapt AMM12 regional configuration to 1-layer s-coordinate case.
* Create idealised Extratropical Cyclone forcing (analytical winds & atmospheric pressure).
* Tidal boundary conditions / bathymetry.

## Namelist Modifications To Do:

* Initialisation from rest & T-S.
* Remove all forcing, except wind and atm. pressure -> use AMM7_surge SBC?
* Remove runoff and SSR.
* Remove CHL nn_chldta
* Tides: check boundary forcing for 1-layer, only tidal harmonics at bdy, rest initialised to initial state.
* Simplified EOS.
* Diagnostics outputs to be checked.

**AMM12 SURGE Model: namelist_cfg**
* Modified horizontal pressure gradient to ln_hpg_sco = .true. (s-coord standard Jacobian formulation)
* Modified bottom friction to ln_non_lin = .true. (non-linear bottom drag coefficient)
* T-S ensure initialised from the same temperature and salinity as the ln_seos reference values (see NEMO v5 manual)

**Domain Configuration: namelist_cfg**
* Use Jerome Chanut April 2022 (Emulating barotropic model) modification on Line 1484-1485 to set bottom_level = 1 (only 1 active level). 
* Use Song & Haidvogel (1994) hybrid S-sigma coordinate.
* rn_max = 1 (smoothing parameter for sigma coords) - remove all smoothing since no stratification present in 1-layer.
* rn_theta - 0.0 (applies stretching near surface) - removed as unnecessary.

**Demonstrator Steps To Explain:**
* Downloading NEMO + dependencies on local machine.
* Downloading AMM12 reference cfg data from SETTE using wget.
* Creating a bathy_meter.nc file from domain_cfg.nc.
* Updating the DOMAINcfg tool for the 1 active layer case.
* Generating new domain_cfg.nc and mesh_mask.nc files.
* Creating constant T-S initial state for 1 active layer case.
* Creating dummy surface heat and freshwater flux climatology files.
* Creating idealised atmospheric forcing - Holland (1980) Extratropical Cyclone.
* Modifications to the namelist_cfg for the 1 active layer case.
* Variables to include / exclude from XIOS3 xml files.
* Running AMM12_SURGE (local machine + HPC) for 5-day idealised case with tides.
* Visualising the outputs - animation + tidal harmonics for validation.