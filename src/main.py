import FileReader_Timefilter

folder_path = 'A:/Program Files/Git/Big-Data/dataset'
analyzer = FileReader_Timefilter.HDF5Analyzer(folder_path)
analyzer.analyze_files()
