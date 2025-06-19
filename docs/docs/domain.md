# **Domain Creation :globe_with_meridians:**

!!! abstract

    In this second tutorial of the NEMO SURGE demonstrator, we cover the creation of a single active layer `domain_cfg.nc` input file for the `AMM12_SURGE` configuration.

**Bathymetry Creation**

Before running the `DOMAINcfg` tool, we first need to create a file containing the bathymetry of the AMM12 reference configuration domain. 

We do this by running the `create_AMM12_SURGE_bathymetry.py` Python script in the `/scripts` directory using our `env_surge_demo` virtual environment as follows:

```sh
conda activate env_surge_demo

cd SURGE_demo/src/scripts

python3 create_AMM12_SURGE_bathymetry.py
```

The script calculates the `Bathymetry` (m) using the `AMM_R12_sco_domcfg.nc` stored in the `AMM12_SURGE/EXP00` run directory and writes this to a new file `bathy_meter_AMM12.nc` in this directory.

**DOMAINcfg Input File Preparation**

Next we need to prepare the namelists and input files for the `DOMAINcfg` tool.

We start by creating a `DOMAIN_AMM12_SURGE` directory in our `AMM12_SURGE/EXP00` run directory and adding a link to our newly created bathymetry input file:

```sh
cd ../../nemo_5.0.1/cfgs/AMM12_SURGE
mkdir DOMAIN_AMM12_SURGE

cd DOMAIN_AMM12_SURGE
ln -s ../bathy_meter_AMM12.nc .
```
Then, we need to add links to the `make_domain_cfg` executable and `namelist_ref` files. We also include a link to the modified `namelist_cfg` file prepared for this demonstrator in the `SURGE_demo/namelists/domain/` directory:

```sh
ln -s ../AMM_R12_sco_domcfg.nc .
ln -s .../SURGE_demo/nemo_5.0.1/tools/DOMAINcfg/BLD/bin/make_domain_cfg.exe .
ln -s .../SURGE_demo/nemo_5.0.1/tools/DOMAINcfg/namelist_ref .
ln -s .../SURGE_demo/namelists/domain/namelist_cfg .
```

Finally, we can run the `DOMAINcfg` tool using the following command:

```sh
./make_domain_cfg.exe
```

This will produce `domain_cfg.nc` and `mesh_mask.nc` files in the current directory, so we add links to these in the run directory.

```sh
cd ..

ln -s DOMAIN_AMM12_SURGE/domain_cfg.nc AMM12_SURGE_domcfg.nc
ln -s DOMAIN_AMM12_SURGE/mesh_mask.nc AMM12_SURGE_mesh_mask.nc
```

!!! success

    You have now created the `domain_cfg.nc` file for our 1-layer barotropic `AMM12_SURGE` configuration.

    Next, continue to the third tutorial **Atmospheric Forcing Creation :cyclone:** to generate idealised atmospheric forcing using a synthetic storm system.