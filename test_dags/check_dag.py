from airflow.sdk import dag, task
from pendulum import datetime


@dag(
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    description="DAG to check data",
    tags=["data_engineering"],
)
def check_dag():

    @task.bash
    def create_file():
        return 'echo "Hi there!" >/tmp/dummy'

    @task.bash
    def check_file():
        return "test -f /tmp/dummy"

    @task
    def read_file():
        print(open("/tmp/dummy", "rb").read())

    create_file() >> check_file() >> read_file()


check_dag()
