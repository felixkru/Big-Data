import file_reader_h5
import mongoConnection


if __name__ == "__main__":
    path = "../dataset"
    analyzer = file_reader_h5.HDF5Analyzer(path)
    dataset = analyzer.handle_file_reader()
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
query_content = mongoConnection.count_data_from_mongo({
    "region": {"$in": ["Europe"]},
    "instrument": {"$in": ["Elephant"]}
}, "raw_measurements_v2")
print(query_content)
"""
for data in query_content:
    print(data['file_name'])
"""
