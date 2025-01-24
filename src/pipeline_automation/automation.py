from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    'owner': 'data_pipeline',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_pipeline_automation',
    default_args=default_args,
    description='A DAG for automating the data pipeline',
    schedule_interval=timedelta(days=7),
)

def run_web_scraping():
    subprocess.run(['python', 'src/web_scraping/scraper.py'])

def run_selenium_scraping():
    subprocess.run(['python', 'src/web_scraping/selenium_scraper.py'])

def run_data_ingestion():
    subprocess.run(['python', 'src/data_ingestion/ingestion.py'])

def run_etl_transformation():
    subprocess.run(['python', 'src/etl_transformation/transformation.py'])

def run_analytics():
    subprocess.run(['python', 'src/analytics/insights.py'])

web_scraping_task = PythonOperator(
    task_id='web_scraping',
    python_callable=run_web_scraping,
    dag=dag,
)

selenium_scraping_task = PythonOperator(
    task_id='selenium_scraping',
    python_callable=run_selenium_scraping,
    dag=dag,
)

data_ingestion_task = PythonOperator(
    task_id='data_ingestion',
    python_callable=run_data_ingestion,
    dag=dag,
)

etl_transformation_task = PythonOperator(
    task_id='etl_transformation',
    python_callable=run_etl_transformation,
    dag=dag,
)

analytics_task = PythonOperator(
    task_id='analytics',
    python_callable=run_analytics,
    dag=dag,
)

web_scraping_task >> selenium_scraping_task >> data_ingestion_task >> etl_transformation_task >> analytics_task