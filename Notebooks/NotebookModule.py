# This is a first draft of a **derivative** subset of the main directory Module.py file
#   ...Modification to path to accommodate being one level deeper
#   ...Add functions but flag them as unique to here




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

labelT = 'Temperature'
labelO = 'Oxygen'
labelS = 'Salinity'
labelA = 'Chlor-A'
labelB = 'Backscatter'
labelC = 'CDOM/FDOM'
labelN = 'Nitrate'
labelP = 'PAR'
labelH = 'pH'

optionsList = [labelO, labelT, labelS, labelA, labelB, labelC, labelN, labelP]


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


# Load XArray Datasets from the smaller (intra-repo!) source files

def ReadOSB_March2021_1min():
    data_source = os.getcwd() + '/../RepositoryData/rca/'
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
        xr.open_dataset(data_source + 'current/osb_vup_march2021_1min.nc')


def ReadOSB_JuneJuly2018_1min():
    data_source = os.getcwd() + '/../RepositoryData/rca/'
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








##################
# more parameter configuration
##################
# Load the 2021 Oregon Slope Base profile metadata; and some March 2021 sensor datasets
##################

# Note these are profile times for Axial Base
pDf21 = ReadProfileMetadata(os.getcwd()+"/../Profiles/osb2021.csv")

# Some code to test out the above ProfileEvaluation() function
t0, t1 = dt64('2021-01-01'), dt64('2021-02-01')
nDays = (t1 - t0).astype(int)
nTotal, nMidn, nNoon = ProfileEvaluation(t0, t1, pDf21)

print("For 2021, month of January, we have...")
print(nDays, 'days or', nDays*9, 'possible profiles')
print("There were, over this time, in fact...")
print(nTotal, 'profiles;', nMidn, 'at local midnight and', nNoon, 'at local noon')

dsA, dsB, dsC, dsT, dsS, dsO, dsH, dsI, dsN, dsP, dsU, dsV, dsW = ReadOSB_March2021_1min()