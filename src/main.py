import check_data
import file_reader_h5

folder_path = '../dataset/'
analyzer = file_reader_h5.HDF5Analyzer(folder_path)
file_counter = check_data.CheckData(folder_path)


