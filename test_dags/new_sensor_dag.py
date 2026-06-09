from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.sdk import dag, task
from pendulum import datetime


@dag(start_date=datetime(2026, 1, 1), tags=["sensor"])
def my_new_sensor():

    sensor_task = FileSensor.partial(
        poke_interval=10,
        task_id="sensor_task",
        fs_conn_id="fs_default",
    ).expand(
        filepath=["data_1.csv", "data_2.csv", "data_3.csv"],
    )

    @task
    def outcome():
        print("File found!")

    sensor_task >> outcome()


my_new_sensor()
