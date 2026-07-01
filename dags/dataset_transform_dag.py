import pandas as pd
from airflow.providers.google.cloud.transfers.gdrive_to_local import (
    GoogleDriveToLocalOperator,
)
from airflow.providers.google.suite.hooks.drive import GoogleDriveHook
from airflow.providers.google.suite.sensors.drive import GoogleDriveFileExistenceSensor
from airflow.sdk import dag, task, task_group
from pendulum import datetime

from config.settings import settings
from plugins.assets import dataset_transformed


@dag(schedule="@daily", start_date=datetime(2026, 1, 1), catchup=False)
def dataset_transform_dag():

    gdrive_sensor = GoogleDriveFileExistenceSensor(
        task_id="wait_for_gdrive_file",
        poke_interval=10,
        timeout=60,
        **settings.GDRIVE_PARAMS,
    )

    @task.branch
    def check_if_file_empty():
        hook = GoogleDriveHook()
        service = hook.get_conn()
        file_id = hook.get_file_id(**settings.GDRIVE_PARAMS).get("id")
        file_metadata = service.files().get(fileId=file_id, fields="size").execute()
        file_size = int(file_metadata.get("size", 0))

        if not file_size:
            return "log_file_empty"
        else:
            return "download_gdrive_file"

    download_file = GoogleDriveToLocalOperator(
        task_id="download_gdrive_file",
        output_file=settings.LOCAL_FILE_PATH,
        **settings.GDRIVE_PARAMS,
    )

    @task_group
    def file_processing():

        @task
        def replace_nulls():
            df = pd.read_csv(settings.LOCAL_FILE_PATH)
            df = df.fillna("-")
            df = df.replace("null", "-")
            df.to_csv(settings.LOCAL_FILE_PATH, index=False)

        @task
        def sort_by_date():
            df = pd.read_csv(settings.LOCAL_FILE_PATH)
            df = df.sort_values("created_date")
            df.to_csv(settings.LOCAL_FILE_PATH, index=False)

        @task
        def clean_context():
            df = pd.read_csv(settings.LOCAL_FILE_PATH)
            df = df.replace(
                {
                    "content": r"\b(?:https?:\/\/|www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,12}(?:\/[^\s]*)?"
                },
                "",
                regex=True,
            )
            df = df.replace(
                {"content": r"[\U00010000-\U0010ffff]|[\u2600-\u27BF]|\ufe0f|\u200d"},
                "",
                regex=True,
            )
            df = df.replace({"content": r"[:;=\-]*[\(\)]+|:[DPpOoDd]"}, "", regex=True)
            df.to_csv(settings.LOCAL_FILE_PATH, index=False)

        replace_nulls() >> sort_by_date() >> clean_context()

    @task.bash
    def log_file_empty():
        return "echo file is empty, transformations aborted"

    @task.bash(outlets=[dataset_transformed])
    def end():
        return "echo transformations ended successfully, asset updated"

    gdrive_sensor >> check_if_file_empty() >> [download_file, log_file_empty()]
    download_file >> file_processing() >> end()


dataset_transform_dag()
