import os, sys, time, glob, warnings
from os.path import join as joindir
import numpy as np, pandas as pd, xarray as xr
from numpy import datetime64 as dt64, timedelta64 as td64

warnings.filterwarnings('ignore')


def ReformatDataFile(verbose=False):
    """Read a NetCDF and reformat it, write the result"""
    print('\n\nSpecify input NetCDF data file\n')

    dataLoc         = os.getcwd() + '/../../data/rca'
    osb             = 'OregonSlopeBase'
    oos             = 'OregonOffshore'
    axb             = 'AxialBase'
    sites_list      = [osb, oos, axb]
    plat            = 'platform'
    prof            = 'profiler'
    structures_list = [plat, prof]

    m = int(input('Site choice: Enter an index 0 1 2 for ' + str(sites_list)))
    n = int(input('Structure choice: Enter an index 0 1 for ' + str(structures_list)))

    resource_folder = joindir(dataLoc, sites_list[m], structures_list[n])
    s = [name for name in os.listdir(resource_folder) if os.path.isdir(joindir(resource_folder, name))]
    print(s)   # This will give PAR, ctd, do, etcetera
    instrument_folder = joindir(resource_folder, s[int(input('Enter index 0, 1, ... to select the instrument: '))])
    l = os.listdir(instrument_folder)
    print(l)
    ds = xr.open_dataset(joindir(instrument_folder, l[int(input('Enter index of NetCDF file to use'))]))

    if verbose: print(ds)
    print()
    print()
    print()

    # user can choose to swap one dimension
    ds_dims      = [i for i in ds.dims]
    ds_coords    = [i for i in ds.coords]
    ds_data_vars = [i for i in ds.data_vars]

    print('\n\nSwap the dimension (e.g. time in place of row or obs)\n')
    print('Dimensions: ' + str(ds_dims))
    print('Coordinates: ' + str(ds_coords))
    print('Data Variables: ' + str(ds_data_vars))

    old_dim = input('Dimension to swap out (need exact match):')
    if old_dim in ds_dims:
        new_dim = input('Coordinate or data variable to swap back in:')
        if new_dim in ds_data_vars or new_dim in ds_coords:
            ds = ds.swap_dims({old_dim:new_dim})

    if verbose: print(ds)

    print('\n\nRename, Drop or Retain Coordinates\n')
    ds_coords = [i for i in ds.coords]
    nC = str(len(ds_coords))
    print('For ' + nC + ' coordinates: 0 to drop, non-zero string to rename, enter to retain:\n')
    for c in ds_coords:
        print('coord name: ' + c)
        a = input('Drop (0), Rename or Keep: ')
        if   a == '0': ds = ds.drop(c)
        elif len(a):   ds = ds.rename({c:a})

    print('\n\nRename, Drop or Retain Data Variables\n')
    ds_data_vars = [i for i in ds.data_vars]
    nDV = str(len(ds_data_vars))
    print('For ' + nDV + ' data variables: 0 to drop, non-zero string to rename, enter to retain:\n')
    for dv in ds_data_vars:
        print('data variable name: ' + dv)
        a = input('Drop (0), Rename or Keep:')
        if   a == '0': ds = ds.drop(dv)
        elif len(a):   ds = ds.rename({dv:a})


    print('\n\nDrop all Attributes (less any you select)\n')
    ds_attrs_dict = ds.attrs.copy()
    for k in ds_attrs_dict: print(k + ' '*(40-len(k)) + str(ds_attrs_dict[k]))
    attrs_to_preserve = []
    print('Enter an attribute to preserve; or just enter by itself when done\n')
    while True:
        s = input('Preserve: ')
        if not len(s): break
        attrs_to_preserve.append(s)
    for key in ds_attrs_dict: 
        if key not in attrs_to_preserve: ds.attrs.pop(key)

    print('\n\nEnsure the new Dimension is sorted (no User action)\n')    
    df   = ds.to_dataframe()
    vals = [xr.DataArray(data=df[c], dims=['time'], coords={'time':df.index}, attrs=ds[c].attrs) for c in df.columns]
    ds  = xr.Dataset(dict(zip(df.columns, vals)), attrs=ds.attrs)

    
    print('\n\nSelect output time window (Format yyyy-mm-dd or enter to use the defaults)\n')
    t0_default, t1_default = '2022-01-01', '2022-02-01'
    t0 = input('start date (' + t0_default + ')')
    t1 = input('end date   (' + t1_default + ')')
    if not len(t0): t0 = t0_default
    if not len(t1): t1 = t1_default
    t0 = dt64(t0)
    t1 = dt64(t1)
    ds = ds.sel(time=slice(t0, t1))

    print('\n\nHere is the resulting dataset summary view:\n')
    print(ds)
    
    # bug: this plot needs plt.show()-style compulsion; it holds back
    # print("\n\ndepth quick look (assumes a 'z' coord/data variable:\n")
    # ds.z[0:10000].plot()

    outfnm = input('\n\nEnter an output file name. Include the .nc extension (or just enter to skip this): ')
    if len(outfnm): ds.to_netcdf(outfnm)    

    return True