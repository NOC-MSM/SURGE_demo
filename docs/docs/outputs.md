# **AMM12_SURGE Outputs**

!!! abstract

    In this final sixth tutorial of the NEMO SURGE demonstrator, we cover visualising the outputs of our `AMM12_surge` example simulation.

**Creating Animations of Atmospheric Forcing & SSH**

Now we have completed our `AMM12_SURGE` configuration, we next show how to produce animations of the atmospheric pressure of our synthetic storm and the sea surface height anomaly both with and without tidal forcing along the boundaries of our domain.

To produce the animations below, we have prodvided the `create_gifs_outputs_final.py` script, which can be run using our `env_surge_demo` virtual environment as follows:

```sh
conda activate env_surge_demo

cd SURGE_demo/src/scripts

python3 create_gifs_output_final.py
```

![Atmospheric Pressure:](./assets/AMM12_SURGE_atmpr_no_logo.gif){ align=center }
/// caption
Atmospheric Pressure
///

![Tidal Forcing:](./assets/AMM12_SURGE_SSH_tides_no_logo.gif){ align=center }
/// caption
Tidal Forcing
///

![Winds + Atm. Pressure:](./assets/AMM12_SURGE_SSH_no_logo.gif){ align=center }
/// caption
Winds + Atmospheric Pressure
///