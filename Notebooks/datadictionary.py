# A data dictionary is constructed so as to do all the "raw --> useable" steps in one go.
# This includes:
#   - Reduce the data range to a time window t0 - t1
#   - Make the dimension 'time'
#   - ...
#   - Save the results as a .nc file inside the repo
#
# Dictionary format
#   { 'timerange': ['t0', 't1'],
#     'nSites': n, 
#     'site folder 1':
#        ['instrument folder 1':
#            ['sensor name 1 (ctd, fluor etc)', 
#                'source abbreviation',
#                number of independent data streams (1, 2, 7 etc),
#                data stream index (0),  
#                    ['datavar', 'rename value', 'abbrev', lo, hi, color1, color2], 
#                data stream index (1),  
#                    ['datavar', 'rename value', 'abbrev', lo, hi, color], 
#        'instrument folder 2':
#     'site folder 2':
#   }

```
Short   Data                  Renamed       Instrument     Runs
-----   ----                  -------       ----------     -----------
A       Chlorophyll-A         chlora        fluorometer    continuous
B       backscatter           backscatter                  continuous
C       CDOM                  cdom                         continuous
E[]     Spectrophotometer     spec          spec           ? (83 channels)
G       pCO2                  pco2          pCO2           midnight/noon descent
H       pH                    ph            pH             midnight/noon descent
I[]     Spectral Irradiance 1 oa            spkir-oa       ? (7 channels)
J[]     Spectral Irradiance 2 ba            spkir-ba       ? (7 channels)
K       Density               density       CTD            continuous
M       Nitrate 1             ?             nitrate        midnight/noon ascent
N       Nitrate 2             ?                            midnight/noon ascent
O       dissolved oxygen      doxygen                      continuous
P       PAR                   par           PAR            continuous
Q       pressure              pressure      CTD            continuous
S       salinity              salinity                     continuous
T       temperature           temp                         continuous
U       velocity east         veast         current        continuous:
V       velocity north        vnorth                           from platform
W       velocity up           vup                              looking up
```

def ddict():
    return \ 
        { 'timerange': ['t0string', 't1string'],
          'nSites': 1,
          
          '/../../data/rca/sf01_OregonSlopeBase/':
             ['PAR', 
                 ['PAR', 2, 
                     [0, 'par_of_the_par_on_par', 'par', 'P', -10, 320, 'magenta', 'xkcd:barbie pink'],
                     [1, 'z_of_depthness',          'z', 'z', -300, 20, 'k', 'k']
                 ]
             ],
             ['CTD',  
                 ['ctd', 6,
                   [0, 'xxxx',      'density',   'K', -10, 320, 'magenta', 'xkcd:barbie pink']
                   [1, 'xxxx',  'temperature',   'T',  -4, 100, 'magenta', 'xkcd:barbie pink']
                   [2, 'xxxx',     'salinity',   'S',  22,  40, 'magenta', 'xkcd:barbie pink']
                   [3, 'xxxx',       'oxygen',   'O',  50, 300, 'magenta', 'xkcd:barbie pink']
                   [4, 'xxxx', 'conductivity', 'Sie', -10, 320, 'magenta', 'xkcd:barbie pink']
                   [5, 'xxxx',            'z',   'z', -10, 320, 'magenta', 'xkcd:barbie pink']
                 ]
             ],
             ['fluor', ['fluor', ]
              'nitrate', []
              'pCO2', []
              'pH', []
              'spkir', []
              'current', []
             ]
          '/../../data/rca/sf03_AxialBase/':
             ['PAR',
              'ctd',
              'fluor',
              'nitrate',
              'pCO2',
              'pH',
              'spkir',
          '/../../data/rca/xxxx_OregonOffshore/':
             ['PAR',
              'ctd',
              'fluor',
              'nitrate',
              'pCO2',
              'pH',
              'spkir']
        } 
              
              
              
```
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

colorTd = 'grey'
colorSd = 'xkcd:yellow orange'
colorOd = 'xkcd:azure'
colorAd = 'xkcd:pale green'
colorBd = 'xkcd:light turquoise'
colorCd = 'xkcd:pinkish'
colorNd = 'xkcd:brownish yellow'
colorPd = 'xkcd:barbie pink'
colorHd = 'xkcd:pastel purple'

labelT = 'Temperature'
labelO = 'Oxygen'
labelS = 'Salinity'
labelA = 'Chlor-A'
labelB = 'Backscatter'
labelC = 'CDOM/FDOM'
labelN = 'Nitrate'
labelP = 'PAR'
labelH = 'pH'
```