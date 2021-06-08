from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from utils import default_args, VOLUME
from airflow.operators.bash import BashOperator


# prod_model_path = '{{ var.value.PROD_MODEL_PATH }}'
prod_model_path = '/data/model/2021-06-08/'
with DAG(dag_id='_prod3_3_predict',
         default_args=default_args,
         schedule_interval="@daily",
         start_date=days_ago(0, 2)) as dag:

    start = DummyOperator(task_id='start')

    print_var = BashOperator(task_id='print_var',
                             bash_command=f'echo {prod_model_path}')

    prediction = DockerOperator(task_id='prediction',
                                image='prediction',
                                command='/data/raw/{{ ds }}/ ' + prod_model_path,
                                network_mode='bridge',
                                volumes=[VOLUME],
                                do_xcom_push=False)

    end = DummyOperator(task_id='end')

    start >> print_var >> prediction >> end

