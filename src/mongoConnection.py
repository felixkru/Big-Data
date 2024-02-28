from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def send_data_to_mongo(processed_datasets):
    uri = "mongodb+srv://felixkruse:FXq82hcEQSH5bNmR@cluster0.bkat9hf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client['Big-D']
    collection = database['Measurements']

    false_dataset_counter = 0
    for item in processed_datasets:
        if not isinstance(item, dict):
            false_dataset_counter += 1
    print(false_dataset_counter)

    try:
        collection.insert_many(processed_datasets)
        print(f'Daten erfolgreich in MongoDB eingefügt: {processed_datasets}')
    except Exception as e:
        print(f'Fehler beim Einfügen in MongoDB: {e}')
    finally:
        client.close()