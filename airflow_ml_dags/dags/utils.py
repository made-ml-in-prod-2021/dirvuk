from datetime import timedelta


default_args = {
    "owner": "airflow",
    "email_on_failure": True,
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

RAW_DIR = "data/raw/{{ ds }}"
VOLUME_DIR = "<PATH TO FOLDER>/data"