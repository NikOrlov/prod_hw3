from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from utils import default_args, VOLUME
from airflow.sensors.filesystem import FileSensor


prod_model_path = '{{ var.value.PROD_MODEL_PATH }}'

with DAG(dag_id='_prod3_3_predict',
         default_args=default_args,
         schedule_interval="@daily",
         start_date=days_ago(0, 2)) as dag:

    start = DummyOperator(task_id='start')

    data_sensor = FileSensor(task_id='data_sensor',
                             filepath='data/raw/{{ ds }}/data.csv',
                             poke_interval=10,
                             retries=100)

    model_sensor = FileSensor(task_id='model_sensor',
                              filepath='data/model/{{ ds }}/model.pkl',
                              poke_interval=10,
                              retries=100)

    transformer_sensor = FileSensor(task_id='transformer_sensor',
                                    filepath='data/model/{{ ds }}/transformer.pkl',
                                    poke_interval=10,
                                    retries=100)

    prediction = DockerOperator(task_id='prediction',
                                image='prediction',
                                command='/data/raw/{{ ds }}/ ' + prod_model_path,
                                network_mode='bridge',
                                volumes=[VOLUME],
                                do_xcom_push=False)

    end = DummyOperator(task_id='end')

    start >> [data_sensor, model_sensor, transformer_sensor] >> prediction >> end

