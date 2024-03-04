from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = ""


def send_data_to_mongo(processed_datasets):
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client['Big-D']
    collection = database['raw_measurements_v2']
    try:
        collection.insert_many(processed_datasets)

        print(f'Daten erfolgreich in MongoDB eingefügt.')
    except Exception as e:
        print(f'Fehler beim Einfügen in MongoDB: {e}')
    finally:
        client.close()


def read_data_from_mongo(query=None):
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client['Big-D']
    collection = database['raw_measurements']
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


def count_data_from_mongo(query=None):
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client['Big-D']
    collection = database['raw_measurements']
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
