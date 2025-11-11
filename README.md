# UHI_Baltimore_EnergyMeteorology
Determining Current and Future UHI for Baltimore, MD
halpin-engineering/
├─ data/
│  ├─ station_raw/            # raw CSVs from Baltimore station
│  ├─ cmip_raw/               # raw .nc files you download manually (or small subset)
│  └─ processed/              # processed CSVs output by pipeline (time series, metrics)
├─ notebooks/
│  └─ exploratory.ipynb
├─ src/
│  ├─ fetch_instructions.md   # notes on how to get CMIP6 data (ESGF query)
│  ├─ process_station.py
│  ├─ process_cmip.py
│  ├─ bias_correction.py
│  └─ compute_uhi.py
├─ outputs/
│  ├─ timeseries_observed.csv
│  ├─ timeseries_model_corrected_ssp245.csv
│  ├─ uhi_metrics_summary.csv
│  └─ figures/
├─ css/, js/, index.html      # frontend visualization files
└─ README.md
