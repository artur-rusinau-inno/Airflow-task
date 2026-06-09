from airflow.sdk import dag, task


@dag
def my_dag():

    @task.sensor
    def task1():
        pass

    @task.branch
    def task2():
        pass

    task1() >> task2()


my_dag()
