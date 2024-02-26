import file_reader_h5

if __name__ == "__main__":
    path = "../dataset"
    analyzer = file_reader_h5.HDF5Analyzer(path)

    dataset = analyzer.handle_file_reader()



