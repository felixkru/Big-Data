import os
import h5py
import numpy as np
import matplotlib.pyplot as plt


class DataSet:
    def __init__(self, name, data):
        self.name = name
        self.data = data


class AllDataSets:
    def __init__(self, data_id, data):
        self.data_id = data_id
        self.data = data


class HDF5Analyzer:

    def __init__(self, folder_path):
        self.folder_path = folder_path

    def create_path(self):
        return os.listdir(self.folder_path)

    def read_h5_files_data(self):
        files = self.create_path()
        counter = -1
        all_data_sets_list = []
        for file in files:
            file_path = os.path.join(self.folder_path, file)
            if file.endswith('.h5'):
                with h5py.File(file_path, 'r') as hdf:
                    key_view = hdf.keys()
                    key = 'data' if 'data' in key_view else ''
                    if key != '':
                        data_group = hdf[key]
                        counter += 1
                        for member_name in data_group:
                            member = data_group[member_name]
                            if isinstance(member, h5py.Dataset):
                                data = np.array(member[:])
                                data_set = DataSet(member_name, data)
                                complete_set = AllDataSets(counter, data_set)
                                all_data_sets_list.append(complete_set)
        return all_data_sets_list

    def count_files_in_schema(self):
        counter = 0
        files = self.create_path()
        for file in files:
            file_path = os.path.join(self.folder_path, file)
            if file.endswith('.h5'):
                with h5py.File(file_path, 'r') as hdf:
                    key_view = hdf.keys()
                    key = 'data' if 'data' in key_view else ''
                    if key != '':
                        counter += 1
        return counter

    def visualize_data(self, data, member_name):
        plt.plot(data)
        plt.title(f"Visualisierung für {member_name}")
        plt.show()
