import random

from airflow.sdk import dag, task


@dag
def agg_dag():

    @task
    def get_files():
        return [f"file_{i}" for i in range(random.randint(3, 5))]

    @task
    def load_files(folder: str, file: str):

        return f"{folder}/{file}"

    @task.bash
    def bash_script(files: list[str]):
        str_files = " ".join(files)
        return f"echo {str_files}"

    files = get_files()

    mapped_files = load_files.partial(folder="src").expand(file=files)

    bash_script(mapped_files)


agg_dag()
