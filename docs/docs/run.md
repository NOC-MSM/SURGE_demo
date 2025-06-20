# **Running AMM12_SURGE :fast_forward:**

!!! abstract

    In this fifth tutorial of the NEMO SURGE demonstrator, we cover how to run the `AMM12_surge` simulation with both atmosheric forcing and tidal forcing along the boundaries.

### Output

Now we have prepared the `domain_cfg`, initial conditions, atmospheric forcing and `namelist_cfg` for our `AMM12_SURGE` configuration, we next need to update the XIOS `.xml` files used to specify the output files of our simulation.

```sh
cd .../
git clone git@github.com:NOC-MSM/SURGE_demo.git
```

### Running NEMO

Now we have prepared the `domain_cfg`, initial conditions, atmospheric forcing and `namelist_cfg` for our `AMM12_SURGE` configuration, we next need to update the XIOS `.xml` files used to specify the output files of our simulation.

```sh
./nemo
```