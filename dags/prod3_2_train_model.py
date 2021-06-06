from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {"owner": 'airflow',
                "email": ["airflow@example.com"],
                "retries": 1,
                "retry_delay": timedelta(minutes=5)}

with DAG(dag_id='_prod3_2_train_model',
         schedule_interval='@daily',
         start_date=days_ago(0, 2),
         default_args=default_args) as dag:

    build_features = DockerOperator(task_id='build_features',
                                    image='build_features',
                                    command='/data/raw/{{ ds }}',
                                    network_mode='bridge',
                                    volumes=['/home/nikita/MADE/Prod/airflow_examples/data:/data'],
                                    do_xcom_push=False)
    split_data = DockerOperator(task_id='split_data',
                                image='split_data',
                                command='/data/processed/{{ ds }}',
                                network_mode='bridge',
                                volumes=['/home/nikita/MADE/Prod/airflow_examples/data:/data'],
                                do_xcom_push=False)
    train_model = DockerOperator(task_id='train_model',
                                 image='train_model',
                                 command='/data/processed/{{ ds }}',
                                 network_mode='bridge',
                                 volumes=['/home/nikita/MADE/Prod/airflow_examples/data:/data'],
                                 do_xcom_push=False)

    validate_model = DockerOperator(task_id='validate_model',
                                    image='validate_model',
                                    command='/data/model/{{ ds }}',
                                    network_mode='bridge',
                                    volumes=['/home/nikita/MADE/Prod/airflow_examples/data:/data'],
                                    do_xcom_push=False)

    build_features >> split_data >> train_model >> validate_model

    # echo = BashOperator(task_id='print',
    #                     bash_command='wc -l /opt/airflow/data/processed/{{ ds }}/train_val.csv')
    #
    # build_features >> echo >> split_data >> train_model
