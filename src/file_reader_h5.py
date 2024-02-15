import os
import h5py


class SubGroupData:
    def __init__(self, group, data):
        self.group = group
        self.data = data


class HDF5Analyzer:

    def __init__(self, folder_path):
        self.folder_path = folder_path

    def create_path(self):
        return os.listdir(self.folder_path)

    def open_file_and_create_path(self):
        file_paths = []
        files_in_directory = self.create_path()
        for file in files_in_directory:
            if file.endswith('.h5'):
                file_path = os.path.join(self.folder_path, file)
                file_paths.append(file_path)
        return file_paths

    @staticmethod
    def open_h5_files_and_return_sub_group_data(file_paths):
        all_data = []
        complete_sub_data_set = []
        for file in file_paths:
            with h5py.File(file, 'r') as h5py_file:
                keys = list(h5py_file.keys())
                if 'data' in keys or 'Daten' in keys:
                    for key in keys:
                        for sub_group in h5py_file[key]:
                            data = h5py_file[key][sub_group][()]
                            sub_group_data = SubGroupData(sub_group, data)
                            complete_sub_data_set.append(sub_group_data)
            all_data.append(complete_sub_data_set)
            complete_sub_data_set = []
        return all_data

    def handle_file_reader(self):
        folder_paths = self.open_file_and_create_path()
        return self.open_h5_files_and_return_sub_group_data(folder_paths)


if __name__ == "__main__":
    path = "../dataset"
    analyzer = HDF5Analyzer(path)
    dataset = HDF5Analyzer.open_h5_files_and_return_sub_group_data(analyzer.open_file_and_create_path())
