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

                        for sub_group in h5py_file[key]:
                            data = h5py_file[key][sub_group][()]
                            sub_group_data = SubGroupData(sub_group, data)

            current_file_id += 1
            all_data.append(dataset_from_file)
            print(all_data)
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


if __name__ == "__main__":
    path = "../test"
    analyzer = HDF5Analyzer(path)
    dataset = HDF5Analyzer.open_h5_files_and_return_file_data(analyzer.open_file_and_create_path())
