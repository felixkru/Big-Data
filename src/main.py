import file_reader_h5
from src import visualization_handler

if __name__ == "__main__":
    # Initialisierungen
    visualization_handler = visualization_handler.VisualizationHandler
    path = "../test"
    analyzer = file_reader_h5.HDF5Analyzer(path)

    #Logik
    dataset = analyzer.handle_file_reader()
    visualization_handler.handle_scatter_chart_with_multiple_arguments(dataset[0])
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
#query_content = mongoConnection.read_data_from_mongo({"timestamp": ""})

#for data in query_content:
    #print(data['file_name'])
