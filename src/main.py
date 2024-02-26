import check_data
import file_reader_h5

if __name__ == "__main__":
    path = "../dataset"
    analyzer = file_reader_h5.HDF5Analyzer(path)
    data_check = check_data.CheckData()

    dataset = analyzer.handle_file_reader()
    # Folgendes Datenschema wird zurückgegeben. dataset:Array:Array:Object
    data_check.check_sub_set_timestamp(dataset)


