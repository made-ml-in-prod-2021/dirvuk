# Example of base project for preparation to prod version

Project Organization
------------

    ├── README.md          <- The top-level README for developers using this project.
    │
    ├── config             <- Configs 
    │
    ├── data               <- The original, immutable data dump.
    │
    ├── enitioes           <- Base params
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │
    ├── tests            <- Test for validation Data and Train model
    │
    └── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
                              generated with `pip freeze > requirements.txt`

-------- 
**Preparation**

```bash
pip3 install -r requirements.txt
```

**Prepare EDA report**
```bash
python3 reports/prepare-EDA-report.py
```
See Example   -   reports/example/EDA-report.html

**Run tests (Data prepared using Faker Lib)**
```bash
pytest tests
```

**Train using RandomForestClassifier**

```bash
python3 train_pipeline.py config\config-rf.yaml
```

**Train using LinearRegression**
```bash
python3 train_pipeline.py config\config-lr.yaml
```

