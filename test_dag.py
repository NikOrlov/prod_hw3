import sys
import pytest
from airflow.models import DagBag

sys.path.append('dags')


@pytest.fixture()
def dag_bag():
    return DagBag(dag_folder='dags', include_examples=False)


def test_dag_bag_import(dag_bag):
    assert dag_bag.dags is not None
    assert dag_bag.import_errors == {}


def test_dag_generate_data(dag_bag):
    assert '_prod3_1_generate_data' in dag_bag.dags
    assert len(dag_bag.dags['_prod3_1_generate_data'].tasks) == 3


def test_dag_train_model(dag_bag):
    assert '_prod3_2_train_model' in dag_bag.dags
    assert len(dag_bag.dags['_prod3_2_train_model'].tasks) == 6


def test_dag_predict(dag_bag):
    assert '_prod3_3_predict' in dag_bag.dags
    assert len(dag_bag.dags['_prod3_3_predict'].tasks) == 6


def test_dag_structure_generate_data(dag_bag):
    structure = {
        'start': ['generate_data'],
        'generate_data': ['end'],
        'end': []
    }
    dag = dag_bag.dags['_prod3_1_generate_data']
    for name, task in dag.task_dict.items():
        assert set(structure[name]) == task.downstream_task_ids


def test_dag_structure_train_model(dag_bag):
    structure = {
        'data_sensor': ['build_features'],
        'target_sensor': ['build_features'],
        'build_features': ['split_data'],
        'split_data': ['train_model'],
        'train_model': ['validate_model'],
        'validate_model': []
    }
    dag = dag_bag.dags['_prod3_2_train_model']
    for name, task in dag.task_dict.items():
        assert set(structure[name]) == task.downstream_task_ids


def test_dag_structure_predict(dag_bag):
    structure = {
        'start': ['data_sensor', 'model_sensor', 'transformer_sensor'],
        'data_sensor': ['prediction'],
        'model_sensor': ['prediction'],
        'transformer_sensor': ['prediction'],
        'prediction': ['end'],
        'end': []
    }
    dag = dag_bag.dags['_prod3_3_predict']
    for name, task in dag.task_dict.items():
        assert set(structure[name]) == task.downstream_task_ids
