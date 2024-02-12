import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import outlier_handler as oh


class HDF5Analyzer:

    def __init__(self, folder_path):
        self.folder_path = folder_path

    def read_files(self):
        files = os.listdir(self.folder_path)
        for file in files:
            file_path = os.path.join(self.folder_path, file)
            if file.endswith('.h5'):
                self.read_h5_files_data(file_path)

    def read_h5_files_data(self, file_path):
        with h5py.File(file_path, 'r') as hdf:
            key_view = hdf.keys()
            key = 'data' if 'data' in key_view else ''
            if key != '':
                data_group = hdf[key]
                for member_name in data_group:
                    member = data_group[member_name]
                    if isinstance(member, h5py.Dataset):
                        data = np.array(member[:])
                        oh_detector = oh.outlier_handler(data)
                        oh_detector.tukeys_detection()
                        self.visualize_data(data, member_name)
                        self.visualize_data(oh_detector.zscore_detection(), member_name)
                        self.visualize_data(oh_detector.tukeys_detection(), member_name)


    def visualize_data(self, data, member_name):
        plt.plot(data)
        plt.title(f"Visualisierung für {member_name}")
        plt.show()
