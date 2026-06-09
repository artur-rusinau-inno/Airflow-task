from airflow.sdk import Variable, dag, task


@dag
def variable():

    @task
    def print_my_var():
        print(Variable.get("api", deserialize_json=True))

    print_my_var()


variable()
