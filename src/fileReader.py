import os
import h5py


class HDF5Analyzer:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def analyze_files(self):
        files = files = os.listdir(self.folder_path)
        for file_name in files:
            file_path = os.path.join(self.folder_path, file_name)
            if file_name.endswith('.h5') and os.path.isfile(file_path):
                try:
                    with h5py.File(file_path, 'r') as file:
                        print(f"Struktur der Datei {file_path}:")
                        self._explore_group(file)
                except Exception as e:
                    print(f"Fehler beim Analysieren der Datei {file_path}: {str(e)}")

    def _explore_group(self, group, indent=0):
        for name, item in group.items():
            if isinstance(item, h5py.Group):
                print("  " * indent + f"Group: {name}")
                self._explore_group(item, indent + 1)
            elif isinstance(item, h5py.Dataset):
                print("  " * indent + f"Dataset: {name}")

    #TODO analyse der Unterordner einer H5 Datei.