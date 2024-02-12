import fileReader

folder_path = "dataset"

if __name__ == "__main__":

    analyzer = fileReader.HDF5Analyzer(folder_path)
    analyzer.read_files()
