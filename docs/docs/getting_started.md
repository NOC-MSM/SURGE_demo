# **Getting Started :rocket:**

!!! abstract

    In this opening tutorial, we cover the installation of the dependencies required to follow the NEMO SURGE demonstrator.

### Installation

To get started, clone the SURGE_demo repository from [GitHub](https://github.com/NOC-MSM/SURGE_demo):

```sh
git clone git@github.com:NOC-MSM/SURGE_demo.git
```

Next, clone NEMO v5.0.1 inside the `SURGE_demo` directory:

```sh
cd SURGE_demo

git clone --branch 5.0.1 https://forge.nemo-ocean.eu/nemo/nemo.git nemo_5.0.1
```

**Note:** above we assume that you have already installed the [NEMO system-prerequisites](https://sites.nemo-ocean.io/user-guide/install.html#system-prerequisites) on your machine. If this is not the case, see the **Helpful Tip...** below.

??? tip "Helpful Tip..."

    To automate the installation of NEMO and its dependencies (e.g., XIOS2/3, NETCDF, HDF5) on your local machine, we have provided a shell script in the `tools` directory. 

### Compiling NEMO

Now we have cloned NEMO v5.0.1, we next need to compile NEMO on our local machine or HPC.

Let's first look at the contents of the `nemo_5.0.1` directory:

```sh
cd nemo_5.0.1
```

| Directory      | Description                          |
| ----------- | ------------------------------------ |
| `arch`      | contains the compilation settings  |
| `cfgs` | contains the reference configurations, including `AMM12` |
| `doc` | contains useful documentation |
| `ext` | includes NEMO dependencies |
| `mk` | includes compilation scripts |
| `src` | includes the NEMO .F90 model routines can be found |
| `tests` | includes idealized test-cases |
| `tools` | includes pre and post processing tools |

We can automatically set-up an Arch file using `build_arch-auto.sh` to create an arch file called `arch-auto.fcm`:
```sh
cd arch

./build_arch-auto.sh
```

Alternatively, we could modify an existing arch file in the `arch` directory, making sure the variables: `%NCDF_HOME`; `%HDF5_HOME` and `%XIOS_HOME` should be set to the installation directories used for XIOS installation.

We can now use `makenemo` to compile the `AMM12` reference configuration:
```sh
cd  nemo_5.0.1

./makenemo -m 'Anemone-ifort-xios3' -j 32 -r 'AMM12' -n 'AMM12_SURGE'
```

??? tip "Helpful Tip..."

    To use XIOS3, we must first update the list of active CPP keys in the `AMM12` reference configuration `.../SURGE_demo/nemo_5.0.1/cfgs/AMM12/cpp_AMM12.fcm` file to include the `key_xios3` key in addition to `key_xios`. Otherwise, we will encounter an error during compilation.

In the example above, we use the `arch/NOC/arch-Anemone-ifort-xios3.fcm` file.

The `AMM12_SURGE` configuration is now compiled in the `nemo_5.0.1/cfgs/AMM12_SURGE` directory with the following sub-directories:

| Directory      | Description                          |
| ----------- | ------------------------------------ |
| `BLD` | BuiLD directory: target executable, libraries, preprocessed routines, … |
| `EXP00` |  Run directory: link to executable, namelists, *.xml and IOs |
| `EXPREF` | Files under version control only for official configurations |
| `MY_SRC` | Your new routines or your modified copies of NEMO sources |
| `WORK` | Links to all fortran routines that you will compile |

### Compiling DOMAINcfg tool

Now we have compiled our `AMM12_SURGE` configuration, we next need to compile the NEMO DOMAINcfg tool on our local machine or HPC.

Before compiling, we first need to modify the `zgr_sco` subroutine in `domzgr.F90` file to handle the creation of a 1-layer S-coordinate `domain_cfg.nc` file.

On [Line 1481](https://forge.nemo-ocean.eu/nemo/nemo/-/blob/main/tools/DOMAINcfg/src/domzgr.F90?ref_type=heads#L1484) `SURGE_demo/nemo_5.0.1/tools/DOMAIN_cfg/src/domzgr.F90`:
```sh
      ! HYBRID : 
      DO jj = 1, jpj
         DO ji = 1, jpi
            DO jk = 1, jpkm1
               ! Modify MAX( 2, jk ) to MAX( 1, jk ) - Jerome Chanut (April 2022):
               IF( scobot(ji,jj) >= gdept_0(ji,jj,jk) )   mbathy(ji,jj) = MAX( 1, jk )
            END DO
         END DO
      END DO
```

Then, we can compile our modified DOMAINcfg tool using `maketools`:

```sh
cd  nemo_5.0.1/tools

./maketools -m Anemone-ifort-xios3 -j 16 -n DOMAINcfg
```

The DOMAINcfg tool is now compiled.

### Downloading AMM12 ancillary files:

We now need to download the ancillary files (topography, domain, boundary and atmospheric forcing) for the AMM12 reference configuration used for SETTE testing.

In our `EXP00` run directory, let's download and uncompress the tarball of input files:

```sh
cd ../cfgs/AMM12_SURGE/EXP00/

wget "https://gws-access.jasmin.ac.uk/public/nemo/sette_inputs/r5.0.0/AMM12_v5.0.0.tar.gz"

tar -xvf AMM12_v5.0.0.tar.gz

cd AMM12_v5.0.0

mv * ..
rm -rf AMM12_v5.0.0
```

### Creating a Python virtual environment:

To run the Python scripts provided for the creation of bathymetry, initial conditions and idealised atmospheric forcing, we first need to create a virtual environment.

!!! info Option 1: venv + pip

    ```sh
    python3 -m venv env_surge_demo

    source env_surge_demo/bin/activate

    pip install --upgrade pip
    pip install -r requirements.txt

    deactivate
    ```

!!! info Option 2: conda

    ```sh
    conda env create -f environment.yml

    source "$(conda info --base)/etc/profile.d/conda.sh"

    conda activate env_surge_demo
    ```

!!! success

    You have now compiled and downloaded all of the ingredients needed to create our `AMM12_SURGE` domain, initial conditions & forcing ancillary files.

    Next, continue to the second tutorial **Domain Creation :globe_with_meridians:** to create the `domain_cfg.nc` file for our 1-layer model.