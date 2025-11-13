# Determining Current and Future Urban Heat Island (UHI) for Baltimore, MD

### Author
Jenna Halpin  
Johns Hopkins University | Civil and Systems Engineering | Fall 2025  

---

## Project Overview
This project determines the **current Baltimore Urban Heat Island (UHI)** and uses both local weather data and data from the **Climate Model Intercomparison Project (CMIP)** to estimate the **impact of climate change on the Baltimore UHI in 2050**.

### Research Objective
> Evaluate how well CMIP historical simulations capture the observed temperature patterns at urban and rural stations near Baltimore, and estimate the regional-scale bias in representing the Baltimore UHI.

---

## Data and Model Information

### Experiments Used
- **Historical**
- **SSP2-4.5:** Medium-level projection assuming moderate global mitigation efforts  
- **SSP3-7.0:** High-emission projection assuming limited mitigation actions

### Variable
- Near-surface air temperature (`tas`)

### Climate Model
- **NASA Earth Exchange Global Daily Downscaled Projections (NEX-GDDP-CMIP6)** dataset  
  - Provides finer spatial resolution suitable for regional-scale climate analysis.

### Observed Data
- Source: **NOAA National Centers for Environmental Information (NCEI)**
- Stations: Urban (Baltimore City) and Rural (BWI Airport)
- Date Range: **1999-01-14 through 2017-01-14** (subset 1999–2014 used for CMIP overlap)

### Projected Data
- CMIP6 Scenarios: `ssp245` and `ssp370`
- Date Range: **2041–2060**

---

## Methods and Workflow

1. **Classify Current UHI**
   - Calculate temperature differences between city and rural stations.
2. **Verify and Compare with CMIP Historical Data**
   - Evaluate how well CMIP historical simulations replicate observed UHI magnitudes and variability.
3. **Bias Correction**
   - Apply correction methods to align CMIP data with observed station data.
4. **Future Projections**
   - Apply bias-corrected models to future scenarios (SSP2-4.5 and SSP3-7.0).
5. **Visualization**
   - Generate time-series plots, bias correction figures, and projected UHI maps.

---

## Initial Hypothesis
In 2050, under both CMIP scenarios, the Baltimore UHI will **increase significantly** due to higher background temperatures and the **diminishing effectiveness of current cooling mitigation strategies** under elevated climate conditions.

---

## Results and Visuals
All graphs, data cleaning steps, and analysis are presented in the notebook below:

**[View Full Notebook with Graphs (index.html)](https://jhalpin15.github.io/UHI_Baltimore_EnergyMeteorology/)**

---

