from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from airflow.sensors.filesystem import FileSensor
from datetime import timedelta
from utils import default_args, VOLUME


with DAG(dag_id='_prod3_2_train_model',
         schedule_interval='@weekly',
         start_date=days_ago(0, 2),
         default_args=default_args) as dag:

    data_sensor = FileSensor(task_id='data_sensor',
                             filepath='data/raw/{{ ds }}/data.csv',
                             poke_interval=10,
                             retries=100)

    target_sensor = FileSensor(task_id='target_sensor',
                               filepath='data/raw/{{ ds }}/target.csv',
                               poke_interval=10,
                               retries=100)

    build_features = DockerOperator(task_id='build_features',
                                    image='build_features',
                                    command='/data/raw/{{ ds }}',
                                    network_mode='bridge',
                                    volumes=[VOLUME],
                                    do_xcom_push=False)

    split_data = DockerOperator(task_id='split_data',
                                image='split_data',
                                command='/data/processed/{{ ds }}',
                                network_mode='bridge',
                                volumes=[VOLUME],
                                do_xcom_push=False)

    train_model = DockerOperator(task_id='train_model',
                                 image='train_model',
                                 command='/data/processed/{{ ds }}',
                                 network_mode='bridge',
                                 volumes=[VOLUME],
                                 do_xcom_push=False)

    validate_model = DockerOperator(task_id='validate_model',
                                    image='validate_model',
                                    command='/data/model/{{ ds }}',
                                    network_mode='bridge',
                                    volumes=[VOLUME],
                                    do_xcom_push=False)

    [data_sensor, target_sensor] >> build_features >> split_data >> train_model >> validate_model

