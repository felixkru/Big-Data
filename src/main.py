import file_reader_h5
import mongoConnection


if __name__ == "__main__":
    path = "../test"
    analyzer = file_reader_h5.HDF5Analyzer(path)

    dataset = analyzer.handle_file_reader()

    mongoConnection.send_data_to_mongo(dataset)




