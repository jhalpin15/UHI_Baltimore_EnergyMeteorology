# src/process_station.py
import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path('../data')
RAW_DIR = DATA_DIR / 'station_raw'
OUT_DIR = DATA_DIR / 'processed'
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Adjust filenames/columns to match your station CSV.
# Expect columns: timestamp (ISO), temperature_C, station_id, lat, lon
def load_station(csv_path):
    df = pd.read_csv(csv_path, parse_dates=['timestamp'])
    df = df.set_index('timestamp').sort_index()
    return df

def daily_stats(df):
    # Compute daily mean, min, max
    daily = pd.DataFrame()
    daily['tmean'] = df['temperature_C'].resample('D').mean()
    daily['tmin'] = df['temperature_C'].resample('D').min()
    daily['tmax'] = df['temperature_C'].resample('D').max()
    return daily

if __name__ == '__main__':
    # change to your actual file
    csv_file = RAW_DIR / 'baltimore_station.csv'
    df = load_station(csv_file)
    daily = daily_stats(df)
    daily.to_csv(OUT_DIR / 'timeseries_observed.csv', index=True)
    print("Wrote:", OUT_DIR / 'timeseries_observed.csv')
