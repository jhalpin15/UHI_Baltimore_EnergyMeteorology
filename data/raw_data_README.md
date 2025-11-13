Where raw data was downloaded from:

BWI Observed Data: https://www.ncei.noaa.gov/cdo-web/datasets/GHCND/stations/GHCND%3AUSW00093721/detail
Output Format: Custom GHCN-Daily CSV
Date Range: 1999-01-01 through 2014-12-31
Data Type: Air Temperature --> Average Temperature. (TAVG)

MD Science Center Obserbed Data: https://www.ncei.noaa.gov/cdo-web/datasets/LCD/stations/WBAN:93784/detail
Output Format: LCD CSV
Date Range: 1999-01-01 through 2014-12-31

CMIP Data:
https://nex-gddp-cmip6.s3.us-west-2.amazonaws.com/index.html#NEX-GDDP-CMIP6/CESM2/
Historical Data: historical/r4i1p1f1/tas/
*download all data from 1999-2014

SSP245 Data: ssp245/r4i1p1f1/tas/
*download all data from 2041-2060

SSP370 Data: ssp370/r4i1p1f1/tas/
*download all data from 2041-2060

Each corresponding file was run through CombineFiles.ipynb to output the following .nc files
Historical_NearSurface_CMIP_City.nc
Historical_NearSurface_BWI.nc
SSP245_NearSurface_City.nc
SSP245_NearSurface_BWI.nc
SSP370_NearSurface_City.nc
SSP370_NearSurface_BWI.nc
