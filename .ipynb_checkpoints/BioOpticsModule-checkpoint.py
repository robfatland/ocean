##################
#
# imports
#
##################

import os, sys, time, glob, warnings
from IPython.display import clear_output
warnings.filterwarnings('ignore')
this_dir = os.getcwd()  

from matplotlib import pyplot as plt
from matplotlib import colors as mplcolors
from matplotlib import animation, rc
import numpy as np, pandas as pd, xarray as xr
from numpy import datetime64 as dt64, timedelta64 as td64

from ipywidgets import *
from traitlets import dlink
from IPython.display import HTML, Video


##################
#
# parameter configuration
#
##################

# time ranges for midnight and noon profiles, adjusted for UTC
# midn0 - midn1 is a time range for the midnight profile start
# noon0 - noon1 is a time range for the noon profile start
midn0 = td64( 7*60 + 10, 'm')        # 7 hours 10 minutes
midn1 = td64( 7*60 + 34, 'm')        # 7 hours 34 minutes
noon0 = td64(20*60 + 30, 'm')        # 20 hours 30 minutes
noon1 = td64(20*60 + 54, 'm')        # 20 hours 54 minutes 

# global sensor range parameters for charting data: based on osb shallow profiler data

# axis ranges for a variety of sensors
par_lo,         par_hi           =   -10.0,      320.
nitrate_lo,     nitrate_hi       =     0.,        35.
do_lo,          do_hi            =    50.0,      300.
chlora_lo,      chlora_hi        =    -0.1,        1.2
temp_lo,        temp_hi          =     6.5,       11.
sal_lo,         sal_hi           =    31.5,       34.5
bb_lo,          bb_hi            =     0.0007,     0.0020
cdom_lo,        cdom_hi          =     0.6,        1.4
ph_lo,          ph_hi            =     7.6,        8.2
pco2_lo,        pco2_hi          =   200.0,     1200.0
si412_lo,       si412_hi         =     0.0,       80.0
si443_lo,       si443_hi         =     0.0,       80.0
si490_lo,       si490_hi         =     0.0,       80.0
si510_lo,       si510_hi         =     0.0,       80.0
si555_lo,       si555_hi         =     0.0,       80.0
si620_lo,       si620_hi         =     0.0,       15.0
si683_lo,       si683_hi         =     0.0,        6.0
veast_lo,       veast_hi         =    -0.4,        0.4
vnorth_lo,      vnorth_hi        =    -0.4,        0.4
vup_lo,         vup_hi           =    -0.4,        0.4

colorT = 'black'
colorS = 'xkcd:blood orange'
colorO = 'xkcd:blue'
colorA = 'xkcd:green'
colorB = 'xkcd:dark cyan'
colorC = 'red'
colorN = 'xkcd:gold'
colorP = 'magenta'
colorH = 'xkcd:purple blue'
colorR = 'xkcd:raspberry'

labelT = 'Temperature'
labelO = 'Oxygen'
labelS = 'Salinity'
labelA = 'Chlor-A'
labelB = 'Backscatter'
labelC = 'CDOM/FDOM'
labelN = 'Nitrate'
labelP = 'PAR'
labelH = 'pH'
labelR = 'pCO2'

optionsList = [labelO, labelT, labelS, labelA, labelB, labelC, labelN, labelP, labelH, labelR]


########################
#
# Functions and Configuration
#
########################


################
# convenience functions 
################
# abbreviating 'datetime64' and so on
################

def doy(theDatetime): return 1 + int((theDatetime - dt64(str(theDatetime)[0:4] + '-01-01')) / td64(1, 'D'))


def dt64_from_doy(year, doy): return dt64(str(year) + '-01-01') + td64(doy-1, 'D')


def day_of_month_to_string(d): return str(d) if d > 9 else '0' + str(d)


###########
# Plot function
###########
# Customized plot to show profiler behavior over one day
###########

def ShallowProfilerDepthOneDay(ds, t0str, t1str, title):
    
    ds_1day = ds.sel(time=slice(dt64(t0str), dt64(t1str)))
    
    fig, axs = plt.subplots(figsize=(12,4), tight_layout=True)
    
    axs.plot(ds_1day.time, ds_1day.z, marker='.', ms=9., color='k', mfc='r')
    
    axs.set(ylim = (-200., 0.), title=title)
    axs.text(dt64('2021-02-28 23:15'), -184, 'AT')
    axs.text(dt64('2021-02-28 23:05'), -193, 'REST')
    axs.text(dt64('2021-03-01 08'), -180, 'midnight')
    axs.text(dt64('2021-03-01 21:40'), -180, 'noon')
    axs.text(dt64('2021-03-01 09:25'), -60, 'slow')
    axs.text(dt64('2021-03-01 09:30'), -70, 'descent')

    axs.text(dt64('2021-03-01 00:12'), -150, 'A')
    axs.text(dt64('2021-03-01 00:17'), -135, 'S')
    axs.text(dt64('2021-03-01 00:22'), -120, 'C')
    axs.text(dt64('2021-03-01 00:27'), -105, 'E')
    axs.text(dt64('2021-03-01 00:32'), -90, 'N')
    axs.text(dt64('2021-03-01 00:37'), -75, 'D')
    axs.text(dt64('2021-03-01 00:42'), -60, ' I')
    axs.text(dt64('2021-03-01 00:47'), -45, 'N')
    axs.text(dt64('2021-03-01 00:52'), -30, 'G')

    axs.text(dt64('2021-03-01 01:50'), -30, 'D')
    axs.text(dt64('2021-03-01 01:52'), -43, 'E')
    axs.text(dt64('2021-03-01 01:54'), -56, 'S')
    axs.text(dt64('2021-03-01 01:56'), -69, 'C')
    axs.text(dt64('2021-03-01 01:58'), -82, 'E')
    axs.text(dt64('2021-03-01 02:00'), -95, 'N')
    axs.text(dt64('2021-03-01 02:02'), -108, 'D')
    axs.text(dt64('2021-03-01 02:04'), -121, 'I')
    axs.text(dt64('2021-03-01 02:06'), -134, 'N')
    axs.text(dt64('2021-03-01 02:08'), -147, 'G')

    plt.show()
    return
    
    
#################
# Time series metadata load function
#################
# Read in pre-processed profiler metadata for subsequent time-series subsetting.
# Shallow profiler metadata are timestamps for Ascent / Descent / Rest. These are stored 
#   as one-year-duration CSV files in the Profiles subfolder; are read into a Pandas 
#   Dataframe. Columns correspond to ascent start time and so on, as noted in the code.
#################

def ReadProfileMetadata(fnm):
    """
    Profiles are saved by site and year as 12-tuples. Here we read only
    the datetimes (not the indices) so there are only six values. These
    are converted to Timestamps. They correspond to ascend start/end, 
    descend start/end and rest start/end. Timestamps are a bit easier to
    use than datetime64 values, being essentially wrappers around the latter with
    additional utility.
    """
    pDf = pd.read_csv(fnm, usecols=["1", "3", "5", "7", "9", "11"])
    pDf.columns=['ascent_start', 'ascent_end', 'descent_start', 'descent_end', 'rest_start', 'rest_end']
    pDf['ascent_start']  = pd.to_datetime(pDf['ascent_start'])
    pDf['ascent_end']    = pd.to_datetime(pDf['ascent_end'])
    pDf['descent_start'] = pd.to_datetime(pDf['descent_start'])
    pDf['descent_end']   = pd.to_datetime(pDf['descent_end'])
    pDf['rest_start']    = pd.to_datetime(pDf['rest_start'])
    pDf['rest_end']      = pd.to_datetime(pDf['rest_end'])
    return pDf




#######################
# Time series metadata (index range) function
#######################
# Given a time range we want the indices of the profiles within.
#######################
def GenerateTimeWindowIndices(pDf, date0, date1, time0, time1):
    '''
    Given two day boundaries and a time window (UTC) within a day: Return a list
    of indices of profiles that start within both the day and time bounds. This 
    works from the passed dataframe of profile times.
    '''
    nprofiles = len(pDf)
    pIndices = []
    for i in range(nprofiles):
        a0 = pDf["ascent_start"][i]
        if a0 >= date0 and a0 <= date1 + td64(1, 'D'):
            delta_t = a0 - dt64(a0.date())
            if delta_t >= time0 and delta_t <= time1: pIndices.append(i)
    return pIndices


def ProfileEvaluation(t0, t1, pDf):
    '''
    At this time the profile metadata in pDf is broken up by year of interest and site.
    For example the code above concerns Oregon Slope Base (OSB) and the year 2021. 
    Only profiles through June are available.
    
    This function evaluates profiles within a given time range: How many profiles are there?
    How many 'local noon', how many 'local midnight'? This is a simple way to check profiler 
    operating consistency. This depends in turn on the profiler metadata reliability.
    '''
    global midn0, midn1, noon0, noon1
    
    nTotal = 0
    nMidn = 0
    nNoon = 0
    nNinePerDay = 0

    for i in range(len(pDf)):
            
        if pDf["ascent_start"][i] >= t0 and pDf["ascent_start"][i] <= t1:
            nTotal += 1
            
            if pDf["descent_end"][i] - pDf["descent_start"][i] >= td64(60, 'm'):
                
                tProf = pDf["ascent_start"][i]
                day_time = tProf - dt64(tProf.date())

                if   day_time > midn0 and day_time < midn1: nMidn += 1
                elif day_time > noon0 and day_time < noon1: nNoon += 1
                else: print("found a long descent that did not fit noon or midnight...")
        
    return nTotal, nMidn, nNoon




def GetProfileDataFrameIndicesForSomeTime(site, year, target, window):
    '''
    This is a convenience function that bundles the profile metadata read with the scan for
    profiles that match both a date window and a time-of-day window. The 'site' and 'year' 
    arguments are strings. The target is a target datetime; so we want the shallow profiler
    profile index that mostly closely matches it. 'window' is a +- window in minutes. This 
    code has two major flaws at the moment.
      - It will not work across day boundaries
      - It returns a list of suitable indices; so these must be sorted out by inspection
    '''
    pDf             = ReadProfileMetadata(os.getcwd() + "/./Profiles/" + site + year + ".csv")        
    t_date          = dt64(target.split('T')[0])                                        
    t_time          = target.split('T')[1].split(':')                                
    t_hrs, t_min    = int(t_time[0]), int(t_time[1])     
    t_early, t_late = td64(t_hrs*60 + t_min - window, 'm'), td64(t_hrs*60 + t_min + window, 'm')    
    return GenerateTimeWindowIndices(pDf, t_date, t_date, t_early, t_late), pDf



def GetDiscreteSummaryCastSubset(dsDf, cast, columns):
    '''
    dsDf is a Discrete Summary Dataframe
    cast is a string corresponding to the cast identifier, e.g. 'CTD-001'
    columns is a list of column names to extract from the full Dataframe
    Returns a Dataframe for 'just that cast' and 'just those parameters'
    '''
    return dsDf.loc[(dsDf['cast']==cast)][columns]



def ChartAB(pDf, xrng, pIdcs, A, Az, Albl, Acolor, B, Bz, Blbl, Bcolor, wid, hgt, \
            z0=-200., z1=0., legA='ascent', legB='ascent'):
    """
    Make a series of charts comparing two types of sensor data, A and B.
    The data are passed in as DataArrays: A and Az are data and z coordinates respectively.
    So A might be dsP.par (PAR DataArray) and depth Az would be dsP.z. Both use time as 
    their dimension. Charting is done over a set of passed profile indices pIdcs[].
    The number of profiles charted is constrained: Too many may bog down the kernel.
    """
    global midn0, midn1, noon0, noon1
        
    # if too many charts are requested: Take the first 117 only
    ncharts = len(pIdcs)
    if ncharts > 117: ncharts = 117
    print("Attempting", ncharts, "charts\n")

    # set up the requested number of charts in a vertical column
    fig, axs = plt.subplots(ncharts, 1, figsize=(wid, hgt*ncharts), tight_layout=True)

    # create a list of twin axes, one for each chart
    axstwin0 = [axs[i].twiny() for i in range(ncharts)]

    keyA0, keyA1 = legA + "_start", legA + "_end"
    keyB0, keyB1 = legB + "_start", legB + "_end"
            
    # this index i will range across the dataframe indices for ascent profiles
    for i in range(ncharts):
        
        # Need both a profile index into the profile dataframe pDf and a chart
        #   index 0, 1, 2, ... These are respectively pIdx and i
        pIdx = pIdcs[i]

        tA0, tA1 = pDf[keyA0][pIdx], pDf[keyA1][pIdx]
        tB0, tB1 = pDf[keyB0][pIdx], pDf[keyB1][pIdx]
        
        Ax, Ay = A.sel(time=slice(tA0,  tA1)), Az.sel(time=slice(tA0, tA1))
        Bx, By = B.sel(time=slice(tB0,  tB1)), Bz.sel(time=slice(tB0, tB1))
        
        axs[i].plot(Ax, Ay, ms = 4., color=Acolor, mfc=Acolor)
        axstwin0[i].plot(Bx, By, markersize = 4., color=Bcolor, mfc=Bcolor)
        
        # axis ranges
        if i == 0: axs[i].set(title = Albl + ' (' + Acolor + ', lower x-axis) and ' \
                                    + Blbl + ' (' + Bcolor + ', upper x-axis)')

        # Set axis ranges from passed list of pairs xrng[][]
        axs[i].set(     xlim = (xrng[0][0], xrng[0][1]), ylim = (z0, z1))
        axstwin0[i].set(xlim = (xrng[1][0], xrng[1][1]), ylim = (z0, z1))

        # chart timestamp (embellish for noon / midnight)
        #   bug: qualifier will fail if the 'A' data is not ascent-type (non-critical)
        ascent_start_time = 'Start UTC: ' + str(tA0)
        delta_t = tA0-dt64(tA0.date())
        if delta_t > midn0 and delta_t < midn1: ascent_start_time += " MIDNIGHT local"
        if delta_t > noon0 and delta_t < noon1: ascent_start_time += " NOON local"

        xlabel = xrng[0][0] + (xrng[0][1] - xrng[0][0])/2.
        axs[i].text(xlabel, -10., ascent_start_time)
        
    return fig, axs



# Load XArray Datasets from the smaller (intra-repo!) source files

def ReadOSB_March2021_1min():
    data_source = os.getcwd() + '/RepositoryData/rca/'
    return                                                                         \
        xr.open_dataset(data_source + 'fluor/osb_chlora_march2021_1min.nc'),       \
        xr.open_dataset(data_source + 'fluor/osb_backscatter_march2021_1min.nc'),  \
        xr.open_dataset(data_source + 'fluor/osb_cdom_march2021_1min.nc'),         \
        xr.open_dataset(data_source + 'ctd/osb_temp_march2021_1min.nc'),           \
        xr.open_dataset(data_source + 'ctd/osb_salinity_march2021_1min.nc'),       \
        xr.open_dataset(data_source + 'ctd/osb_doxygen_march2021_1min.nc'),        \
        xr.open_dataset(data_source + 'pH/osb_ph_march2021_1min.nc'),              \
        xr.open_dataset(data_source + 'irrad/osb_spectir_march2021_1min.nc'),      \
        xr.open_dataset(data_source + 'nitrate/osb_nitrate_march2021_1min.nc'),    \
        xr.open_dataset(data_source + 'par/osb_par_march2021_1min.nc'),            \
        xr.open_dataset(data_source + 'current/osb_veast_march2021_1min.nc'),      \
        xr.open_dataset(data_source + 'current/osb_vnorth_march2021_1min.nc'),     \
        xr.open_dataset(data_source + 'current/osb_vup_march2021_1min.nc'),        \
        xr.open_dataset(data_source + 'pCO2/osb_pco2_march2021.nc')

def ReadOSB_JuneJuly2018_1min():
    data_source = os.getcwd() + '/RepositoryData/rca/'
    return                                                                         \
        xr.open_dataset(data_source + 'fluor/osb_chlora_june_july2018_1min.nc'),       \
        xr.open_dataset(data_source + 'fluor/osb_backscatter_june_july2018_1min.nc'),  \
        xr.open_dataset(data_source + 'fluor/osb_cdom_june_july2018_1min.nc'),         \
        xr.open_dataset(data_source + 'ctd/osb_temp_june_july2018_1min.nc'),           \
        xr.open_dataset(data_source + 'ctd/osb_salinity_june_july2018_1min.nc'),       \
        xr.open_dataset(data_source + 'ctd/osb_doxygen_june_july2018_1min.nc'),        \
        xr.open_dataset(data_source + 'pH/osb_ph_june_july2018_1min.nc'),              \
        xr.open_dataset(data_source + 'irrad/osb_spectir_june_july2018_1min.nc'),      \
        xr.open_dataset(data_source + 'nitrate/osb_nitrate_june_july2018_1min.nc'),    \
        xr.open_dataset(data_source + 'par/osb_par_june_july2018_1min.nc'),            \
        xr.open_dataset(data_source + 'current/osb_veast_june_july2018_1min.nc'),      \
        xr.open_dataset(data_source + 'current/osb_vnorth_june_july2018_1min.nc'),     \
        xr.open_dataset(data_source + 'current/osb_vup_june_july2018_1min.nc')





def SixSignalChartSequence(df, dsA, dsB, dsC, dsO, dsS, dsT, xrng, chart_indices = [506]):
    """
    This chart sequence shows chlorophyll-a, FDOM, backscatter, temperature, dissolved oxygen 
    and salinity with depth. (Note: FDOM is the fluorometer proxy for CDOM; so the data product
    uses CDOM, an unfortunate point of confusion.) The six sensor types { temperature, salinity, 
    dissolved oxygen, chlorophyll-a, FDOM, backscatter } are separated into three 'two-per' charts 
    across each row to reduce visual clutter. The data are from shallow profiler ascents only as
    these introduce the sensors from below into undisturbed water. Which profiles to use are 
    indicated in the passed list 'chart_indices'. The default produces a single chart sequence 
    (profile 506) taken midnight-local March 1 2021. The number of profiles is constrained: 
    Too many may bog down the kernel. An improvement here would be to pass year and site values
    and include the appropriate corresponding profile metadata load operation.
    """
    
    # A B C O S T are datasets respectively chlor-A, backscatter, FDOM (CDOM), oxygen, salinity, temperature
    global midn0, midn1, noon0, noon1     # timedelta ranges
    
    ncharts = len(chart_indices)
    if ncharts > 117: ncharts = 117
    print("Attempting", ncharts, "chart sequences")

    fig, axs = plt.subplots(ncharts, 3, figsize=(15, 4*ncharts), tight_layout=True)

    axstwin0 = [axs[i][0].twiny() for i in range(ncharts)]
    axstwin1 = [axs[i][1].twiny() for i in range(ncharts)]
    axstwin2 = [axs[i][2].twiny() for i in range(ncharts)]


    for i in range(ncharts):

        # chart row index is i; profile index (dataframe df is OSB, 2021) is pIdx
        pIdx = chart_indices[i]

        ta0, ta1 = df["ascent_start"][pIdx], df["ascent_end"][pIdx]

        A = dsA.sel(time=slice(ta0,  ta1))
        B = dsB.sel(time=slice(ta0,  ta1))
        C = dsC.sel(time=slice(ta0,  ta1))
        O = dsO.sel(time=slice(ta0,  ta1))
        S = dsS.sel(time=slice(ta0,  ta1))
        T = dsT.sel(time=slice(ta0,  ta1))

        axs[i][0].plot(T.temp,        T.z, ms = 4., color=colorT, mfc=colorT)
        axstwin0[i].plot(S.salinity,  S.z, ms = 4., color=colorS, mfc=colorS)

        axs[i][1].plot(O.doxygen,     O.z, ms = 4., color=colorO, mfc=colorO)
        axstwin1[i].plot(A.chlora,    A.z, ms = 4., color=colorA, mfc=colorA)

        axs[i][2].plot(B.backscatter, C.z, ms = 4., color=colorB, mfc=colorB)
        axstwin2[i].plot(C.cdom,      C.z, ms = 4., color=colorC, mfc=colorC)
        
        # axis ranges
        if i == 0: 
            axs[i][0].set(title='Temperature (black) and Salinity (orange)')
            axs[i][1].set(title='Dissolved Oxygen (blue) and Chlorophyll (green)')
            axs[i][2].set(title='FDOM (aka CDOM: red) and Backscatter (cyan)')

        # Set axis ranges from passed list of pairs xrng[][]
        # Order is temp, salinity: left, DO, Chlor-A: center, backscatter, FDOM (CDOM): right 
        axs[i][0].set(xlim   = (xrng[0][0], xrng[0][1]), ylim = (-200., 0.))
        axstwin0[i].set(xlim = (xrng[1][0], xrng[1][1]), ylim = (-200., 0.))
        axs[i][1].set(xlim   = (xrng[2][0], xrng[2][1]), ylim = (-200., 0.))
        axstwin1[i].set(xlim = (xrng[3][0], xrng[3][1]), ylim = (-200., 0.))
        axs[i][2].set(xlim   = (xrng[4][0], xrng[4][1]), ylim = (-200., 0.))
        axstwin2[i].set(xlim = (xrng[5][0], xrng[5][1]), ylim = (-200., 0.))

        # labels
        ascent_start_time = str(ta0)
        delta_t = ta0-dt64(ta0.date())
        if delta_t > midn0 and delta_t < midn1: ascent_start_time += "\n local MIDNIGHT"
        if delta_t > noon0 and delta_t < noon1: ascent_start_time += "\n local NOON"

        axstwin0[i].text(xrng[1][0] + 0.8, -20., ascent_start_time)
        
        axs[i][0].text(xrng[0][1] - 0.6,   -75, 'Temp',   color=colorT)
        axstwin0[i].text(xrng[1][0] + 0.1, -75, 'Sal',    color=colorS)

        axs[i][1].text(xrng[2][1]-32,      -25, 'DO',      color=colorO)
        axstwin1[i].text(xrng[3][0]+0.05,  -25, 'Chl-A',   color=colorA)

        axs[i][2].text(xrng[4][1]-0.00020, -50, 'SCATT',   color=colorB)
        axs[i][2].text(xrng[4][1]-0.00022, -60, '(bb700)', color=colorB)
        axstwin2[i].text(xrng[5][0]+0.02,  -25, 'FDOM',    color=colorC)
        
    return fig, axs  


def BundleStatic(pDf, date0, date1, time0, time1, wid, hgt, color, x0, x1, y0, y1, dsXd, dsXz, title):
    pIdcs = GenerateTimeWindowIndices(pDf, date0, date1, time0, time1)
    nProfiles = len(pIdcs)
    fig, ax = plt.subplots(figsize=(wid, hgt), tight_layout=True)
    for i in range(nProfiles):
        ta0, ta1 = pDf["ascent_start"][pIdcs[i]], pDf["ascent_end"][pIdcs[i]]
        dsXx, dsXy = dsXd.sel(time=slice(ta0,  ta1)), dsXz.sel(time=slice(ta0, ta1))
        ax.plot(dsXx, dsXy, ms = 4., color=color, mfc=color)
        ax.set(title = title)
    ax.set(xlim = (x0, x1), ylim = (y0, y1))
    plt.show()
    return


def ShowStaticBundles():
    '''creates six bundle charts for March 2021, Oregon Slope Base'''
    BundleStatic(pDf21, dt64_from_doy(2021, 60), dt64_from_doy(2021, 91), td64(0, 'h'), td64(24, 'h'), 5, 4, \
                   colorO, do_lo, do_hi, -200, 0, dsO.doxygen, dsO.z, 'Oxygen')
    BundleStatic(pDf21, dt64_from_doy(2021, 60), dt64_from_doy(2021, 91), td64(0, 'h'), td64(24, 'h'), 5, 4, \
                   colorT, temp_lo, temp_hi, -200, 0, dsT.temp, dsT.z, 'Temperature')
    BundleStatic(pDf21, dt64_from_doy(2021, 60), dt64_from_doy(2021, 91), td64(0, 'h'), td64(24, 'h'), 5, 4, \
                   colorS, sal_lo, sal_hi, -200, 0, dsS.salinity, dsS.z, 'Salinity')
    BundleStatic(pDf21, dt64_from_doy(2021, 60), dt64_from_doy(2021, 91), td64(0, 'h'), td64(24, 'h'), 5, 4, \
                   colorA, chlora_lo, chlora_hi, -200, 0, dsA.chlora, dsA.z, 'Chlorophyll')
    BundleStatic(pDf21, dt64_from_doy(2021, 60), dt64_from_doy(2021, 91), td64(0, 'h'), td64(24, 'h'), 5, 4, \
                   colorC, cdom_lo, cdom_hi, -200, 0, dsC.cdom, dsC.z, 'Fluorescence')
    BundleStatic(pDf21, dt64_from_doy(2021, 60), dt64_from_doy(2021, 91), td64(0, 'h'), td64(24, 'h'), 5, 4, \
                   colorB, bb_lo, bb_hi, -200, 0, dsB.backscatter, dsB.z, 'Particulate Backscatter')
    return
    


def BundleInteract(choice, time_index, bundle_size):
    '''
    Consider a time range that includes many (e.g. 279) consecutive profiles. This function plots sensor data
    within the time range. Choose the sensor using a dropdown. Choose the first profile using the start slider.
    Choose the number of consecutive profiles to chart using the bundle slider. 
    '''
    global pDf21
    
    # this code sets up chart configuration based on choice of sensor
    if   choice == labelO: dsXv, dsXz, xlo, xhi, xtitle, xcolor = dsO.doxygen,     dsO.z, do_lo,      do_hi,      labelO, colorO
    elif choice == labelT: dsXv, dsXz, xlo, xhi, xtitle, xcolor = dsT.temp,        dsT.z, temp_lo,    temp_hi,    labelT, colorT
    elif choice == labelS: dsXv, dsXz, xlo, xhi, xtitle, xcolor = dsS.salinity,    dsS.z, sal_lo,     sal_hi,     labelS, colorS
    elif choice == labelA: dsXv, dsXz, xlo, xhi, xtitle, xcolor = dsA.chlora,      dsA.z, chlora_lo,  chlora_hi,  labelA, colorA
    elif choice == labelB: dsXv, dsXz, xlo, xhi, xtitle, xcolor = dsB.backscatter, dsB.z, bb_lo,      bb_hi,      labelB, colorB
    elif choice == labelC: dsXv, dsXz, xlo, xhi, xtitle, xcolor = dsC.cdom,        dsC.z, cdom_lo,    cdom_hi,    labelC, colorC
    elif choice == labelN: dsXv, dsXz, xlo, xhi, xtitle, xcolor = dsN.nitrate,     dsN.z, nitrate_lo, nitrate_hi, labelN, colorN
    elif choice == labelP: dsXv, dsXz, xlo, xhi, xtitle, xcolor = dsP.par,         dsP.z, par_lo,     par_hi,     labelP, colorP
    elif choice == labelH: dsXv, dsXz, xlo, xhi, xtitle, xcolor = dsH.ph,          dsH.z, ph_lo,      ph_hi,      labelH, colorH
    elif choice == labelR: dsXv, dsXz, xlo, xhi, xtitle, xcolor = dsR.pco2,        dsR.z, pco2_lo,    pco2_hi,    labelR, colorR
    else: return 0

    # This configuration code block is hardcoded to work with March 2021
    date0, date1   = dt64_from_doy(2021, 60), dt64_from_doy(2021, 91)
    time0, time1   = td64(0, 'h'), td64(24, 'h')
    wid, hgt       = 9, 5
    x0, x1, y0, y1 = xlo, xhi, -200, 0
    title          = xtitle
    color          = xcolor
    pIdcs          = GenerateTimeWindowIndices(pDf21, date0, date1, time0, time1)
    nProfiles      = len(pIdcs)

    # ad hoc locations on respective charts for text giving time range of current bundle
    pxpy           = { labelO: (60, -25), labelT: (6.8, -25), labelS: (33.5, -25),    \
                       labelA: (0.7, -150), labelB: (.0017, -70), labelC: (.65, -175),    \
                       labelN: (23, -25), labelP: (150, -75), labelH: (7.65, -25),    \
                       labelR: (900, -25) }
    px, py         = pxpy[choice]
    
    fig, ax = plt.subplots(figsize=(wid, hgt), tight_layout=True)
    iProf0 = time_index if time_index < nProfiles else nProfiles
    iProf1 = iProf0 + bundle_size if iProf0 + bundle_size < nProfiles else nProfiles
    for i in range(iProf0, iProf1):
        pIdx = pIdcs[i]
        if choice == labelH or choice == labelR:
            ta0, ta1 = pDf21["descent_start"][pIdx], pDf21["descent_end"][pIdx]
        else:
            ta0, ta1 = pDf21["ascent_start"][pIdx], pDf21["ascent_end"][pIdx]
        dsXsensor, dsXdepth = dsXv.sel(time=slice(ta0,  ta1)), dsXz.sel(time=slice(ta0, ta1))
        ax.plot(dsXsensor, dsXdepth, ms = 4., color=color, mfc=color)
    ax.set(title = title)
    ax.set(xlim = (x0, x1), ylim = (y0, y1))

    # Add text indicating the current time range of the profile bundle
    tString = str(pDf21["ascent_start"][pIdcs[iProf0]])
    if iProf1 - iProf0 > 1: tString += '\n ...through... \n' + str(pDf21["ascent_start"][pIdcs[iProf1-1]])
    ax.text(px, py, tString)
    
    plt.show()
    return



def Interactor():
    '''Set up three bundle-interactive charts, vertically. Independent sliders for choice of 
    sensor, starting profile by index, and number of profiles in bundle. (90 profiles is about
    ten days.)
    '''
    style = {'description_width': 'initial'}
    interact(BundleInteract, choice = widgets.Dropdown(options=optionsList,  value=labelT, description='sensor'), \
                             time_index = widgets.IntSlider(min=0, max=270, step=1, value=188,                    \
                                                            layout=widgets.Layout(width='35%'),                   \
                                                            continuous_update=True, description='bundle start',  \
                                                            style=style),
                             bundle_size = widgets.IntSlider(min=1, max=90, step=1, value=18,                     \
                                                            layout=widgets.Layout(width='35%'),                   \
                                                            continuous_update=True, description='bundle width',  \
                                                            style=style))

    interact(BundleInteract, choice = widgets.Dropdown(options=optionsList, value=labelO, description='sensor'),  \
                             time_index = widgets.IntSlider(min=0, max=270, step=1, value=188,                    \
                                                            layout=widgets.Layout(width='35%'),                   \
                                                            continuous_update=True, description='bundle start',  \
                                                            style=style),
                             bundle_size = widgets.IntSlider(min=1, max=90, step=1, value=18,                     \
                                                            layout=widgets.Layout(width='35%'),                   \
                                                            continuous_update=True, description='bundle width',  \
                                                            style=style))

    interact(BundleInteract, choice = widgets.Dropdown(options=optionsList, value=labelS, description='sensor'),  \
                             time_index = widgets.IntSlider(min=0, max=270, step=1, value=188,                    \
                                                            layout=widgets.Layout(width='35%'),                   \
                                                            continuous_update=True, description='bundle start',  \
                                                            style=style),                                         \
                             bundle_size = widgets.IntSlider(min=1, max=90, step=1, value=18,                     \
                                                            layout=widgets.Layout(width='35%'),                   \
                                                            continuous_update=True, description='bundle width',  \
                                                            style=style))
    return


def NitrateStaggerChart():
    '''Another visualization method: like fanning a deck of cards'''
    pIdcsMidn = GenerateTimeWindowIndices(pDf21, dt64_from_doy(2021, 60), dt64_from_doy(2021, 91), midn0, midn1)   # 30
    pIdcsNoon = GenerateTimeWindowIndices(pDf21, dt64_from_doy(2021, 60), dt64_from_doy(2021, 91), noon0, noon1)   # 31
    pIdcs = pIdcsMidn + pIdcsNoon
    pIdcs.sort()
    nProfiles = len(pIdcs)
    print(str(nProfiles) + " profiles (noon/midnight only) in March 2021")
    profile_shift   = 50
    nitrate_stretch = 10
    colorwheel = ['k', 'r', 'y', 'g', 'c', 'b', 'm']
    cwmod = len(colorwheel)
    nitrate_lower_bound = 20
    nitrate_upper_bound = nitrate_lower_bound + (nProfiles - 1)*profile_shift + 250
    fig, ax = plt.subplots(figsize=(12,7), tight_layout=True)
    for i in range(len(pIdcs)):
        ta0, ta1 = pDf21["ascent_start"][pIdcs[i]], pDf21["ascent_end"][pIdcs[i]]
        Nx, Ny = dsN.nitrate.sel(time=slice(ta0,  ta1)), dsN.z.sel(time=slice(ta0, ta1))
        ax.plot(nitrate_stretch * Nx + i * profile_shift, Ny, ms = 4., color=colorwheel[i%cwmod] , mfc=colorwheel[i%cwmod])
    ax.set(xlim = (nitrate_lower_bound, nitrate_upper_bound), \
           ylim = (-200., 0.),                                \
           title='staggered nitrate concentration')
    plt.show()
    return


##################
# more parameter configuration
##################
# Load the 2021 Oregon Slope Base profile metadata; and some March 2021 sensor datasets
##################

# Note these are profile times for Axial Base
pDf21 = ReadProfileMetadata(os.getcwd()+"/Profiles/osb2021.csv")

# Some code to test out the above ProfileEvaluation() function
t0, t1 = dt64('2021-01-01'), dt64('2021-02-01')
nDays = (t1 - t0).astype(int)
nTotal, nMidn, nNoon = ProfileEvaluation(t0, t1, pDf21)

print("For 2021, month of January, we have...")
print(nDays, 'days or', nDays*9, 'possible profiles')
print("There were, over this time, in fact...")
print(nTotal, 'profiles;', nMidn, 'at local midnight and', nNoon, 'at local noon')

dsA, dsB, dsC, dsT, dsS, dsO, dsH, dsI, dsN, dsP, dsU, dsV, dsW, dsR = ReadOSB_March2021_1min()

# Having loaded the data we drop extraneous data variables that were missed to this point

dsO = dsO.drop('moles_of_oxygen_per_unit_mass_in_sea_water_profiler_depth_enabled_qc_agg')
dsT = dsT.drop('sea_water_temperature_profiler_depth_enabled_qc_agg')
dsS = dsS.drop('sea_water_practical_salinity_profiler_depth_enabled_qc_agg')

# ...and then apply the .dropna() to eliminate NaNs

dsA = dsA.dropna('time')
dsB = dsB.dropna('time')
dsC = dsC.dropna('time')
dsT = dsT.dropna('time')
dsS = dsS.dropna('time')
dsO = dsO.dropna('time')
dsH = dsH.dropna('time')
dsI = dsI.dropna('time')
dsN = dsN.dropna('time')
dsP = dsP.dropna('time')
dsU = dsU.dropna('time')
dsV = dsV.dropna('time')
dsW = dsW.dropna('time')
dsR = dsR.dropna('time')