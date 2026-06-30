from airflow.sdk import dag, task

from dags.assets import dataset_transformed


@dag(schedule=[dataset_transformed])
def mongo_dag():

    @task
    def upload(): ...

    @task
    def run_queries(): ...

    upload() >> run_queries()


mongo_dag()
