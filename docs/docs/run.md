# **Running AMM12_SURGE :fast_forward:**

!!! abstract

    In this fifth tutorial of the NEMO SURGE demonstrator, we cover how to run the `AMM12_surge` simulation with both atmosheric forcing and tidal forcing along the boundaries.

### Output

Now we have prepared the `domain_cfg`, initial conditions, atmospheric forcing and `namelist_cfg` for our `AMM12_SURGE` configuration, we next need to update the XIOS `.xml` files used to specify the output files of our simulation.

In our `AMM12_SURGE/EXP00/` run directory, we do the following:

```sh
cd .../SURGE_demo/nemo_5.0.1/cfgs/AMM12_SURGE/EXP00/

rm file_def_nemo-oce.xml
ln -s .../SURGE_demo/namelists/XIOS/file_def_nemo-oce_SURGE.xml file_def_nemo-oce.xml
```

### Running NEMO

Finally, we can run our `AMM12_SURGE` configuration using the NEMO executable on a single processor on our local machine or HPC:

```sh
./nemo
```