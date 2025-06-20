"""
surge_anim.py

A python script to build an animation of 2D .nc files

A new environment was build as follows::
    module load anaconda/5-2021
    conda create -p /work/jelt/conda-env/ntslf_py39 python=3.9
    conda activate /work/jelt/conda-env/ntslf_py39
    conda install netCDF4 numpy xarray matplotlib
    conda install cartopy    
    conda install cmocean

If already built:
    module load anaconda/5-2021
    conda activate /work/jelt/conda-env/ntslf_py39

To run:
    python create_gifs_outputs.py

Know issues:
    The disct_cmap option may not work perfectly.

"""


import matplotlib.pyplot as plt
import numpy as np
from numpy import pi
import matplotlib as mpl
import os
from math import cos, sin
import cartopy.crs as ccrs  # mapping plots
from cartopy.feature import NaturalEarthFeature
import xarray as xr
import datetime
from datetime import timezone
import pytz
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
import locale
import cmocean.cm as cmo

# To make sure you plot days of the week in english
locale.setlocale(locale.LC_ALL, 'en_GB')

plt.rcParams['svg.fonttype'] = 'none'

MIN_LAT = 46
MAX_LAT = 61
MIN_LON = -15
MAX_LON = 9.5

#################### INTERNAL FCTNS #########################

def dt64(now) -> np.datetime64:
    """ All the nano seconds can mess up conversions, so strip them out """
    return np.datetime64(np.datetime_as_string(now, unit="m"))

def get_am_pm(now) -> str:
    hour = now.astype(object).hour
    if (hour >= 12): return "pm"
    else: return "am"

def get_day(now) -> str:
    return now.astype(object).strftime('%a')

def to_localtime(now) -> np.datetime64:
    """ UTC --> np.datetime64(GMT/BST), str(GMT/BST) """
    datetime_obj_in = now.astype(object).replace(tzinfo=timezone.utc)
    datetime_obj_out = datetime_obj_in.astimezone(pytz.timezone("Europe/London"))
    if datetime_obj_out.dst() != datetime.timedelta(0,0): timezone_str = "BST"
    else: timezone_str = "GMT"
    return np.datetime64(datetime_obj_out.replace(tzinfo=None)), timezone_str

def clock(ax, now):
    plt.ylim(0,1)
    plt.xlim(0,1)
    ax.text(0.5, 1.1, get_day(now) + ":" + get_am_pm(now), horizontalalignment='center',
            fontsize=10)
    hour= now.astype(object).hour
    minute = now.astype(object).minute
    second = now.astype(object).second
    angles_h= pi/2 - 2*pi*hour/12-2*pi*minute/(12*60)-2*second/(12*60*60)
    angles_m= pi/2 - 2*pi*minute/60-2*pi*second/(60*60)
    hand_m_r = 0.45
    hand_h_r = 0.3
    ax.plot([0.5, 0.5 + hand_h_r*cos(angles_h)], [0.5, 0.5 + hand_h_r*sin(angles_h)],
            color="black", linewidth=4)
    ax.plot([0.5, 0.5 + hand_m_r*cos(angles_m)], [0.5, 0.5 + hand_m_r*sin(angles_m)],
            color="black", linewidth=2)
    ax.grid(False)
    plt.axis('off')
    return ax

def min_round_interval(vmin, vmax, nb_points, contain_vmin=False, contain_vmax = False):
    d_val = (vmax-vmin)/nb_points ; log10_d_val = np.floor(np.log10(d_val))
    d_val = round(d_val/(10**log10_d_val),0)*(10**log10_d_val)
    vmin_round = round(vmin/(10**log10_d_val),0)*(10**log10_d_val)
    interval = np.arange(vmin_round-d_val*contain_vmin, vmax+contain_vmax*d_val,d_val)

    return interval

# Defines ticks depending on the fromat asked by the user
def calc_list_coords(ax, format_ticks, nb_ticks, lim, xaxis):
    if nb_ticks is not None :
        #Usefull for very coarse grid and fine domain where we have only one lat
        if lim[0]!=lim[1] :
            list_coords = min_round_interval(
                lim[0],lim[1],nb_ticks, contain_vmin=True,contain_vmax=True)
        else : list_coords=[lim[0]]

    elif xaxis: 
        list_coords = ax.get_xticks()
    else: 
        list_coords = ax.get_yticks()

    if format_ticks is not None :
        list_coords = [('{0:'+format_ticks+'}').format(i) for i in list_coords]

    return np.asarray(list_coords).astype('float')

def create_geo_axes(lonbounds, latbounds,
                    fig=None, ax=None,
                    projection=ccrs.PlateCarree(),
                    data_crs=ccrs.PlateCarree()):
    """
    A routine for creating an axis for any geographical plot. Within the
    specified longitude and latitude bounds, a map will be drawn up using
    cartopy. Any type of matplotlib plot can then be added to this figure.

    Accommodates coordinate transforms from data's coordinates (data_crs) onto
    a new coordinate system (projection).

    For example:

    Example Useage
    ##############

        f,a = create_geo_axes(lonbounds, latbounds)
        sca = a.scatter(stats.longitude, stats.latitude, c=stats.corr,
                        vmin=.75, vmax=1,
                        edgecolors='k', linewidths=.5, zorder=100)
        f.colorbar(sca)
        a.set_title('SSH correlations \n Monthly PSMSL tide gauge vs CO9_AMM15p0',
                    fontsize=9)

    * Note: For scatter plots, it is useful to set zorder = 100 (or similar
            positive number)
    """

    # If no figure or ax is provided, create a new one
    if ax==None and fig==None:
        fig = plt.figure(figsize=(6,3.7))
        plt.subplots_adjust(top=0.975, bottom=0.020, left=0.095, right=0.89,
                            hspace=0.2, wspace=0.2)
        fig.clf()
        ax = fig.add_subplot(1, 1, 1, projection=projection)

    ax.set_extent([lonbounds[0], lonbounds[1], latbounds[0], latbounds[1]],
                  crs=data_crs)

    coast = NaturalEarthFeature(category="physical", facecolor=[0.9, 0.9, 0.9],
                                name="coastline", scale="50m")
    ax.add_feature(coast, edgecolor="gray")
    
    gl = ax.gridlines(
        crs=projection, linewidth=1, color='gray', alpha=0.35,
        linestyle='--')
    
    # Defines the yticks. Not that we use the ax extent, as it is the 
    # most updated ylim
    current_y_lim = ax.get_extent()[2:]
    gl.ylocator = mticker.FixedLocator(
        calc_list_coords(
            ax=ax, format_ticks=None, nb_ticks=4, 
            lim=current_y_lim, xaxis=False)
        )
    gl.left_labels=True
    gl.yformatter = LATITUDE_FORMATTER
    gl.ylabel_style = {'size': 14, 'color': 'k'}
    
    # X ticks are fine so we do not change them
    gl.bottom_labels=True
    gl.xformatter = LONGITUDE_FORMATTER
    gl.xlabel_style = {'size': 14, 'color': 'k'}
    
    return fig, ax


def make_gif(files, output, delay=100, repeat=True, **kwargs):
    """
    Uses imageMagick to produce an animated .gif from a list of
    picture files.
    """

    loop = -1 if repeat else 0
    os.system('convert -delay %d -loop %d %s %s'
              % (delay, loop, " ".join(files), output.replace(".gif","_final.gif")))

class Animate:
    def __init__(self,
                lon:xr.DataArray=None,
                lat:xr.DataArray=None,
                var:xr.DataArray=None,
                time:xr.DataArray=None,
                lon_bounds: [float, float] = None,
                lat_bounds: [float, float] = None,
                levels: list = [],
                suptitle_str = '',
                cbar_str:str="",
                cmap:str="PiYG_r",
                filename:str="",
                ofile_gif:str="",
                ofile_svg:str="",
                disct_cmap:bool=False,
                date_data_process:np.datetime64=np.datetime64("2007-01-01T01")
                 ):

        self.lon = lon
        self.lat = lat
        self.var = var
        self.time = time
        self.levels = levels
        self.suptitle_str = suptitle_str
        self.cbar_str = cbar_str
        self.cmap = cmap
        self.proj = ccrs.PlateCarree()  # coord sys for projected (displayed) data
        self.data_crs = ccrs.PlateCarree() # coord sys of data
        
        # Boolean to check if you want to use discrete cmap or not
        self.disct_cmap = disct_cmap
        
        # Date when we whant to start ploting the data 
        self.date_data_process = date_data_process

        self.filename = filename
        self.ofile_gif = ofile_gif
        self.ofile_svg = ofile_svg
        if lon_bounds == None: self.lon_bounds = [lon.min(), lon.max()]
        else: self.lon_bounds = lon_bounds
        if lat_bounds == None: self.lat_bounds = [lat.min(), lat.max()]
        else: self.lat_bounds = lat_bounds

        self.process()

    def process(self):
        files = []
        start_idx = np.argwhere(self.time.values == self.date_data_process)[0,0]
        for count in range(start_idx, len(self.time)):
            self.timestamp = np.datetime_as_string(dt64(self.time[count]), unit="m")
            f = self.make_frame(count=count, cmap=self.cmap) #cmap="PiYG_r")

            ## OUTPUT FIGURES - svg
            fname = self.ofile_svg.replace('.png', '_' + str(count).zfill(4) + '.png')
            print(str(count) + "/" + str(len(self.time)), fname)
            f.savefig(fname, bbox_inches='tight', pad_inches=0) # transparent=True,
            plt.close(f)

            files.append(fname)

        ## Make the animated gif and clean up the frame files
        make_gif(files, self.ofile_gif, delay=20)
        for f in files:
            os.remove(f)

        ## Make a backup copy of gif if the max surge is large enough
        if "surge_anom_latest" in self.ofile_gif and (self.var.max() > 1.0 or self.var.min() < -1.0):
            print(f'Backing up {self.ofile_gif}')
            os.system(f'cp {self.ofile_gif} {fig_dir + self.filename.replace(".nc", ".gif")}')


    def make_frame(self, count:int=0, cmap="PiYG_r"):
        if type(cmap) == str:
            cmap0 = mpl.colormaps.get_cmap(cmap)
        else: 
            cmap0 = cmap

        f, a = create_geo_axes(self.lon_bounds, self.lat_bounds,
                               projection=self.proj,
                               data_crs=self.data_crs)

        ## For disct_cmap: Contour fill surge + zero contour
        if self.disct_cmap: 
            sca = a.contourf(self.lon, self.lat, self.var[count,:,:],
                              levels=self.levels,
                              cmap=cmap0,
                              extend='both',
                              transform=self.data_crs)
        # Otherwise, pcolormesh
        else: 
            sca = a.pcolormesh(self.lon, self.lat, self.var[count,:,:],
                             cmap=cmap0, vmin=self.levels[0],
                             vmax=self.levels[-1],
                             transform=self.data_crs)

        ## title
        f.suptitle(self.suptitle_str, fontsize=16, y=0.97) # label

        ## Colorbar
        cbar_size=0.02
        cbar_pad = 0.01
        bb = a.get_position()
        # Bounds: x0, y0, width, height
        bounds_ax=bb.bounds
        pos_ax=bb.get_points()
        cax = f.add_axes(
            [pos_ax[1,0]+cbar_pad, pos_ax[0,1], cbar_size, bounds_ax[-1]])
        
        if self.disct_cmap:
            norm = mpl.colors.BoundaryNorm(self.levels, cmap0.N, extend='both')
            cbar=f.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap0),
                       cax=cax, orientation='vertical',
                       spacing='proportional')
        else: 
            cbar = plt.colorbar(
                mappable=sca, cax=cax, orientation = "vertical")
        
        
        cbar.set_label(self.cbar_str, rotation=90, fontsize=6)
        
        ## Clock
        dt64_now, timezone_str = to_localtime(dt64(self.time[count]))
        clock_ax = f.add_axes([0.77, 0.1, 0.1, 0.1], zorder=1)  ## mid lower right
        clock(clock_ax, dt64_now)

        ## snapshot timestamp.
        snapshot_timestamp = np.datetime_as_string(dt64_now, unit="m").replace('T', ' ')+" "+timezone_str
        a.annotate(snapshot_timestamp,
                   xy=(self.lon_bounds[1] - 0.1, 49.0),
                   xycoords = self.data_crs._as_mpl_transform(a),
                   fontsize=10,
                   horizontalalignment='right',
                   verticalalignment='bottom'
                   )
        
        return f

if __name__ == '__main__':
    fig_dir = "Figures/"
    example = 0
    
    # FIRST EXAMPLE: for the SSH:
    if example == 0:
        data_dir = f"{'/'.join(os.getcwd().split('/')[:-2])}/nemo_5.0.1/cfgs/AMM12_SURGE/EXP00"
        data_file = "AMM12_SURGE_1h_20120101_20120109_grid_T.nc"
        ds = xr.load_dataset(data_dir + data_file)
        time_var = "time_counter"
            
        # Coordinates and time variable
        lon_var = "nav_lon"
        lat_var = "nav_lat"
        var_lab = "zos"
        
        # Variable to plot
        var_lab_plot = "Sea Surface Height [m]"
        mult_fact = 1
        # Levels are [vmin,vmax] when not using disct_cmap
        levels = [-0.4, 0.4]
        cmap = "PiYG_r"
        
        save_lab = "AMM12_SURGE_SSH"
        
        # Starts after the spin-up period. But you can start earlier if you want to
        date_data_process = np.datetime64("2012-01-05T01")
    
    # SECOND EXAMPLE: for the atmospheric pressure
    if example == 1:
        # Define NEMO AMM12 SURGE run directory path:
        data_dir = f"{'/'.join(os.getcwd().split('/')[:-2])}/nemo_5.0.1/cfgs/AMM12_SURGE/EXP00/fluxes/"
        data_file = "amm12_surge_somslpre_y2012m01d*.nc"
        ds = xr.open_mfdataset(data_dir + data_file)
        
        lon_var = "nav_lon"
        lat_var = "nav_lat"
        time_var = "t"
        
        # Variable to plot
        var_lab = "somslpre"
        var_lab_plot = "Atmospheric pressure [hPa]"
        mult_fact = 1/100
        # Levels are [vmin,vmax] when not using disct_cmap
        levels = [985, 1009.918]
        cmap = cmo.matter
        
        save_lab = "AMM12_SURGE_atmpr"
        
        # Starts after the spin-up period. But you can start earlier if you want to
        # NOTE THAT IT IS LABELLED AS 2007 FORCING
        date_data_process = np.datetime64("2007-01-05T01")

    animate = Animate(lon=ds[lon_var],
                      lat = ds[lat_var],
                      var=ds[var_lab] * mult_fact,
                      time=ds[time_var],
                      lon_bounds=[MIN_LON, MAX_LON],
                      lat_bounds=[MIN_LAT, MAX_LAT],
                      levels=levels,
                      suptitle_str = var_lab_plot,
                      cbar_str = "",
                      cmap = cmap,
                      filename=data_dir + data_file,
                      ofile_svg=fig_dir + save_lab + '.png',
                      ofile_gif=fig_dir + save_lab + '.gif',
                      disct_cmap=False,
                      date_data_process = date_data_process)
