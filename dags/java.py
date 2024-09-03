from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Define the default_args dictionary
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

# Define the DAG
with DAG(
    dag_id='print_java_version',
    default_args=default_args,
    schedule_interval=None,  # or set a cron schedule
    catchup=False,
) as dag:

    # Define the BashOperator to print the Java version
    print_java_version = BashOperator(
        task_id='print_java_version',
        bash_command='java -version',
    )

    # Set the task dependencies (if any)
    print_java_version

