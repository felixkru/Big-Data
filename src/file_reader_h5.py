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
        counter = 0

        for file in file_paths:
            single_dataset = {
                "file_id": current_file_id,
                "file_name": HDF5Analyzer.create_file_name(file),
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

                        data_preparation_and_conversion = []
                        count_calls_on_update_velocity = 0

                        for item in sub_group_data_set:

                            if 'defect_channel' in item:
                                checked_value = CheckData.check_array_length(item['defect_channel'])
                                checked_value = CheckData.parse_type_to_float(checked_value)
                                single_dataset["defect_channel"] = list(checked_value)

                            if 'wall_thickness' in item:
                                checked_value = CheckData.check_array_length(item['wall_thickness'])
                                checked_value = CheckData.parse_type_to_float(checked_value)
                                single_dataset["wall_thickness"] = list(checked_value)

                            if 'magnetization' in item:
                                checked_value = CheckData.check_array_length(item['magnetization'])
                                checked_value = CheckData.parse_type_to_float(checked_value)
                                single_dataset["magnetization"] = list(checked_value)

                            if 'distance' in item or 'distance_' in item or 'DISTANCE' in item:
                                if 'distance' in item:
                                    checked_value = CheckData.check_array_length(item['distance'])
                                    checked_value = CheckData.parse_type_to_float(checked_value)
                                elif 'distance_' in item:
                                    checked_value = CheckData.check_array_length(item['distance_'])
                                    checked_value = CheckData.parse_type_to_float(checked_value)
                                else:
                                    checked_value = CheckData.check_array_length(item['DISTANCE'])
                                    checked_value = CheckData.parse_type_to_float(checked_value)
                                distance = {'distance': checked_value}
                                data_preparation_and_conversion.append(distance)
                                single_dataset["distance"] = list(checked_value)

                            if 'timestamp' in item or 'TIMESTAMP' in item:
                                if 'timestamp' in item:
                                    checked_value = CheckData.check_array_length(item['timestamp'])
                                else:
                                    checked_value = CheckData.check_array_length(item['TIMESTAMP'])

                                checked_value = CheckData.parse_type_to_float(checked_value)
                                timestamp = {'timestamp': checked_value}
                                data_preparation_and_conversion.append(timestamp)
                                single_dataset["timestamp"] = list(checked_value)

                            if 'velocity' in item:
                                checked_value = CheckData.check_array_length(item['velocity'])
                                if len(checked_value) == 0:
                                    velocity = {'velocity': item['velocity']}
                                    data_preparation_and_conversion.append(velocity)
                                else:
                                    checked_value = CheckData.parse_type_to_float(checked_value)
                                    single_dataset["velocity"] = list(checked_value)

                            if 'Velocity' in item:
                                checked_value = CheckData.check_array_length(item['Velocity'])
                                if len(checked_value) == 0:
                                    velocity = {'velocity': item['Velocity']}
                                    data_preparation_and_conversion.append(velocity)
                                else:
                                    checked_value = CheckData.parse_type_to_float(checked_value)
                                    single_dataset["velocity"] = list(checked_value)

                            if len(data_preparation_and_conversion) == 3 and count_calls_on_update_velocity < 1:
                                count_calls_on_update_velocity += 1
                                data_for_calculation = HDF5Analyzer.handle_and_set_correct_attributes_for_velocity_calculation(data_preparation_and_conversion)
                                velocity = CheckData.calculate_velocity_from_time_and_distance(data_for_calculation[0], data_for_calculation[1], data_for_calculation[2])

                                if velocity is not None:
                                    single_dataset["velocity"] = list(velocity)

            current_file_id += 1
            all_data.append(single_dataset)
        return all_data

    def handle_file_reader(self):
        folder_paths = self.open_file_and_create_path()
        return self.open_h5_files_and_return_file_data(folder_paths)

    @staticmethod
    def handle_and_set_correct_attributes_for_velocity_calculation(data):
        response = [0, 0, 0]

        for data_set in data:

            if 'distance' in data_set:
                response[0] = {'distance': data_set['distance']}

            if 'velocity' in data_set:
                response[1] = {'velocity': data_set['velocity']}

            if 'timestamp' in data_set:
                response[2] = {'timestamp': data_set['timestamp']}

        return response

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
