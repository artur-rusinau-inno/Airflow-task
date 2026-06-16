from airflow.sdk import dag, task

values = ["1", "2", "3"]


@dag
def my_dag():

    @task.bash
    def bash_echo(value: str):
        return f"echo {value}"

    bash_echo.expand(value=values)


my_dag()
