import fileReader

folder_path = '../dataset/'
analyzer = fileReader.HDF5Analyzer(folder_path)
analyzer.analyze_files()
combined_data = analyzer.get_combined_data()
print(combined_data)
