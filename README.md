# LMDI-IDA Analysis of Norwegian GHG Emissions

This project performs a Log-Mean Divisia Index (LMDI) Index Decomposition Analysis (IDA) on Norwegian greenhouse gas emissions from 1990 to 2019. The analysis aims to identify and quantify the impact of various drivers on emissions over time.

## Author
Benedikt Goodman (goodmanbenedikt@gmail.com)

## Overview
This analysis investigates why Norway's emissions have remained relatively stagnant despite over 30 years of climate policies. It uses LMDI-IDA methods to measure the effect of different factors on direct greenhouse gas emissions in Norway.

## Drivers Analyzed
- Economic activity (total GDP)
- Economic structure (industry GDP/Total GDP)
- Energy efficiency (industry consumption of energy/industry GDP)
- Fossil share of energy (fossil energy per industry/industry consumption of energy)
- Carbon efficiency of fossil energy (emissions/fossil energy per industry)

## Key Findings
- There was a net increase in emissions of 6218 mktCO2e (about 10%) between 1990 and 2019.
- The increase is primarily due to economic growth and worsening energy efficiency outweighing the abating effects of structural shifts, lower fossil share, and higher carbon efficiency of energy.
- The main sectors contributing to increased emissions are the petroleum and transport industries.

## Project Structure
- `src/df_funcs.py`: Functions for data manipulation and preparation
- `src/lmdi_module.py`: Implementation of LMDI-IDA analysis
- `src/plot_funcs.py`: Functions for plotting results
- `LMDI-IDA-analysis.ipynb`: Main script for running the analysis and generating plots

## Dependencies
- pandas
- numpy
- matplotlib
- seaborn

## Usage
1. Ensure all dependencies are installed.
2. Place your input data in a CSV file named `sektor_kaya.csv` in the `data/` directory.
3. Run the `LMDI_script.py` file to perform the analysis and generate plots.

## Notes
- The analysis focuses on direct emissions and does not factor in emissions embodied in consumption.
- Results should be considered as ballpark estimates due to uncertainties in the underlying data.

## Further Information
For more detailed information about the methodology and findings, please refer to the author's master's thesis: [Drivers of Norwegian GHG emissions 1990-2019](https://nmbu.brage.unit.no/nmbu-xmlui/handle/11250/3033120)

## Contact
For questions or access to the full dataset, please contact the author at goodmanbenedikt@gmail.com.