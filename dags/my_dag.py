from airflow.sdk import dag, task

# from airflow.providers.google.suite.hooks.drive import GoogleDriveHook
# from airflow.providers.google.cloud.transfers.gdrive_to_local import GoogleDriveToLocalOperator


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
