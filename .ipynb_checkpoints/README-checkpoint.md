[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/robfatland/ocean.git/HEAD)


# Introduction to the **ocean** GitHub repository

This [repository](https://github.com/robfatland/ocean) is a collection of Python Jupyter notebooks and supporting data. 
It is a learning resource for expanding on sensor data visualization in oceanography. There are two
driving emphases: Good dataset construction, and comparison of data from different types of sensors.
The latter is herein referred to as a 'synoptic view' of the water column.


Click the following link -- it may take a few minutes to initialize -- to create a *'binder'* sandbox version
of this repository. Once the binder environment appears in your browser, double-click
the **BioOptics** Jupyter notebook to view its contents. Additional work may be found in the **`Notebooks`** sub-folder.
You may experiment as you like with the binder contents as the environment is temporary.


To work from a copy of this repository: Establish a stable Jupyter notebook server environment 
and use `git clone`. 


The work here centers on **shallow profilers** located in the
[Regional Cabled Array (RCA)](https://interactiveoceans.washington.edu); 
in turn a large component of NSF's Ocean Observatories Initiative (OOI). 
Additional datasets are featured that originate in other programs 
([RCA cruise data](https://alfresco.oceanobservatories.org/), 
ARGO, 
MODIS and so on).


An RCA shallow profiler rests at a depth of 200 meters below the surface and transits the upper 
water column nine times per day. These nine excursions include two 
intervallic ('with pauses') profiles that accommodate equilibration of a pH sensor. 


<img src="https://github.com/robfatland/ocean/blob/main/Images/rca/shallow%20profiler%20platform%202%20OSB%20pool.png" alt="drawing" width="500"/>



## Structure of this Repository

- Overview: This **`README.md`** markdown file
- Primary BioOptics narrative: **`BioOptics.ipynb`** Jupyter notebook
- Subdirectories
    - **`Images`** are images from the project organized into categories
    - **`RepositoryData`** contains (smaller-sized) datasets
        - Contrasted with an external **`../data`** directory for larger datasets
    - **`Profiles`** contains metadata on the timing of shallow profiler ascent/descent/rest intervals
    - **`binder`** contains information on building sandbox versions of this repository using the [**binder**](https://mybinder.org) service


## Additional Notes


### Python and related libraries


The Jupyter notebooks in this repository include Python 3 code and refer to a set of common geospatial analysis libraries. These include
`dask`, `XArray`, `pandas`, `matplotlib`, and `numpy`. Timing is managed using the (**numpy**) datatime64 utility.



### How to create the binder feature for a GitHub repository


- Reduce the source data to a few Megabytes so it can reside in the repository
- Add a subfolder `binder` and an `environment.yml` file as shown given below
- Add a binder badge linking to this repo

Binder link: 

```
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/robfatland/ocean/HEAD)
```


Within the `binder` folder the `environment.yml` file reflects necessary libraries / packages: 


```
channels:
  - conda-forge
dependencies:
  - python=3
  - numpy
  - pandas
  - matplotlib
  - netcdf4
  - xarray
  - ffmpeg
```


### Configuration notes

* One may be obliged to `conda install dask`

