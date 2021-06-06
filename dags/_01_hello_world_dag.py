from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(2),
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
        dag_id="_01_hello_world",
        default_args=default_args,
        description="Printing HELLO WORLD",
        schedule_interval=timedelta(days=1)
) as dag:
    t1 = BashOperator(task_id='print_hello',
                      bash_command=f'echo Hello')
    t2 = BashOperator(task_id='print_world',
                      bash_command=f'echo WORLD')
    t3 = BashOperator(task_id='write_file',
                      bash_command='echo olalala >> /opt/airflow/data/olala.txt')

    t1 >> t2 >> t3

