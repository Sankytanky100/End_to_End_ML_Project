# End to End ML Project

An end-to-end machine learning project that trains a regression model to predict student
math performance and serves predictions through a Flask web UI.

## Highlights

- **Clear pipeline stages**: data ingestion, transformation, and model training.
- **Reusable components**: each pipeline stage is encapsulated in a class for easy
  experimentation and maintenance.
- **Production-ready inference**: predictions are served via a Flask app using persisted
  model and preprocessing artifacts.

## Project Structure

```
.
├── app.py                     # Flask app entrypoint
├── application.py             # Alternative Flask entrypoint (same behavior)
├── src
│   ├── components             # Ingestion, transformation, training components
│   ├── pipeline               # Train and prediction pipelines
│   └── utils                  # Logging, exceptions, helpers
├── artifacts                  # Persisted training outputs (generated)
├── templates                  # HTML templates for the UI
└── notebook                   # Exploratory notebooks and legacy shims
```

## Setup

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Ensure the dataset exists at `notebook/data/stud.csv`.

## Training the Model

Use the training pipeline to build the preprocessing artifacts and train the model:

```bash
python -m src.pipeline.train_pipeline
```

This will create model artifacts under `artifacts/`.

## Running the Web App

Start the Flask server:

```bash
python app.py
```

Then open your browser to `http://localhost:5000` to access the UI.

## Making Predictions Programmatically

You can use the prediction pipeline directly:

```python
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

sample = CustomData(
    gender="female",
    race_ethnicity="group A",
    parental_level_of_education="bachelor's degree",
    lunch="standard",
    test_preparation_course="none",
    reading_score=72,
    writing_score=74,
)

pred_df = sample.get_data_as_data_frame()
prediction = PredictPipeline().predict(pred_df)
print(prediction)
```

## Notes

- `main/` and `notebook/components/` include compatibility shims for legacy imports.
- Logs are written to the `logs/` directory with timestamped file names.
