import file_reader_h5
import check_data
import mongoConnection
from calculate_location_parameters import CalculateLocationParameters

if __name__ == "__main__":
    path = "../test"
    analyzer = file_reader_h5.HDF5Analyzer(path)
    dataset = analyzer.handle_file_reader()
    dataset_with_velocity = check_data.CheckData.calculate_velocity_from_time_and_distance(dataset)
    #full_dataset = CalculateLocationParameters.handle_update_average_and_median_calculation(dataset)
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
#query_content = mongoConnection.count_data_from_mongo({
    "region": {"$in": ["Europe"]},
    "instrument": {"$in": ["Elephant"]}
})
print(query_content)
"""
#for data in query_content:
#   print(data['file_name'])
"""
