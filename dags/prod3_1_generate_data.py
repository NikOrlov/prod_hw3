from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from airflow.operators.dummy import DummyOperator
from utils import default_args, VOLUME


with DAG(dag_id='_prod3_1_generate_data',
         default_args=default_args,
         schedule_interval="@daily",
         start_date=days_ago(0, 2),
         ) as dag:

    start = DummyOperator(task_id='start')

    download = DockerOperator(
        image="generate_data",
        command="/data/raw/{{ ds }}",
        network_mode="bridge",
        task_id="generate_data",
        do_xcom_push=False,
        volumes=[VOLUME]
    )

    end = DummyOperator(task_id='end')

    start >> download >> end
