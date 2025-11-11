# src/process_cmip.py
import xarray as xr
import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path('../data')
CMIP_RAW = DATA_DIR / 'cmip_raw'
OUT_DIR = DATA_DIR / 'processed'
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Replace with the latitude/longitude of your station (Decimal degrees)
STATION_LAT = 39.2904
STATION_LON = -76.6122

def select_nearest(ds, lat, lon):
    # ensure lon coordinates are -180..180; convert if necessary
    if ds.lon.max() > 180:
        ds = ds.assign_coords(lon=(((ds.lon + 180) % 360) - 180))
    # select nearest
    da = ds.sel(lat=lat, lon=lon, method='nearest')
    return da

def process_file(ncpath, varname='tas'):
    ds = xr.open_dataset(ncpath)
    da = ds[varname]
    sel = select_nearest(da, STATION_LAT, STATION_LON)
    # convert to pandas time series (daily)
    # CMIP usually uses time in np.datetime64
    # Convert units K -> C if value > 100 (naive check)
    if sel.mean() > 120:
        sel = sel - 273.15
    ts = sel.to_series()
    daily = ts.resample('D').mean()
    return daily

if __name__ == '__main__':
    # Put your CMIP .nc files in data/cmip_raw/
    # Filenames might be like: gfdl-esm4_historical_tas.nc, gfdl-esm4_ssp245_tas.nc ...
    files = {
        'historical': CMIP_RAW / 'gfdl-esm4_historical_tas.nc',
        'ssp245': CMIP_RAW / 'gfdl-esm4_ssp245_tas.nc',
        'ssp370': CMIP_RAW / 'gfdl-esm4_ssp370_tas.nc'
    }
    for name, path in files.items():
        if not path.exists():
            print("File missing:", path)
            continue
        daily = process_file(path)
        out = OUT_DIR / f'timeseries_model_{name}.csv'
        daily.to_csv(out, header=['tas_C'])
        print("Wrote:", out)
