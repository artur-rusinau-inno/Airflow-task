from airflow.sdk import dag, task
from pendulum import datetime


@dag(
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    description="test description",
    tags=["tag1", "tag2"],
    max_consecutive_failed_dag_runs=3,
)
def my_dag():

    @task
    def task_1():
        print("Hello 1")

    @task
    def task_2():
        print("Hello 2")

    @task
    def task_3():
        print("Hello 3")

    @task
    def task_4():
        print("Hello 4")

    task_1() >> task_2() >> task_3() >> task_4()


my_dag()
