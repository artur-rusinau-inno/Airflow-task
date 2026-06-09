from airflow.sdk import dag, task


@dag
def my_sensor():

    @task.sensor(poke_interval=60, timeout=7 * 24 * 60 * 60)
    def get_status():
        return False

    get_status()


my_sensor()
