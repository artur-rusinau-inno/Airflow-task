from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.sdk import dag, task


@dag()
def test_mongodb_connection():
    @task
    def check_mongo_ping():
        # Подключаемся по ID, который вы настроили в UI (mongo_default)
        hook = MongoHook(mongo_conn_id="mongo_default")

        # Получаем прямой клиент pymongo
        client = hook.get_conn()

        # Стучимся в базу admin, где лежат ваши root-учетные данные
        db = client.admin

        # Выполняем стандартную команду проверки связи
        status = db.command("ping")

        print("====== ОТВЕТ БАЗЫ ДАННЫХ ======")
        print(status)
        print("===============================")

    check_mongo_ping()


test_mongodb_connection()
