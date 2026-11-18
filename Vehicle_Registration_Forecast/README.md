# :car: Vehicle Registration Forecast

Data science challenge: forecast how many new vehicles will be registered in Brazil in the coming months.

**Solution:** [notebook](Vehicle_Registration_Forecast.ipynb)

<br>

## :exclamation: Problem

1. **Forecast the number of new vehicles registered 1 month and 6 months ahead.**
2. **Test the model on registrations by segment: passenger cars, light commercials, trucks and buses.**

## :computer: Resources

Public data from ANFAVEA and IBGE. The files are not included in this repository.

**[ANFAVEA](https://anfavea.com.br/estatisticas)** (National Association of Motor Vehicle Manufacturers)

- Monthly series since January 1957, by segment (passenger cars, light commercials, trucks, buses, total): production, registrations (domestic, imported and total) and exports in units.
- Monthly series since January 1985 of exports in value, by sector (vehicles; agricultural and road machinery).
- Monthly series since January 1983 of employment, by sector (vehicles; agricultural and road machinery).

**[IBGE SIDRA](https://sidra.ibge.gov.br)** (Brazilian Institute of Geography and Statistics)

- **LSPA** (Systematic Survey of Agricultural Production)
  - Annual estimate of planted area, harvested area, production and average yield of crops (table 6588)
- **PIM-PF** (Monthly Industrial Survey – Physical Production)
  - By selected industrial groups and classes (table 3650)
  - By major economic categories (table 3651)
  - Typical civil construction inputs (table 3652)
  - By sections and industrial activities (table 3653)
  - By special indicators (table 6607)
- **PMC** (Monthly Retail Survey), 2014 = 100
  - Sales of construction materials (table 3415)
  - Retail sales (table 3416)
  - Expanded retail sales (table 3417)
  - Retail sales by activity (table 3418)
  - Expanded retail sales by activity (table 3419)
  - Sales of vehicles, motorcycles, parts and pieces (table 3420)
- **PMS** (Monthly Services Survey), 2014 = 100
  - Revenue and volume of services (table 6442)
  - By service activity and subdivision (table 6443)
  - By service activity (table 6444)
- **IPCA** (Broad National Consumer Price Index)
  - Seasonally adjusted, monthly change since January 1998 (table 118)
  - Index number and changes over 3, 6 and 12 months and year to date, since December 1979 (table 1737)
  - Index number and changes from 12 months onwards, since November 2014 (table 6691)
  - Monthly change, year to date, 12 months and weights, by group, subgroup, item and sub-item, since January 2020 (table 7060)
  - The same, seasonally adjusted (table 7061)

## :rocket: Deliverables

A Jupyter notebook showing the full development of the solution.

## :gear: Running the notebook

The dependencies are managed with [uv](https://docs.astral.sh/uv/): `pyproject.toml` lists the packages and `uv.lock` pins the exact versions the notebook was run with (Python 3.14). uv installs Python 3.14 if it is missing.

```bash
cd Vehicle_Registration_Forecast
uv sync                            # create .venv with the locked versions
uv run jupyter lab
```

The data is not included in this repository. To run the notebook, point `DATA_DIR` in its setup cell to your copy of the data.

<br>

[← Back to portfolio](../README.md)
