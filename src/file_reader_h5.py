import os
import h5py
from check_data import CheckData
import numpy as np


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
    def open_h5_files_and_return_file_data(file_paths):
        current_file_id = 1
        all_data = []

        for file in file_paths:
            dataset_from_file = []

            file_id = {"file_id": current_file_id}
            dataset_from_file.append(file_id)

            filename = {"file_name": HDF5Analyzer.create_file_name(file)}
            dataset_from_file.append(filename)

            with h5py.File(file, 'r') as h5py_file:

                keys = list(h5py_file.keys())
                if 'data' in keys or 'Daten' in keys:
                    for key in keys:
                        attributes = HDF5Analyzer.return_file_attributes(h5py_file[key].attrs.items())
                        dataset_from_file.append(attributes[0])
                        dataset_from_file.append(attributes[1])

                        sub_group_data_set = []
                        for sub_group in h5py_file[key]:
                            data = h5py_file[key][sub_group][()]
                            complete_set = {sub_group: data}
                            sub_group_data_set.append(complete_set)

                        data_preparation_and_conversion = []
                        for item in sub_group_data_set:
                            if 'defect_channel' in item:
                                checked_value = CheckData.check_array_length(item['defect_channel'])
                                checked_value = HDF5Analyzer.parse_type_to_float(checked_value)
                                defect_channel = {'defect_channel': checked_value}
                                dataset_from_file.append(defect_channel)

                            if 'magnetization' in item:
                                checked_value = CheckData.check_array_length(item['magnetization'])
                                checked_value = HDF5Analyzer.parse_type_to_float(checked_value)
                                magnetization = {'magnetization': checked_value}
                                dataset_from_file.append(magnetization)

                            if 'distance' in item or 'distance_' in item or 'DISTANCE' in item:
                                if 'distance' in item:
                                    checked_value = CheckData.check_array_length(item['distance'])
                                    checked_value = HDF5Analyzer.parse_type_to_float(checked_value)
                                elif 'distance_' in item:
                                    checked_value = CheckData.check_array_length(item['distance_'])
                                    checked_value = HDF5Analyzer.parse_type_to_float(checked_value)
                                else:
                                    checked_value = CheckData.check_array_length(item['DISTANCE'])
                                    checked_value = HDF5Analyzer.parse_type_to_float(checked_value)
                                distance = {'distance': checked_value}
                                dataset_from_file.append(distance)

                            if 'velocity' in item:
                                checked_value = CheckData.check_array_length(item['velocity'])
                                if len(checked_value) == 0:
                                    velocity = {'velocity': item['velocity']}
                                    data_preparation_and_conversion.append(velocity)
                                else:
                                    checked_value = HDF5Analyzer.parse_type_to_float(checked_value)
                                    velocity = {'velocity': checked_value}
                                    dataset_from_file.append(velocity)

            current_file_id += 1
            all_data.append(dataset_from_file)
        return all_data

    def handle_file_reader(self):
        folder_paths = self.open_file_and_create_path()
        return self.open_h5_files_and_return_file_data(folder_paths)

    @staticmethod
    def create_file_name(file_path):
        return os.path.splitext(os.path.basename(file_path))[0]

    @staticmethod
    def return_file_attributes(file):
        attributes = []

        region_attribute = {"region": "None"}
        instrument_attribute = {"instrument": "None"}

        for item in file:
            if item[0] == 'configuration':
                region_attribute = {"region": item[1]}
            elif item[0] == 'instrument':
                instrument_attribute = {"instrument": item[1]}

        attributes.append(region_attribute)
        attributes.append(instrument_attribute)

        return attributes

    @staticmethod
    def parse_type_to_float(data):
        try:
            checked_value = np.frombuffer(data, dtype=np.float64)
            return checked_value
        except ValueError as e:
            print("ValueError:", e)


if __name__ == "__main__":
    path = "../test"
    analyzer = HDF5Analyzer(path)
    dataset = HDF5Analyzer.open_h5_files_and_return_file_data(analyzer.open_file_and_create_path())
