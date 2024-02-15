import check_data
import file_reader_h5

if __name__ == "__main__":
    path = "../dataset"
    analyzer = file_reader_h5.HDF5Analyzer(path)
    dataset = analyzer.handle_file_reader()
    # Folgendes Datenschema wird zurückgegeben. dataset:Array:Array:Object
    print(dataset[0][0].group)
    print(dataset[0][0].data)

