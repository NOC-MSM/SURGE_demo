# **Welcome to the NEMO SURGE Demonstrator**

**Description**

---

## **Quick Start :rocket:**

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

    To automate the installation of NEMO and its dependencies (e.g., XIOS3, NETCDF, HDF5) on your local machine, we have provided a shell script in the `tools` directory. 