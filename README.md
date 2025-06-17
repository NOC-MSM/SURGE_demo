# SURGE_demo
NEMO v5.0.1 Hackathon Storm Surge Demonstrator using Shallow Water Equations

## Plan:

* Create demonstrator for existing Shallow Water Gyre test configuration.
* Introduce atmospheric pressure term to the SWE code.
* Create idealised Tropical Cyclone forcing (analytical winds & atmospheric pressure).
* Tidal boundary conditions / bathymetry.

## Namelist Modifications To Do:

* Initialisation from rest & T-S.
* Remove all forcing, except wind and atm. pressure -> use AMM7_surge SBC?
* Remove runoff and SSR.
* Remove CHL nn_chldta
* Tides: check boundary forcing for 1-layer, only tidal harmonics at bdy, rest initialised to initial state.
* Simplified EOS.
* Diagnostics outputs to be checked.
