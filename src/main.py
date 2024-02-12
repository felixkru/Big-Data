import fileReader
import check_data

folder_path = '../dataset/'
analyzer = fileReader.HDF5Analyzer(folder_path)
file_counter = check_data.CheckData(folder_path)

counted_files_in_directory = file_counter.count_files()
counted_h5_files = analyzer.count_files_in_schema()
sets = analyzer.read_h5_files_data()


def print_all_data_sets(all_data_sets_list):
    for item in all_data_sets_list:
        print(f"Data ID: {item.data_id}")
        print(f"DataSet Name: {item.data.name}")
        print(f"DataSet Data: {item.data.data}")
        print("=" * 30)


#print_all_data_sets(sets)
print(counted_h5_files)
print(counted_files_in_directory)
