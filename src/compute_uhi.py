# src/compute_uhi.py
import pandas as pd
from pathlib import Path
DATA_DIR = Path('../data')
PROC = DATA_DIR / 'processed'
OUT = Path('../outputs')
OUT.mkdir(parents=True, exist_ok=True)

def compute_daily_uhi(urban_series, rural_series=None, baseline_mean=None):
    # If rural_series provided: uhi = urban - rural (daily)
    # Else: uhi = urban - baseline_mean (daily anomaly)
    if rural_series is not None:
        uhi = urban_series - rural_series
    else:
        if baseline_mean is None:
            baseline_mean = urban_series[(urban_series.index.year>=1995)&(urban_series.index.year<=2014)].mean()
        uhi = urban_series - baseline_mean
    return uhi

def summarize_uhi(uhi_series):
    # summary metrics: mean, median, 90th percentile of daily UHI; change in #hot nights
    summary = {}
    summary['mean_uhi'] = uhi_series.mean()
    summary['median_uhi'] = uhi_series.median()
    summary['p90_uhi'] = uhi_series.quantile(0.9)
    # hot nights count example: nights where tmin > 25C (if uhi measured on tmin)
    return summary

if __name__ == '__main__':
    obs = pd.read_csv(PROC / 'timeseries_observed.csv', index_col=0, parse_dates=True)
    obs_tmean = obs['tmean']

    # corrected model outputs (take QM result) - example
    model_corr = pd.read_csv(PROC / 'model_corrected_ssp245_qm.csv', index_col=0, parse_dates=True)['tas_C']

    # compute UHI relative to baseline mean
    baseline_mean = obs_tmean[(obs_tmean.index.year>=1995)&(obs_tmean.index.year<=2014)].mean()
    uhi_obs = compute_daily_uhi(obs_tmean, baseline_mean=baseline_mean)
    uhi_model_fut = compute_daily_uhi(model_corr, baseline_mean=baseline_mean)

    # summarize
    sum_obs = summarize_uhi(uhi_obs)
    sum_fut = summarize_uhi(uhi_model_fut)

    df_sum = pd.DataFrame([sum_obs, sum_fut], index=['observed_baseline','ssp245_qm_2050'])
    df_sum.to_csv(OUT / 'uhi_metrics_summary.csv')
    print("Wrote summary:", OUT / 'uhi_metrics_summary.csv')

    # Save time series for plotting on web
    uhi_obs.to_csv(PROC / 'uhi_obs_daily.csv', header=['uhi_C'])
    uhi_model_fut.to_csv(PROC / 'uhi_ssp245_qm_daily.csv', header=['uhi_C'])
    print("Wrote daily UHI time series.")
