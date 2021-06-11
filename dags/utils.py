from airflow.utils.dates import timedelta


VOLUME = '/home/lolvista/MADE/Prod/prod_hw3/data:/data'

default_args = {
    'owner': 'airflow',
    'email': ['n1@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email_on_success': True,
    'email_on_retry': True
}
