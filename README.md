# gaps_tdi

**Repository for analyzing data gap propagation and widening effects due to Time-Delay Interferometry (TDI) computations**

## Overview

This project investigates how data gaps in onboard LISA (Laser Interferometer Space Antenna) interferometers telemetry measurements propagate through TDI pipelines. The research focuses on understanding, predicting, and quantifying the widening of data gaps that occurs due to Lagrange interpolation (applying FIR filters) and delay operations in the TDI pipeline, with particular emphasis on static constellation configurations. We provide notebooks to generate the plots in the paper and codes to compute the gap augmentation in the intermediary and TDI variables

## Project Structure

```
gaps_tdi/
├── README.md                           # Project documentation
├── data_for_simulations/               # Simulation data and configuration
│   ├── config.yaml                     # LISA instrument configuration
│   ├── groundtrack.h5                  # Ground tracking data
│   ├── gw.h5                           # Gravitational wave data
│   ├── instru.h5                       # Instrument telemetry data
│   └── orbits.h5                       # Orbital trajectory data
├── utility_funcs/                      # Core utility functions
│   ├── gap_widening_utils.py           # Gap augmentation calculations
│   └── multi_gap_utils.py              # Multi-gap analysis tools
├── notebooks/                          # Analysis notebooks
│   ├── static_constellation/           # Static LISA configuration analysis
│   │   ├── investigation_gap_widening_static.ipynb    # Main gap analysis
│   │   ├── compare_TDI_timeseries_missing_data.ipynb  # TDI comparison tools
│   │   └── *.h5                        # Static simulation datasets
│   ├── time_varying_explore/           # Time-varying arm analysis
│   │   └── investigation_gap_widening_time_varying_arms.ipynb
│   ├── full_LISA_simulations/          # Full-scale LISA simulations
│   └── data/                           # Processed analysis data
│       └── data_for_large_LISA_like_simulations/
└── Plots/                              # Generated visualizations
    ├── Duty_Cycle_Distribution*.png
    ├── gap_widening_comparison*.png
    └── TDI_X_augmentation.png
```

## Dependencies

The project relies on several key libraries:

- **numpy**: Array operations  
- **matplotlib**: Plotting
- **scipy**: Scientific computing
- **h5py**: HDF5 data access
- **yaml**: Config parsing
- **tqdm**: Progress bars
- **pickle**: Data serialization

- **lisaconstants**: Constants and parameters specific to the LISA mission
- **lisainstrument**: LISA telemetry data generation 
- **pytdi**: Time-Delay Interferometry calculations and factorized TDI expressions
- **lisagap**: Gap mask generation and analysis tools.

## Usage

```bash
conda create -n gap_tdi_env python=3.12
pip install -r requirements.txt
pip install lisainstrument pytdi lisaconstants lisaorbits
pip install --extra-index-url https://test.pypi.org/simple/ lisa-gap==0.3.4
```

### Main Analysis Notebooks

1. **Static Constellation Gap Analysis**:

```bash
   jupyter notebook notebooks/static_constellation/investigation_gap_widening_static.ipynb
   ```
   - Core gap widening investigation for static LISA configurations
   - Includes gap augmentation validation and multi-generation TDI analysis

2. **TDI Time Series Comparison**:
```bash
   jupyter notebook notebooks/static_constellation/compare_TDI_timeseries_missing_data.ipynb
   ```
   - Spectral analysis of TDI variables with and without gaps
   - Lomb-Scargle periodogram comparisons

3. **Time-Varying Analysis**:
```bash
   jupyter notebook notebooks/time_varying_explore/investigation_gap_widening_time_varying_arms.ipynb
   ```
   - Gap analysis for time-varying LISA arm lengths
   - Still under development!

### Utility Functions

Import the core gap analysis functions:

```python
from utility_funcs.gap_widening_utils import (
    gap_augmentation_expression,
    widening_gap_X1,
    widening_gap_X2
)

from utility_funcs.multi_gap_utils import (
    mask_TDI_X,
    approx_total_nans_from_nan_blocks_X
)
```

### Configuration

The simulation parameters are configured in `data_for_simulations/config.yaml`, including:
- Instrument noise parameters (test mass, laser, optical metrology system)
- Orbital configuration and sampling rates  
- TDI processing settings and interpolation orders
- Time sampling (dt = 0.25s) and simulation duration


### Gap Augmentation Formula

The project implements mathematical expressions to predict gap widening through TDI processing:

```python
def gap_augmentation_expression(lagrange_order, N_nans, delay, delay_number=1.0):
    """
    Compute the gap augmentation from telemetry to eta variables.
    
    Parameters:
    - lagrange_order: Order of Lagrange interpolation (typically 45)
    - N_nans: Number of NaN values in original gap
    - delay: Time delay in samples (~33 for LISA)
    - delay_number: Delay multiplier for different TDI stages
    
    Returns:
    - extra_widening: Additional widening due to interpolation
    - total_nans: Total NaN values after widening
    """
```

### Multi-Generation TDI Widening

```python
def widening_gap_X1(lagrange_order, N_nans, delay):
    """Compute gap augmentation from eta to X1 variables (factorized)"""
    
def widening_gap_X2(lagrange_order, N_nans, delay):
    """Compute gap augmentation from X1 to X2 variables (fully factorized)"""
```

## Results

The analysis produces several key outputs:

- **Gap Widening Predictions**: Mathematical models validated against PyTDI simulations
- **Multi-generation Analysis**: Tracking gap amplification through η → X1 → X2 TDI stages
- **Time-domain Comparisons**: Direct visualization of gap effects on TDI time series
- **Plots for Paper**: The notebooks here can reproduce the plots in the paper

### Key Findings

- Gap widening depends on Lagrange interpolation order and time delays between LISA arms.
- For TDI2, we observe a gap widening of roughly 90 seconds per gap in raw telemetry.
- Higher-order TDI generations show increased gap widening. 
- Due to merging of gaps, overall duty cycle is ~ 84%.
- For a realistic gap scenario, we expect to lose approximately 4 days worth of data if ultra high frequent missing data segments are present. 

## Applications

This research is relevant for:

- **LISA Mission Planning**: Understanding data availability requirements
- **Pipeline Optimization**: Improving TDI algorithms for gap resilience
- **Data Quality Assessment**: Predicting the impact of telemetry interruptions

## Contributing

The project is organized as a research codebase with Jupyter notebooks for interactive analysis and modular utility functions for reusable computations. 

### Development Workflow
- **Main analysis**: Use notebooks in `static_constellation/` for core investigations. Reproduces Figure 1. 
- **LISA based simulations** Use notebooks in `full_LISA_simulations` to see a realistic gap augmentation case for the instrument.
- **Utility functions**: Extend `utility_funcs/` for codes that allow you to cheaply compute the gap augmentation for different TDI variables.

## License

This project is part of LISA gravitational wave detection research and follows standard academic research practices.


## Citations

If you use any parts of this code, please cite 

```bibtex
    @unpublished{Burke:2025:TDI-Gaps,
    author       = {Burke, Ollie and Muratore, Martina and Woan, Graham},
    title        = {The impact of missing data on the construction of LISA Time Delay Interferometry Michelson variables},
    note         = {In preparation and to be submitted to \textit{Phys.\ Rev.\ D}},
    year         = {2025},
    month        = sep,
    }

    @software{lisagap,
    author = {Burke, Ollie and Castelli, Eleonora},
    title = {lisa-gap: A tool for simulating data gaps in LISA time series},
    url = {https://github.com/ollieburke/lisa-gap},
    version = {0.3.3},
    year = {2025}
    }

---

*This project contributes to the understanding of data gap propagation in space-based gravitational wave detectors, specifically focusing on the Time-Delay Interferometry techniques used in the LISA mission.*
