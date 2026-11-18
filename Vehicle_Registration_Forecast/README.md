# :car: Vehicle Registration Forecast

Data science challenge: forecast how many new vehicles will be registered in Brazil in the coming months.

**Solution:** [notebook](Vehicle_Registration_Forecast.ipynb)

<br>

## :exclamation: Problem

1. **Forecast the number of new vehicles registered 1 month and 6 months ahead.**
2. **Test the model on registrations by segment: passenger cars, light commercials, trucks and buses.**

## :computer: Resources

Public data from ANFAVEA and IBGE. The files are not included in this repository.

- **[ANFAVEA](https://anfavea.com.br/estatisticas)** (National Association of Motor Vehicle Manufacturers): monthly registrations since January 1957, by segment (passenger cars, light commercials, trucks, buses), among other series.
- **[IBGE SIDRA](https://sidra.ibge.gov.br)** (Brazilian Institute of Geography and Statistics), one table per survey:
  - **PIM-PF** (Monthly Industrial Survey), table 3653: industrial production
  - **PMC** (Monthly Retail Survey), table 3416: retail sales
  - **PMS** (Monthly Services Survey), table 6442: services volume
  - **LSPA** (Systematic Survey of Agricultural Production), table 6588: harvested area
  - **IPCA** (Broad National Consumer Price Index), table 1737: consumer prices

Another 15 IBGE tables from the same surveys were provided and are not used.

## :rocket: Deliverables

A Jupyter notebook showing the full development of the solution.

## :gear: Running the notebook

The dependencies are managed with [uv](https://docs.astral.sh/uv/): `pyproject.toml` lists the packages and `uv.lock` pins the exact versions the notebook was run with (Python 3.14). uv installs Python 3.14 if it is missing.

```bash
cd Vehicle_Registration_Forecast
uv sync                            # create .venv with the locked versions
uv run jupyter lab
```

The data is not included in this repository. The notebook expects it in `portfolio-data/Vehicle_Registration_Forecast/data/`, in a `portfolio-data` folder next to this repository. To use another location, change `DATA_DIR` in the notebook's setup cell.

<br>

[← Back to portfolio](../README.md)
