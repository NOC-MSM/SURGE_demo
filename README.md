# SURGE_demo
NEMO v5.0.1 Hackathon Storm Surge Demonstrator using Shallow Water Equations

## Plan:

* Create demonstrator for existing Shallow Water Gyre test configuration.
* Introduce atmospheric pressure term to the SWE code.
* Create idealised Tropical Cyclone forcing (analytical winds & atmospheric pressure).
* Tidal boundary conditions / bathymetry.

## Namelist Modifications To Do:

* Initialisation from rest & T-S.
* [ ] Remove all forcing, except wind and atm. pressure -> use AMM7_surge SBC?
* [ ] Remove runoff and SSR.
* [ ] Remove CHL nn_chldta
* [ ] Tides: check boundary forcing for 1-layer, only tidal harmonics at bdy, rest initialised to initial state.
* [ ] Simplified EOS.
* [ ] Diagnostics outputs to be checked.

**AMM12 SURGE Model: namelist_cfg**
* Modified horizontal pressure gradient to ln_hpg_sco = .true. (s-coord standard Jacobian formulation)
* Modified bottom friction to ln_non_lin = .true. (non-linear bottom drag coefficient)
* T-S ensure initialised from the same temperature and salinity as the ln_seos reference values (see NEMO v5 manual)

**Domain Configuration: namelist_cfg**
* Use Jerome Chanut April 2022 (Emulating barotropic model) modification on Line 1484-1485 to set bottom_level = 1 (only 1 active level). 
* Use Song & Haidvogel (1994) hybrid S-sigma coordinate.
* rn_max = 1 (smoothing parameter for sigma coords) - remove all smoothing since no stratification present in 1-layer.
* rn_theta - 0.0 (applies stretching near surface) - removed as unnecessary.

