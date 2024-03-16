import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = ""


def send_data_to_mongo(processed_datasets, collection):
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client['Big-D']
    collection = database[collection]
    try:
        collection.insert_many(processed_datasets)

        print(f'Daten erfolgreich in MongoDB eingefügt.')
    except Exception as e:
        print(f'Fehler beim Einfügen in MongoDB: {e}')
    finally:
        client.close()


def read_data_from_mongo(query=None, collection="raw_measurements"):
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client['Big-D']
    collection = database[collection]
    query_result = []
    if query is None:
        query = {}
    try:
        for document in collection.find(query):
            query_result.append(document)
        print(f'Daten erfolgreich gelesen.')
        return query_result
    except Exception as e:
        print(f'Fehler beim lesen der Daten: {e}')
        return None
    finally:
        client.close()


def count_data_from_mongo(query=None, collection="raw_measurements"):
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client['Big-D']
    collection = database[collection]
    if query is None:
        query = {}
    try:
        query_result = collection.count_documents(query)
        print(f'Daten erfolgreich gezählt.')
        return query_result
    except Exception as e:
        print(f'Fehler beim lesen der Daten: {e}')
        return None
    finally:
        client.close()


def update_data_from_mongo(file=None, input_data=None, collection="raw_measurements"):
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client['Big-D']
    collection = database[collection]
    db_filter = file
    update = input_data
    if file or input_data is None:
        pass
    try:
        collection.update_one(db_filter, update)
        print(f"Datei erfolgreich geupdated: {file}")
    except Exception as e:
        print(f'Fehler beim updaten der Datei: {e}')
        return None
    finally:
        client.close()


def bulk_update_mongo(updates, collection="raw_measurements"):
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client['Big-D']
    collection = database[collection]
    try:
        collection.bulk_write(updates)
        print("Dateien erfolgreich geupdated")
    except Exception as e:
        print(f'Fehler beim updaten der Dateien: {e}')
        return None
    finally:
        client.close()
