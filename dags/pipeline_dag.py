from airflow import DAG
#from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

# this is for demonstration purposes only

# Define the default_args
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 9, 5),
    'retries': 1,
}

# Define the DAG
with DAG(
    'taxi_revenue_by_car_model_date',
    default_args=default_args,
    description='A DAG to calculate taxi revenue by car model and date.',
    schedule_interval=None,
    catchup=False,
) as dag:

    # to decouple airflow docker image from the code.
    # suggest having the logic in a seperate image and
    # using helm charts to run your job related logic
    # => airflow should have helm/k8s binary in its image
    pyspark_kafka_to_parquet = BashOperator(
        task_id='pyspark_kafka_to_parquet',
        # running in spark local mode. a spark program in local mode is still a spark program :)
        bash_command='python /opt/airflow/dags/kafka_to_parquet_job.py',
    )

    duckdb_calculate_stats = BashOperator(
        task_id='duckdb_calculate_stats',
        bash_command='python /opt/airflow/dags/create_stats_from_taxi_rides.py',
    )

    # Set task dependencies
    pyspark_kafka_to_parquet >> duckdb_calculate_stats
