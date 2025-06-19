# **NEMO Namelists**

!!! abstract

    In this fourth tutorial of the NEMO SURGE demonstrator, we cover the changes to the `namelist_cfg` required to perform the `AMM12_surge` example simulation.

**Namelist**

Below we discuss the important changes to the `namelist_cfg` required for the AMM12 1-layer barotropic storm surge model:

**Temperature & Salinity (&namtsd)**

* Initialise our 1-layer regional model using constant temperature (10 degrees C) and salinity (35 PSU) from the `init_state_AMM12_SURGE_y2012.nc` file created in **Atmospheric Forcing Creation :cyclone:**.

```sh
!-----------------------------------------------------------------------
&namtsd        !    Temperature & Salinity Data  (init/dmp)             (default: OFF)
!-----------------------------------------------------------------------
   !                       ! =T  read T-S fields for:
   ln_tsd_init = .true.         !  ocean initialisation
   ln_tsd_dmp  = .false.         !  T-S restoring   (see namtra_dmp)

   cn_dir      = './'      !  root directory for the T-S data location
   !___________!_________________________!___________________!___________!_____________!________!___________!__________________!__________!_______________!
   !           !  file name              ! frequency (hours) ! variable  ! time interp.!  clim  ! 'yearly'/ ! weights filename ! rotation ! land/sea mask !
   !           !                         !  (if <0  months)  !   name    !   (logical) !  (T/F) ! 'monthly' !                  ! pairing  !    filename   !
   sn_tem = 'init_state_AMM12_SURGE',  -1.     , 'votemper',   .false.    , .false. , 'yearly'  ,    ''            ,    ''    ,    ''
   sn_sal = 'init_state_AMM12_SURGE',  -1.     , 'vosaline',   .false.    , .false. , 'yearly'  ,    ''            ,    ''    ,    ''
/
```

**Surface Boundary Conditions (&namsbc)**

* Use flux formulation to impose surface boundary conditions (`ln_flx`) and take the atmospheric pressure into account when
computing the surface pressure gradient (`ln_apr_dyn`). 

* Hourly zonal (`utau`) and meridional (`vtau`) wind stress is read from daily files generated in **Atmospheric Forcing Creation :cyclone:**.

* Dummy surface heat (0 W m-2) and freshwater fluxes (0 kg s-1 m-2) are read as climatologies from annual file.

```sh
!-----------------------------------------------------------------------
&namsbc        !   Surface Boundary Condition (surface module)          (default: NO selection)
!-----------------------------------------------------------------------
   nn_fsbc     = 1         !  frequency of SBC module call
   ln_flx      = .true.    !  flux formulation                          (T => fill namsbc_flx)
   ln_traqsr   = .false.   !  Light penetration in the ocean            (T => fill namtra_qsr)
   ln_ssr      = .false.   !  Sea Surface Restoring on T and/or S       (T => fill namsbc_ssr)
   ln_rnf      = .false.   !  runoffs                                   (T => fill namsbc_rnf)
   ln_apr_dyn  = .true.    !  Patm gradient added in ocean & ice Eqs.   (T => fill namsbc_apr )
/
!-----------------------------------------------------------------------
&namsbc_flx    !   surface boundary condition : flux formulation
!-----------------------------------------------------------------------
   cn_dir      = './fluxes/'  !  root directory for the fluxes data location
   !___________!_________________________!___________________!___________!_____________!________!___________!__________________!__________!_______________!
   !           !  file name              ! frequency (hours) ! variable  ! time interp.!  clim  ! 'yearly'/ ! weights filename ! rotation ! land/sea mask !
   !           !                         !  (if <0  months)  !   name    !   (logical) !  (T/F) ! 'monthly' !                  ! pairing  !    filename   !
   sn_utau     = 'amm12_surge_utau'      ,          1.       , 'utau'    ,  .true.     , .false., 'daily'   ,  ''              ,  ''      , ''
   sn_vtau     = 'amm12_surge_vtau'      ,          1.       , 'vtau'    ,  .true.     , .false., 'daily'   ,  ''              ,  ''      , ''
   sn_qtot     = 'AMM12_SURGE_dummy_flx' ,          -12      , 'sonsfldo',  .false.    , .true. , 'yearly'   ,  ''              ,  ''      , ''
   sn_qsr      = 'AMM12_SURGE_dummy_flx' ,          -12      , 'soshfldo',  .false.    , .true. , 'yearly'   ,  ''              ,  ''      , ''
   sn_emp      = 'AMM12_SURGE_dummy_flx' ,          -12      , 'sowafldo',  .false.    , .true. , 'yearly'   ,  ''              ,  ''      , ''
/
```

* Transform atmospheric pressure into an equivalent inverse barometer sea surface height.

* Hourly mean sea level pressure is read from daily files generated in **Atmospheric Forcing Creation :cyclone:**.

```sh
!-----------------------------------------------------------------------
&namsbc_apr    !   Atmospheric pressure used as ocean forcing           (ln_apr_dyn =T)
!-----------------------------------------------------------------------
   rn_pref     = 101000.   !  reference atmospheric pressure   [N/m2]/
   nn_ref_apr  =   0       !  ref. pressure: 0: constant, 1: global mean or 2: read in a file
   ln_apr_obc  = .true.    !  inverse barometer added to OBC ssh data

   cn_dir = './fluxes/'    !  root directory for the Patm data location
   !___________!_________________________!___________________!___________!_____________!________!___________!__________________!__________!_______________!
   !           !  file name              ! frequency (hours) ! variable  ! time interp.!  clim  ! 'yearly'/ ! weights filename ! rotation ! land/sea mask !
   !           !                         !  (if <0  months)  !   name    !   (logical) !  (T/F) ! 'monthly' !                  ! pairing  !    filename   !
   sn_apr      = 'amm12_surge_somslpre'  ,          1.       ,'somslpre' ,   .true.    , .false., 'daily'  ,    ''            ,    ''    ,      ''
/
```

**Tides (&nam_tide)**

* Activate tidal forcing, including tidal potential, on the domain boundaries.

* Use a linear ramp to introduce the tides over the duration of 1-day.

```sh
!-----------------------------------------------------------------------
&nam_tide      !   tide parameters                                      (default: OFF)
!-----------------------------------------------------------------------
   ln_tide     = .true.        ! Activate tides
   ln_tide_pot = .true. !  use tidal potential forcing
   sn_tide_cnames(1)  = 'Q1'   !  name of constituent
   sn_tide_cnames(2)  = 'O1'
   sn_tide_cnames(3)  = 'P1'
   sn_tide_cnames(4)  = 'S1'
   sn_tide_cnames(5)  = 'K1'
   sn_tide_cnames(6)  = '2N2'
   sn_tide_cnames(7)  = 'MU2'
   sn_tide_cnames(8)  = 'N2'
   sn_tide_cnames(9)  = 'NU2'
   sn_tide_cnames(10) = 'M2'
   sn_tide_cnames(11) = 'L2'
   sn_tide_cnames(12) = 'T2'
   sn_tide_cnames(13) = 'S2'
   sn_tide_cnames(14) = 'K2'
   sn_tide_cnames(15) = 'M4'

   ln_tide_ramp  = .true.               !  Use linear ramp for tides at startup
   rn_tide_ramp_dt = 1.               !  ramp duration in days
/
```

**Unstructured Open Boundaries (&nambdy)**

* Use Flather radiation scheme for the barotropic variables `cn_dyn2d = 'flather'`.

* Use tidal harmonic forcing without external tidal data.

* Use the Flow Relaxation Scheme (FRS) for all variables (`cn_tra`, `cn_dyn3d`) & set bdy data equal to the initial state (`nn_tra_dta = 0`).

```sh
!-----------------------------------------------------------------------
&nambdy        !  unstructured open boundaries                          (default: OFF)
!-----------------------------------------------------------------------
    ln_bdy     = .true.   !  Use unstructured open boundaries
    nb_bdy     =  1       !  number of open boundary sets
    !
    cn_dyn2d     = 'flather'
    nn_dyn2d_dta =  2
    cn_tra       = 'frs'
    nn_tra_dta   =  0 
    cn_dyn3d     = 'frs' 
/
```

**Bottom Drag (&namdrg)**

* Use non-linear bottom friction parameterisation assuming quadratic bottom friction.

```sh
!-----------------------------------------------------------------------
&namdrg        !   top/bottom drag coefficient                          (default: NO selection)
!-----------------------------------------------------------------------
! Quadratic
   ln_non_lin  = .true.      !  non-linear drag coefficient
   ln_loglayer = .false.     !  logarithmic drag: Cd = vkarmn/log(z/z0) |U|
/
```

**Equation Of Seawater (&nameos)**

* Use simplified Equation of State for Seawater with reference temperature and salinity consistent with initial conditions.

```sh
!-----------------------------------------------------------------------
&nameos        !   ocean Equation Of Seawater                           (default: NO selection)
!-----------------------------------------------------------------------
   ln_teos10   = .false.         ! = Use TEOS-10 equation of state
   ln_seos     = .true.          ! = Simplified EOS.
   rn_T0       = 10.             !  reference temperature
   rn_S0       = 35.             !  reference salinity
/
```

**Tracer Lateral Diffusion (&namtra_ldf)**

* Turn off lateral mixing - lateral diffusive tendency will not be applied to the tracer equation.

```sh
!-----------------------------------------------------------------------
&namtra_ldf    !   lateral diffusion scheme for tracers                 (default: NO selection)
!-----------------------------------------------------------------------
   ln_traldf_OFF   =  .true.   !  No explicit diffusion
   ln_traldf_lap   =  .false.   !    laplacian operator
   ln_traldf_hor   =  .true.   !  horizontal (geopotential)
   !                       !  Coefficients:
   nn_aht_ijk_t    = 0         !  =  0   constant = 1/2  Ud*Ld   (lap case) 
      rn_Ud        = 0.01           !  lateral diffusive velocity [m/s] (nn_aht_ijk_t= 0, 10, 20, 30)
      rn_Ld        = 10.e+3         !  lateral diffusive length   [m]   (nn_aht_ijk_t= 0, 10)
/
```

**Hydrostatic Pressure Gradient (&namdyn_hpg)**

* Use standard Jacobian formulation for pressure gradient with a generalised s(x, y, z, t) coordinates.

```sh
!-----------------------------------------------------------------------
&namdyn_hpg    !   Hydrostatic pressure gradient option                 (default: NO selection)
!-----------------------------------------------------------------------
   ln_hpg_prj  = .false.    !  s-coordinate (Pressure Jacobian scheme)
   ln_hpg_sco  = .true.     !  s-coordinate (standard jacobian formulation)
/
```