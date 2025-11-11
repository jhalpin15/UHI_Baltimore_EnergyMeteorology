# src/bias_correction.py
import pandas as pd
import numpy as np
from pathlib import Path
from scipy.interpolate import interp1d

DATA_DIR = Path('../data')
PROC = DATA_DIR / 'processed'

def delta_correct(obs_baseline, model_hist, model_future):
    # obs_baseline: pandas Series (daily) observed baseline period
    # model_hist: model historical daily (same baseline period)
    # model_future: model future daily (future period)
    # delta: model_future.mean - model_hist.mean (per calendar month or overall)
    # We'll do monthly deltas
    md_hist_monthly = model_hist.groupby(model_hist.index.month).mean()
    md_fut_monthly = model_future.groupby(model_future.index.month).mean()
    delta_monthly = md_fut_monthly - md_hist_monthly
    # apply delta to observed baseline climatology to generate future projection
    # For each date in model_future, map its month and add delta to the observed baseline climatology for that month
    obs_clim_monthly = obs_baseline.groupby(obs_baseline.index.month).mean()
    # Build corrected series with same index as model_future
    corrected = model_future.copy() * np.nan
    for date in model_future.index:
        m = date.month
        corrected.loc[date] = obs_clim_monthly.loc[m] + (md_fut_monthly.loc[m] - md_hist_monthly.loc[m])
    return corrected

def quantile_map(obs_hist, model_hist, model_future, nquantiles=100):
    """
    Simple empirical quantile mapping: for each calendar month,
    map model_hist quantiles to obs_hist quantiles, then apply mapping to model_future.
    """
    corrected = model_future.copy() * np.nan
    for month in range(1,13):
        obs_m = obs_hist[obs_hist.index.month==month].dropna()
        mod_hist_m = model_hist[model_hist.index.month==month].dropna()
        mod_fut_m = model_future[model_future.index.month==month].dropna()
        if len(obs_m) < 10 or len(mod_hist_m) < 10:
            # fallback to monthly mean delta
            mean_delta = mod_fut_m.mean() - mod_hist_m.mean() if len(mod_fut_m)>0 and len(mod_hist_m)>0 else 0
            corrected.loc[mod_fut_m.index] = obs_m.mean() + mean_delta
            continue

        # empirical CDF
        q = np.linspace(0,1,nquantiles)
        mod_hist_q = np.quantile(mod_hist_m, q)
        obs_q = np.quantile(obs_m, q)

        # function mapping model value -> quantile (inverse CDF)
        # build monotonic interpolation from mod_hist_q to obs_q
        # since quantiles might have repeated values, we make them strictly increasing for interp
        # ensure monotonic increase:
        eps = 1e-6
        mod_hist_q_mon = np.maximum.accumulate(mod_hist_q + (np.arange(len(mod_hist_q))*eps))
        f = interp1d(mod_hist_q_mon, obs_q, bounds_error=False, fill_value=(obs_q[0], obs_q[-1]))
        # apply mapping
        mapped = f(mod_fut_m.values)
        corrected.loc[mod_fut_m.index] = mapped
    return corrected

if __name__ == '__main__':
    obs = pd.read_csv(PROC / 'timeseries_observed.csv', index_col=0, parse_dates=True)
    mod_hist = pd.read_csv(PROC / 'timeseries_model_historical.csv', index_col=0, parse_dates=True)
    mod_fut = pd.read_csv(PROC / 'timeseries_model_ssp245.csv', index_col=0, parse_dates=True)

    # Define baseline period (e.g. 1995-2014). Adjust to your availability:
    baseline_mask = (obs.index.year >= 1995) & (obs.index.year <= 2014)
    obs_baseline = obs.loc[baseline_mask, 'tmean']

    # align model hist baseline to same period (truncate)
    # Ensure series are same freq
    mod_hist = mod_hist['tas_C']
    mod_fut = mod_fut['tas_C']

    # Trim model_hist to baseline years (choose same years)
    mod_hist_baseline = mod_hist[(mod_hist.index.year >= 1995) & (mod_hist.index.year <= 2014)]

    corrected_delta = delta_correct(obs_baseline, mod_hist_baseline, mod_fut)
    corrected_qm = quantile_map(obs_baseline, mod_hist_baseline, mod_fut)

    corrected_delta.to_csv(PROC / 'model_corrected_ssp245_delta.csv', header=['tas_C'])
    corrected_qm.to_csv(PROC / 'model_corrected_ssp245_qm.csv', header=['tas_C'])
    print("Wrote corrected CSVs.")
