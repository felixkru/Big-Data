import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pymongo
from calculate_location_parameters import CalculateLocationParameters
from outlierhandler import OutlierHandler
import file_reader_h5
import mongoConnection


def handle_outliers_and_prepare_for_db_push():
    updates = []
    bulk_operations = []
    query_content = mongoConnection.read_data_from_mongo({}, "asian_dolphins")

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


def calculate_median_and_average_and_write_to_db():
    query = {}
    collection = "european_dolphins"
    updates = []
    bulk_operations = []

    results = mongoConnection.read_data_from_mongo(query, collection)

    new_set = CalculateLocationParameters.handle_update_average_and_median_calculation_without_outliers(results)

    for index, element in enumerate(results):
        db_filter = {"file_name": element["file_name"]}
        update = {
            "$set": {
                "velocity_median": new_set[index]["velocity_median"],
                "velocity_average": new_set[index]["velocity_average"],
                "magnetization_median": new_set[index]["magnetization_median"],
                "magnetization_average": new_set[index]["magnetization_average"],
                "wall_thickness_median": new_set[index]["wall_thickness_median"],
                "wall_thickness_average": new_set[index]["wall_thickness_average"],
            }
        }
        updates.append((db_filter, update))

    for db_filter, update in updates:
        operation = pymongo.UpdateOne(db_filter, update)
        bulk_operations.append(operation)

    return bulk_operations


if __name__ == "__main__":
    bulk_operations = handle_outliers_and_prepare_for_db_push()
    mongoConnection.bulk_update_mongo(bulk_operations, "asian_dolphins")
