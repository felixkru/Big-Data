import file_reader_h5
import check_data
#import mongoConnection
from calculate_location_parameters import CalculateLocationParameters


def handle_file_reader_and_write_to_database():
    path = "../test"
    collection = "complete_dataset"
    analyzer = file_reader_h5.HDF5Analyzer(path)
    dataset = analyzer.handle_file_reader()

    # Bei dem dataset_with_velocity gibt es noch Probleme durch die Umwandulng des Timestamps
    dataset_with_velocity = check_data.CheckData.calculate_velocity_from_time_and_distance(dataset)

    # Bei der Berechnung der statistischen Werte gibt es noch Probleme durch die falschen Timstamps
    dataset_with_statistic_parameters = CalculateLocationParameters.handle_update_average_and_median_calculation(dataset_with_velocity)
    full_dataset = analyzer.handle_set_full_distance(dataset_with_statistic_parameters)

    #mongoConnection.send_data_to_mongo(full_dataset, collection)


if __name__ == "__main__":
    """
    Die Funktion verarbeitet das komplette Datenset
    """
    handle_file_reader_and_write_to_database()

"""
    query_counter_result = mongoConnection.count_data_from_mongo({"region": "Africa"})
    print(f"Soviele Datensätze entsprechen deinem Query: {query_counter_result}")

    #mongoConnection.send_data_to_mongo(dataset)


    #query_counter_result = mongoConnection.count_data_from_mongo({"region": "Africa"})
    #print(f"Soviele Datensätze entsprechen deinem Query: {query_counter_result}")

    #query_content = mongoConnection.read_data_from_mongo({"file_id": 312})
    #print(query_content)

    So kann man z.B. die namen der datensätze ermitteln bei denen dein query zu trifft."""
"""

So kann man z.B. die namen der datensätze ermitteln bei denen dein query zu trifft.

query_content = mongoConnection.count_data_from_mongo({
    "region": {"$in": ["Europe"]},
    "instrument": {"$in": ["Elephant"]}
}, "raw_measurements_v2")
print(query_content)


for data in query_content:
    print(data['file_name'])
    """
