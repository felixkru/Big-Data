import datetime

import numpy as np
import pymongo

import mongoConnection


def jahreszahl_ermitteln():
    updates = []
    bulk_operations = []
    query_result = mongoConnection.read_data_from_mongo({}, "european_dolphins")
    for dataset in query_result:
        mean = np.median(dataset["timestamp"])
        datum = datetime.datetime.utcfromtimestamp(mean)

        jahreszahl = datum.year

        db_filter = {"file_name": dataset["file_name"]}
        update = {"$set": {"year": jahreszahl}}

        updates.append((db_filter, update))

    for db_filter, update in updates:
        operation = pymongo.UpdateOne(db_filter, update)
        bulk_operations.append(operation)

    mongoConnection.bulk_update_mongo(bulk_operations, "european_dolphins")


jahreszahl_ermitteln()