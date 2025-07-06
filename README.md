# gaps_tdi

Repository to predict widening of gap due to calculations resulting from time-delay interferometry

## Overview

This project investigates the impact of data gaps on the LISA (Laser Interferometer Space Antenna) L01 pipeline, specifically focusing on how gaps in telemetry data propagate and widen when processed through Time-Delay Interferometry (TDI) calculations. The research aims to understand and predict the widening of data gaps that occurs due to interpolation and delay operations in the TDI pipeline.

## Research Objectives

The main research goals include:

- **Gap Impact Analysis**: Understanding what types of data gaps are most impacted by TDI processing
- **TDI Generation Effects**: Determining which generation of TDI variables shows the most significant impact
- **Gap Widening Dependencies**: Identifying the factors that influence data gap widening
- **Statistical Modeling**: Building distributions of data gaps to predict their behavior

## Project Structure

```
gaps_tdi/
├── README.md                          # This file
├── data_for_simulations/              # Simulation data and configuration
│   ├── config.yaml                    # LISA instrument configuration
│   ├── groundtrack.h5                 # Ground tracking data
│   ├── gw.h5                          # Gravitational wave data
│   ├── instru.h5                      # Instrument data
│   └── orbits.h5                      # Orbital data
├── notebooks/                         # Jupyter notebooks for analysis
│   ├── investigation_gap_widening.ipynb    # Main gap widening investigation
│   ├── pipeline_w_gaps.ipynb              # Pipeline with gap handling
│   ├── research_pipeline_w_gaps.ipynb     # Research pipeline implementation
│   └── results_full_LISA_dataset.ipynb    # Full dataset analysis results
└── Plots/                             # Generated plots and visualizations
    ├── Duty_Cycle_Distribution.png
    ├── TDI_X_augmentation.png
    ├── gap_widening_comparison*.png
    └── multiple_nans_order_45_2nd_generation_TDI_widening.png
```

## Key Features

### Gap Widening Analysis
- **Mathematical Framework**: Implementation of gap augmentation expressions that predict how gaps widen through TDI processing
- **Lagrange Interpolation**: Analysis of how different Lagrange interpolation orders affect gap widening
- **Delay Dependencies**: Investigation of how time delays in the TDI pipeline contribute to gap expansion

### TDI Pipeline Implementation
- **Mojito Integration**: Uses the Mojito noise pipeline with gap handling capabilities
- **Multi-generation TDI**: Supports analysis of different TDI variable generations (η, ξ, X, Y, Z)
- **Real LISA Data**: Works with realistic LISA constellation data including orbital dynamics

### Visualization and Analysis
- **Gap Widening Comparisons**: Comprehensive plots showing gap widening across different configurations
- **Duty Cycle Analysis**: Statistical analysis of data availability and gap distributions
- **TDI Variable Augmentation**: Visual representations of how gaps propagate through TDI calculations

## Dependencies

The project relies on several key libraries:

- **lolipops**: LISA data processing pipeline
- **pytdi**: Time-Delay Interferometry calculations
- **LISA_artefacts**: Custom gap mask generation tools
- **lisaconstants**: LISA mission constants
- **numpy**: Numerical computations
- **matplotlib**: Plotting and visualization
- **h5py**: HDF5 file handling
- **yaml**: Configuration file parsing

## Usage

### Running the Analysis

1. **Gap Widening Investigation**:
   ```bash
   jupyter notebook notebooks/investigation_gap_widening.ipynb
   ```

2. **Pipeline with Gaps**:
   ```bash
   jupyter notebook notebooks/pipeline_w_gaps.ipynb
   ```

3. **Full Dataset Results**:
   ```bash
   jupyter notebook notebooks/results_full_LISA_dataset.ipynb
   ```

### Configuration

The simulation parameters are configured in `data_for_simulations/config.yaml`, including:
- Instrument noise parameters
- Orbital configuration
- TDI processing settings
- Sampling rates and timing

## Key Algorithms

### Gap Augmentation Formula

The project implements mathematical expressions to predict gap widening:

```python
def gap_augmentation_expression(lagrange_order, N_nans, delay, delay_number=1.0):
    """
    Compute the gap augmentation from telemetry to eta variables.
    
    Parameters:
    - lagrange_order: Order of Lagrange interpolation
    - N_nans: Number of NaN values in original gap
    - delay: Time delay in samples
    - delay_number: Delay multiplier
    
    Returns:
    - extra_widening: Additional widening due to interpolation
    - total_nans: Total NaN values after widening
    """
```

### Cascade Widening

The project also handles multiple stages of gap widening as data flows through different TDI generations.

## Results

The analysis produces several key outputs:

- **Gap Widening Predictions**: Accurate mathematical models for predicting how gaps expand
- **Statistical Distributions**: Characterization of gap behavior across different scenarios
- **Performance Metrics**: Quantitative assessment of pipeline robustness to data gaps
- **Visualization Suite**: Comprehensive plots showing gap behavior across various configurations

## Applications

This research is relevant for:

- **LISA Mission Planning**: Understanding data availability requirements
- **Pipeline Optimization**: Improving TDI algorithms for gap resilience
- **Data Quality Assessment**: Predicting the impact of telemetry interruptions
- **Scientific Analysis**: Ensuring robust gravitational wave detection in the presence of data gaps

## Contributing

The project is organized as a research codebase with Jupyter notebooks for interactive analysis. The main entry points are the notebooks in the `notebooks/` directory, each focusing on different aspects of the gap widening investigation.

## License

This project is part of LISA gravitational wave detection research and follows standard academic research practices.

---

*This project contributes to the understanding of data gap propagation in space-based gravitational wave detectors, specifically focusing on the Time-Delay Interferometry techniques used in the LISA mission.*
