import pandas as pd

from pandas_profiling import ProfileReport


dataset = pd.read_csv("data/heart.csv")

profile = ProfileReport(dataset, title='Pandas Profiling Report', explorative=True)

profile.to_file("reports/example/EDA-report.html")
