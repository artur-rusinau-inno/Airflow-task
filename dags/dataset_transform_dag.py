from airflow.providers.google.suite.sensors.drive import GoogleDriveFileExistenceSensor
from airflow.sdk import dag, task, task_group

from config.settings import settings
from dags.assets import dataset_transformed

# from airflow.providers.google.cloud.transfers.gdrive_to_local import GoogleDriveToLocalOperator


@dag
def my_dag():

    gdrive_sensor = GoogleDriveFileExistenceSensor(
        task_id="wait_for_gdrive_file",
        poke_interval=10,
        timeout=60,
        folder_id=settings.GOOGLE_DISK_FOLDER_ID,
        file_name=settings.GOOGLE_FILE_NAME,
    )

    @task.branch
    def check_if_file_empty():
        file = False

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
        gdrive_sensor
        >> check_if_file_empty()
        >> [file_processing(), log_file_empty()]
        >> end()
    )


my_dag()
