import fileReader

folder_path = '../dataset/'
analyzer = fileReader.HDF5Analyzer(folder_path)
analyzer.read_files()
