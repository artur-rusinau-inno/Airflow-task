import pandas as pd
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.sdk import dag, task

from config.settings import settings
from plugins.assets import dataset_transformed
from plugins.mongo_qieries import LESS_THAN_5_LENGHT_COMMENTS, TOP_5_COMMENTS


@dag(schedule=[dataset_transformed])
def mongo_dag():

    @task
    def upload_data():
        df = pd.read_csv(settings.LOCAL_FILE_PATH)
        dict_df = df.to_dict("records")
        print(f"прочитано {len(dict_df)} строк")
        hook = MongoHook()
        hook.delete_many(filter_doc={}, **settings.mongo_settings.MONGO_PARAMS)
        hook.insert_many(docs=dict_df, **settings.mongo_settings.MONGO_PARAMS)

    @task
    def run_queries():
        hook = MongoHook()
        collection = hook.get_conn()[settings.mongo_settings.MONGO_DB_NAME][
            settings.mongo_settings.MONGO_COLLECTION_NAME
        ]
        print(f"всего {collection.count_documents({})} строк")
        top_5_comments = list(collection.aggregate(TOP_5_COMMENTS))
        for index, comment in enumerate(top_5_comments, 1):
            print(f"{index}) {comment.get('_id')} === {comment.get('count')}")

        print("=" * 20)

        less_than_5_lenght_comments = list(
            collection.aggregate(LESS_THAN_5_LENGHT_COMMENTS)
        )
        for index, comment in enumerate(less_than_5_lenght_comments, 1):
            print(f"{index}) {comment.get('content')}")

    upload_data() >> run_queries()


mongo_dag()
