# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
import pendulum
from airflow.hooks.base_hook import BaseHook
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator

with DAG(
    'slack_dag',
    description='Slack DAG tutorial',
    schedule_interval="@daily",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=['riki'],
) as dag:
    slack_webhook_token = BaseHook.get_connection('Slack').password
    slack_msg = """
                :red_circle: Task Failed. 
                *Task*: task  
                *Dag*: dag 
                """
    failed_alert = SlackWebhookOperator(
        task_id='slack_test',
        http_conn_id='Slack',
        webhook_token=slack_webhook_token,
        message=slack_msg,
        username='airflow',
        dag=dag)

    failed_alert
