<br />
<p align="center">
  </a>
  <h1 align="center">NEMO SURGE Demonstrator</h1>

  <p align="center">
    <strong>Create a regional 1-layer storm surge model using NEMO version 5.0.1<strong>
    </a>
    <br />
    <br />
    ·
    <a href="https://noc-msm.github.io/SURGE_demo"><strong>Documentation</strong></a>
    ·
    <a href="https://github.com/NOC-MSM/SURGE_demo/issues"><strong>Report an Issue</strong></a>
    ·
  </p>
</p>

## **Description:**

This NEMO version 5.0.1 demonstrator shows how to create a 1-layer baroptropic storm surge model using the AMM12 regional configuration.

The instructions can be adapted to any region of the ocean by changing the bathymetry, coordinates, initial conditions and forcing files.

<p align="center">
    <a href="url"><img src="./docs/docs/assets/AMM12_SURGE_SSH.gif" align="center" height="170" width="200" ></a>
</p>

## **Background**

The coastlines of the United Kingdom are increasingly vulnerable to the impacts of storm surges driven by extreme weather events and rising sea levels. Accurate and efficient regional storm surge simulations are essential for early warning systems, risk assessment, and coastal planning.

Single-layer, barotropic storm surge models offer a simplified yet robust framework for simulating sea level responses to atmospheric forcing, such as wind, and sea level pressure and tides, without the added complexity of 3-dimensional processes.

This demonstrator adapts the AMM12 reference configuration covering the Northwest European Shelf. The AMM12 regional domain uses a regular lat-lon grid at approximately 12km horizontal resolution and S-coordinates in the vertical rather than z-coordinates. In addition to atmospheric forcing, our adapted AMM12_SURGE configuration is forced with tidal lateral boundary conditions using a flather boundary condition.

## **System Prerequisites**

We expect the following software to be installed on your local machine or HPC: 
* NETCDF
* XIOS3
* An arch file for your HPC (this just sets paths to XIOS, netcdf and the compiling option
which depends on your compiler)
* Python (for the creation of forcing files and analysis of outputs)

If you need to install any of the software above, we have provided an installation script in the `tools/` directory.

## **Resources Provided**

* Topography, coordinates, boundary conditions for the AMM12 reference configuration (`data/`).
* Python scripts to create idealised atmospheric forcing, initial conditions and 1-layer domain bathymetry (`src/scripts`).
* Namelist to build the 1-layer domain_cfg.nc file from the bathymetry and coordinates file (`namelists/domain`).
* Namelist for AMM12_SURGE configuration (`namelists/nemo`).

> **Get started with our [documentation...](https://noc-msm.github.io/SURGE_demo)** 
