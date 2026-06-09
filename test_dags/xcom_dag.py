from airflow.sdk import dag, task


@dag
def xcom_dag():

    @task
    def task1():
        return 111

    @task
    def task2(val: int):
        print(val)

    task_1 = task1()
    task2(task_1)


xcom_dag()
