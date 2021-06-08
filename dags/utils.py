from airflow.utils.dates import timedelta


VOLUME = '/home/lolvista/MADE/Prod/prod_hw3/data:/data'

default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}