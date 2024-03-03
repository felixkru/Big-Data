import file_reader_h5
import mongoConnection


if __name__ == "__main__":
    path = "../dataset"
    ##analyzer = file_reader_h5.HDF5Analyzer(path)

    ##dataset = analyzer.handle_file_reader()

    query_counter_result = mongoConnection.count_data_from_mongo({"region": "Africa"})
    print(f"Soviele Datensätze entsprechen deinem Query: {query_counter_result}")

    query_content = mongoConnection.read_data_from_mongo({"file_id": 312})
    print(query_content)
