import os
import h5py
from check_data import CheckData


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
            file_name = HDF5Analyzer.create_file_name(file)
            single_dataset = {
                "file_id": current_file_id,
                "file_name": file_name,
                "region": "",
                "instrument": "",
                "defect_channel": "",
                "wall_thickness": "",
                "magnetization": "",
                "distance": "",
                "timestamp": "",
                "velocity": ""
            }

            with h5py.File(file, 'r') as h5py_file:

                keys = list(h5py_file.keys())
                if 'data' in keys or 'Daten' in keys:
                    for key in keys:
                        region, instrument = HDF5Analyzer.return_file_attributes(h5py_file[key].attrs.items())
                        single_dataset["region"] = region
                        single_dataset["instrument"] = instrument

                        sub_group_data_set = []
                        for sub_group in h5py_file[key]:
                            data = h5py_file[key][sub_group][()]
                            complete_set = {sub_group: data}
                            sub_group_data_set.append(complete_set)

                        for item in sub_group_data_set:
                            if 'defect_channel' in item:
                                checked_value = CheckData.parse_type_to_float(item['defect_channel'])
                                single_dataset["defect_channel"] = list(checked_value)

                            if 'wall_thickness' in item or 'WALL_THICKNESS' in item or 'wall_thickness_' in item:
                                if 'wall_thickness' in item:
                                    checked_value = CheckData.parse_type_to_float(item['wall_thickness'])
                                    if len(checked_value) != 1000:
                                        checked_value = CheckData.handle_ascii_string(item['wall_thickness'])

                                        if len(checked_value) == 0:
                                            checked_value = CheckData.handel_byte_string(item['wall_thickness'])

                                            if len(checked_value) == 0:
                                                checked_value = CheckData.handle_easter_egg(item['wall_thickness'], file_name)

                                if 'WALL_THICKNESS' in item:
                                    checked_value = CheckData.parse_type_to_float(item['WALL_THICKNESS'])
                                    if len(checked_value) != 1000:
                                        checked_value = CheckData.handle_ascii_string(item['WALL_THICKNESS'])
                                        if len(checked_value) == 0:
                                            checked_value = CheckData.handel_byte_string(item['WALL_THICKNESS'])

                                            if len(checked_value) == 0:
                                                checked_value = CheckData.handle_easter_egg(item['WALL_THICKNESS'], file_name)

                                if 'wall_thickness_' in item:
                                    checked_value = CheckData.parse_type_to_float(item['wall_thickness_'])
                                    if len(checked_value) != 1000:
                                        checked_value = CheckData.handle_ascii_string(item['wall_thickness_'])

                                        if len(checked_value) == 0:
                                            checked_value = CheckData.handel_byte_string(item['wall_thickness_'])

                                            if len(checked_value) == 0:
                                                checked_value = CheckData.handle_easter_egg(item['wall_thickness_'], file_name)

                                single_dataset["wall_thickness"] = list(checked_value)

                            if 'magnetization' in item:
                                checked_value = CheckData.parse_type_to_float(item['magnetization'])

                                if len(checked_value) != 1000:
                                    checked_value = CheckData.handle_ascii_string(item['magnetization'])

                                    if len(checked_value) == 0:
                                        checked_value = CheckData.handel_byte_string(item['magnetization'])

                                        if len(checked_value) == 0:
                                            checked_value = CheckData.handle_easter_egg(item['magnetization'], file_name)

                                single_dataset["magnetization"] = list(checked_value)

                            if 'distance' in item or 'distance_' in item or 'DISTANCE' in item:
                                if 'distance' in item:
                                    checked_value = CheckData.parse_type_to_float(item['distance'])
                                    if len(checked_value) != 1000:
                                        checked_value = CheckData.handle_ascii_string(item['distance'])

                                elif 'distance_' in item:
                                    checked_value = CheckData.parse_type_to_float(item['distance_'])

                                elif 'DISTANCE' in item:
                                    checked_value = CheckData.parse_type_to_float(item['DISTANCE'])

                                single_dataset["distance"] = list(checked_value)

                            if 'timestamp' in item or 'TIMESTAMP' in item or 'timestamp_' in item:
                                if 'timestamp' in item:
                                    checked_value = CheckData.parse_type_to_float(item['timestamp'])
                                    if len(checked_value) != 1000:
                                        checked_value = CheckData.convert_datetime_to_float(item['timestamp'], file_name)

                                if 'TIMESTAMP' in item:
                                    checked_value = CheckData.parse_type_to_float(item['TIMESTAMP'])
                                    if len(checked_value) != 1000:
                                        checked_value = CheckData.convert_datetime_to_float(item['TIMESTAMP'], file_name)

                                if 'timestamp_' in item:
                                    checked_value = CheckData.parse_type_to_float(item['timestamp_'])
                                    if len(checked_value) != 1000:
                                        checked_value = CheckData.convert_datetime_to_float(item['timestamp_'], file_name)
                                single_dataset["timestamp"] = list(checked_value)

                            if 'velocity' in item or 'VELOCITY' in item or 'velocity_' in item:
                                if 'velocity' in item:
                                    checked_value = CheckData.parse_type_to_float(item['velocity'])

                                if 'Velocity' in item:
                                    checked_value = CheckData.parse_type_to_float(item['Velocity'])

                                if 'velocity_' in item:
                                    checked_value = CheckData.parse_type_to_float(item['velocity_'])

                                single_dataset["velocity"] = list(checked_value)

            current_file_id += 1
            all_data.append(single_dataset)
        return all_data

    def handle_file_reader(self):
        folder_paths = self.open_file_and_create_path()
        return self.open_h5_files_and_return_file_data(folder_paths)

    @staticmethod
    def create_file_name(file_path):
        return os.path.splitext(os.path.basename(file_path))[0]

    @staticmethod
    def return_file_attributes(file):

        region_attribute = ""
        instrument_attribute = ""

        for item in file:
            if item[0] == 'configuration':
                region_attribute = item[1]
            elif item[0] == 'instrument':
                instrument_attribute = item[1]

        return region_attribute, instrument_attribute

    @staticmethod
    def set_full_distance_for_each_set(distance_dataset, filename):
        try:
            full_distance = distance_dataset['distance'][-1]
            distance_dataset['full_distance'] = full_distance

            return distance_dataset
        except ValueError as e:
            print("Es konnte keine maximale Distanz ermittelt werden: ", filename)
            return distance_dataset

    @staticmethod
    def handle_set_full_distance(datasets):
        new_set = []
        for data_set in datasets:
            new_set.append(HDF5Analyzer.set_full_distance_for_each_set(data_set, data_set['file_name']))
        return new_set


if __name__ == "__main__":
    path = "../test"
    analyzer = HDF5Analyzer(path)
    dataset = HDF5Analyzer.open_h5_files_and_return_file_data(analyzer.open_file_and_create_path())
