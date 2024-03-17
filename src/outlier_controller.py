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

    query_content = mongoConnection.read_data_from_mongo({
        "region": {"$in": ["Europe"]},
        "instrument": {"$in": ["Dolphin"]},
        "file_name": "1f91871f-95d9-4715-bc3d-4b152870be02"
    }, "european_dolphins")

    for element in query_content:
        try:
            x = np.array(element["timestamp"])
            y = np.array(element["velocity"])
            plt.scatter(x, y)
            plt.show()

            y = np.array(element["velocity_clean"])
            plt.scatter(x, y)
            plt.show()

        except Exception as e:
            print(f"Error: {e}")

    # path = "../dataset"
    # analyzer = file_reader_h5.HDF5Analyzer(path)
    # dataset = analyzer.handle_file_reader()

    """
    query_content = mongoConnection.read_data_from_mongo({
        "region": {"$in": ["Europe"]},
        "instrument": {"$in": ["Dolphin"]},
        "file_name": "1f91871f-95d9-4715-bc3d-4b152870be02"
    }, "european_dolphins")
    print(query_content[0]["wall_thickness"])
    x = np.array(query_content[0]["timestamp"])
    y = np.array(query_content[0]["magnetization"])
    y_new = np.array(OutlierHandler.tukeys_detection(query_content[0]["magnetization"]))
    """
"""
    mongoConnection.send_data_to_mongo(dataset)
"""
"""
    query_counter_result = mongoConnection.count_data_from_mongo({"region": "Africa"})
    print(f"Soviele Datensätze entsprechen deinem Query: {query_counter_result}")

    query_content = mongoConnection.read_data_from_mongo({"file_id": 312})
    print(query_content)
"""
"""So kann man z.B. die namen der datensätze ermitteln bei denen dein query zu trifft."""
"""
query_content = mongoConnection.count_data_from_mongo({
    "region": {"$in": ["Europe"]},
    "instrument": {"$in": ["Dolphin"]}
}, "european_dolphins")
print(query_content)
"""
"""
for data in query_content:
    print(data['file_name'])
"""
