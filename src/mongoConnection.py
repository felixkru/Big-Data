from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def send_data_to_mongo(processed_datasets):
    uri = "bitte bei felix anfragen"
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client['Big-D']
    collection = database['raw_measurements']

    try:
        collection.insert_many(processed_datasets)
        print(f'Daten erfolgreich in MongoDB eingefügt.')
    except Exception as e:
        print(f'Fehler beim Einfügen in MongoDB: {e}')
    finally:
        client.close()
