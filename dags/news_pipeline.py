from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fetch_news import fetch_top_headlines, save_raw_data
from src.summarize import process_articles

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
}

dag = DAG(
    'news_summarizer',
    default_args=default_args,
    description='Fetch news, summarize, version with DVC',
    schedule='@daily',
    catchup=False,
)

def fetch_task(**context):
    data = fetch_top_headlines(country='us', page_size=10)
    raw_path = save_raw_data(data)
    context['ti'].xcom_push(key='raw_path', value=raw_path)
    return raw_path

def summarize_task(**context):
    raw_path = context['ti'].xcom_pull(key='raw_path', task_ids='fetch_news')
    processed_path = process_articles(raw_path)
    context['ti'].xcom_push(key='processed_path', value=processed_path)
    return processed_path

fetch = PythonOperator(
    task_id='fetch_news',
    python_callable=fetch_task,
    dag=dag,
)

summarize = PythonOperator(
    task_id='summarize_news',
    python_callable=summarize_task,
    dag=dag,
)

dvc_init = BashOperator(
    task_id='dvc_init',
    bash_command='cd /opt/airflow && rm -rf .dvc && uv run dvc init --no-scm',
    dag=dag,
)


dvc_add_raw = BashOperator(
    task_id='dvc_add_raw',
    bash_command='cd /opt/airflow && uv run dvc add data/raw',
    dag=dag,
)

dvc_add_processed = BashOperator(
    task_id='dvc_add_processed',
    bash_command='cd /opt/airflow && uv run dvc add data/processed',
    dag=dag,
)

# dvc_push = BashOperator(
#     task_id='dvc_push',
#     bash_command='cd /opt/airflow && uv run dvc push',
#     dag=dag,
# )

# Update the dependency chain
# fetch >> summarize >> [dvc_add_raw, dvc_add_processed] >> dvc_push
# fetch >> summarize >> [dvc_add_raw, dvc_add_processed]
fetch >> summarize >> dvc_init >> [dvc_add_raw, dvc_add_processed]