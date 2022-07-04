from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.exceptions import AirflowSensorTimeout
from datetime import datetime
default_args = {
    'start_date': datetime(2021, 1, 1)
}


def _process():
    pass


def _store():
    pass


def _failure_callback(context):

    if isinstance(context['exception'], AirflowSensorTimeout):
        print(context)
        print("Sensor timed out")


with DAG('filesensor_example',
         schedule_interval='@daily',
         default_args=default_args,
         tags=['riki'],
         catchup=False) as dag:
    partners = [
        FileSensor(
            task_id=f'partner_{partner}',
            poke_interval=60,
            timeout=60 * 30,
            mode="reschedule",
            on_failure_callback=_failure_callback,
            filepath=f'/home/rolando/kindshare/partner_{partner}.txt',
            fs_conn_id=f'conn_filesensor_{partner}'
        ) for partner in ['a', 'b', 'c']]

    process = PythonOperator(
        task_id="process",
        python_callable=_process,
    )

    store = PythonOperator(
        task_id="store",
        python_callable=_store,
    )

    partners >> process >> store
