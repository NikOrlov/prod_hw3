from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta


default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(dag_id='_prod3_1_generate_data',
         default_args=default_args,
         schedule_interval="@daily",
         start_date=days_ago(0, 2),
         ) as dag:
    download = DockerOperator(
        image="generate_data",
        command="/data/raw/{{ ds }}",
        network_mode="bridge",
        task_id="generate_data",
        do_xcom_push=False,
        # !!! HOST folder(NOT IN CONTAINER) replace with yours !!!
        volumes=["/home/nikita/MADE/Prod/airflow_examples/data:/data"]
    )
    #
    echo = BashOperator(task_id='printing',
                        bash_command='wc -l /opt/airflow/data/raw/{{ ds }}/target.csv')

    # echo = BashOperator(task_id='printing',
    #                     bash_command='ls -al /opt/airflow/data/raw/{{ ds }}')
    pwd = BashOperator(task_id='pwd',
                       bash_command='pwd')

    download >> echo >> pwd
