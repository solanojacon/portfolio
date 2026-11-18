# :moneybag: Lead Scoring for WhatsApp Campaigns

Data science challenge: find which leads are most likely to buy, so that WhatsApp messages go to the right people.

**Solution:** [notebook](Lead_Scoring_for_WhatsApp_Campaigns.ipynb)

<br>

## :question: Context

You work at an e-commerce company that sells personalized hair-care products. To personalize the product, the company asks customers to fill out a questionnaire about their hair and routine. When they finish, they are taken straight to checkout, where they decide whether to complete the purchase.

The online sale has three steps:

1. Filling out the questionnaire
2. Selecting the products
3. Completing the purchase

## :exclamation: Problem

The company spends a lot on WhatsApp messages sent to everyone who fills out the questionnaire (the *leads*). Identifying the leads most likely to buy would make these messages more effective.

Your task is to **find the relationship between leads and buyers** using the company's data, and present your conclusions.

## :computer: Resources

The data comes from the company's PostgreSQL database, with the structure below. The data is not included in this repository.

![Database structure](images/db-uml.png 'Database structure')

## :rocket: Deliverables

A Jupyter notebook showing the full development of the solution, including:

1. Data reading and normalization
2. Algorithm choice
3. Train/test split and model training
4. Theoretical and practical support for the chosen algorithms (there may be more than one)
5. How and why the features were chosen
6. Saving the trained model, loading it and generating scores
7. Final results with performance metrics

## :gear: Running the notebook

The dependencies are managed with [uv](https://docs.astral.sh/uv/): `pyproject.toml` lists the packages and `uv.lock` pins the exact versions the notebook was run with (Python 3.14). uv installs Python 3.14 if it is missing.

```bash
cd Lead_Scoring_for_WhatsApp_Campaigns
uv sync                            # create .venv with the locked versions
uv run jupyter lab
```

The data is not included in this repository. To run the notebook, point `DATA_PATH` in its setup cell to your copy of the data.

<br>

[← Back to portfolio](../README.md)
