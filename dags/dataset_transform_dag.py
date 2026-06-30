from airflow.providers.google.suite.hooks.drive import GoogleDriveHook
from airflow.sdk import dag, task, task_group

from dags.assets import dataset_transformed

# from airflow.providers.google.cloud.transfers.gdrive_to_local import GoogleDriveToLocalOperator


@dag
def my_dag():

    @task.sensor
    def file_sensor():
        hook = GoogleDriveHook()

    @task.branch
    def check_if_file_empty(file):
        if not file:
            return "log_file_empty"
        else:
            return "file_processing"

    @task_group
    def file_processing():

        @task
        def replace_nulls(): ...

        @task
        def sort_by_date(): ...

        @task
        def clean_text(): ...

        replace_nulls() >> sort_by_date() >> clean_text()

    @task.bash
    def log_file_empty():
        return "echo file is empty"

    @task(trigger_rule="none_failed_min_one_success", outlets=[dataset_transformed])
    def end(): ...

    (
        file_sensor()
        >> check_if_file_empty()
        >> [file_processing(), log_file_empty()]
        >> end()
    )


my_dag()
