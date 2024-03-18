import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pymongo

from outlierhandler import OutlierHandler
import file_reader_h5
import mongoConnection


def handle_outliers_and_prepare_for_db_push():
    updates = []
    bulk_operations = []
    query_content = mongoConnection.read_data_from_mongo({
        "region": {"$in": ["Europe"]},
        "instrument": {"$in": ["Dolphin"]}
    }, "european_dolphins")

    for element in query_content:
        db_filter = {"file_name": element["file_name"]}
        try:
            cleaned_array = OutlierHandler.tukeys_detection(element["magnetization_straightened"])
            cleaned_array = list(cleaned_array)
            update = {"$set": {"magnetization_straightened_clean": cleaned_array}}
            updates.append((db_filter, update))
        except Exception as e:
            print(f"Error while outlier detection: {e}")
            continue
        try:
            cleaned_array = OutlierHandler.tukeys_detection(element["wall_thickness"])
            cleaned_array = list(cleaned_array)
            update = {"$set": {"wall_thickness_clean": cleaned_array}}
            updates.append((db_filter, update))
        except Exception as e:
            print(f"Error while outlier detection: {e}")
            continue
        try:
            cleaned_array = OutlierHandler.tukeys_detection(element["distance"])
            cleaned_array = list(cleaned_array)
            update = {"$set": {"distance_clean": cleaned_array}}
            updates.append((db_filter, update))
        except Exception as e:
            print(f"Error while outlier detection: {e}")
            continue
        try:
            if len(element["calculated_velocity"]) != 0:
                cleaned_array = OutlierHandler.tukeys_detection(element["calculated_velocity"])
                cleaned_array = list(cleaned_array)
            else:
                cleaned_array = OutlierHandler.tukeys_detection(element["velocity"])
                cleaned_array = list(cleaned_array)

            update = {"$set": {"velocity_clean": cleaned_array}}
            updates.append((db_filter, update))

        except Exception as e:
            print(f"Error while outlier detection: {e}")
            continue
    for db_filter, update in updates:
        operation = pymongo.UpdateOne(db_filter, update)
        bulk_operations.append(operation)
    return bulk_operations


if __name__ == "__main__":

    bulk_operations = handle_outliers_and_prepare_for_db_push()
    mongoConnection.bulk_update_mongo(bulk_operations, "european_dolphins")
