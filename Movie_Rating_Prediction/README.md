# :movie_camera: Movie Rating Prediction

Data science challenge: predict how audiences will rate a movie or TV show before adding it to a streaming catalog.

**Solution:** [notebook](Movie_Rating_Prediction.ipynb)

<br>

## :exclamation: Problem

You were hired by a streaming company to build a model that predicts the rating a title would receive if it were added to the catalog. The goal is to decide whether a title is worth adding.

## :computer: Resources

The dataset `catalog.xlsx`, a catalog of about 6,200 movies and TV shows with their audience ratings. The data is not included in this repository.

## :rocket: Deliverables

A Jupyter notebook showing the full development of the solution, including:

1. Data processing
2. Feature engineering
3. Train/test split
4. Confusion matrix and precision–recall plot of the model on the test data
5. Improvement opportunities for the model, given the final result

## :gear: Running the notebook

The dependencies are managed with [uv](https://docs.astral.sh/uv/): `pyproject.toml` lists the packages and `uv.lock` pins the exact versions the notebook was run with (Python 3.14). uv installs Python 3.14 if it is missing.

```bash
cd Movie_Rating_Prediction
uv sync                            # create .venv with the locked versions
uv run jupyter lab
```

The data is not included in this repository. To run the notebook, point `DATA_PATH` in its setup cell to your copy of the data.

<br>

[← Back to portfolio](../README.md)
