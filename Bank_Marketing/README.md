# :bank: Bank Marketing

Data science challenge: find which bank clients are most likely to subscribe to a term deposit, so that telemarketing calls go to the right people.

**Solution:** [notebook](Bank_Marketing.ipynb)

<br>

## :question: Context

A Portuguese bank runs telemarketing campaigns to sell term deposits. Often more than one call to the same client is needed before the client decides whether to subscribe.

## :exclamation: Problem

**Predict whether a client will subscribe to a term deposit**, using a real-world dataset: explore the data, prepare it, build and evaluate a classification model, interpret the results, and assess how the model could be used in production.

## :computer: Resources

The public [Bank Marketing dataset](https://archive.ics.uci.edu/dataset/222/bank+marketing), also distributed on [Kaggle](https://www.kaggle.com/datasets/abdelazizsami/bank-marketing): 45,211 calls from May 2008 to November 2010, with 16 attributes of the client and the campaign, and the target `y` (the client subscribed). The data is not included in this repository.

> S. Moro, R. Laureano and P. Cortez. *Using Data Mining for Bank Direct Marketing: An Application of the CRISP-DM Methodology.* In P. Novais et al. (Eds.), Proceedings of the European Simulation and Modelling Conference – ESM'2011, pp. 117–121, Guimarães, Portugal, October 2011. EUROSIS.

## :rocket: Deliverables

Reproducible Python code (a Jupyter notebook) covering:

1. **Exploratory analysis:** basic statistics and data types, missing values and how they are handled, numeric and categorical distributions, and the relationship between the features and the target
2. **Preprocessing:** encoding, normalization or standardization (with justification), and the train/test split
3. **Modeling:** a classification model, with the choice of model and the parameter tuning justified
4. **Evaluation:** appropriate metrics (with justification) and explanatory charts
5. **Interpretation:** the most important features and actionable insights
6. **Production:** how the model could be used in production

## :gear: Running the notebook

The dependencies are managed with [uv](https://docs.astral.sh/uv/): `pyproject.toml` lists the packages and `uv.lock` pins the exact versions the notebook was run with (Python 3.14). uv installs Python 3.14 if it is missing.

```bash
cd Bank_Marketing
uv sync                            # create .venv with the locked versions
uv run jupyter lab
```

The data is not included in this repository. Download `bank-full.csv` from one of the links above and save it as `portfolio-data/Bank_Marketing/data/bank-full.csv`, in a `portfolio-data` folder next to this repository. The trained model is saved to `portfolio-data/Bank_Marketing/models/`. To use other locations, change `DATA_PATH` and `MODEL_PATH` in the notebook's setup cell.

<br>

[← Back to portfolio](../README.md)
