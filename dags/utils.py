from airflow.utils.dates import timedelta


VOLUME = '/your/abs/path/to/data:/data'

default_args = {
    'owner': 'airflow',
    'email': ['your_email@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True
}
