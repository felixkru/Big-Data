import os
import h5py

class HDF5Analyzer:

    def __init__(self, folder_path):
        self.folder_path = folder_path

    def read_files(self):
        files = os.listdir(self.folder_path)
        for file in files:
            if file.endswith('.h5'):
                file_path = os.path.join(self.folder_path, file)
                self.extract_and_print_timestamps(file_path)

    def extract_and_print_timestamps(self, file_path):
        with h5py.File(file_path, 'r') as hdf:
            self.inspect_group(hdf)

    def inspect_group(self, item):
        if isinstance(item, h5py.Dataset):
            # Identifizieren von Datasets, die Zeitstempel enthalten könnten, basierend auf dem Namen
            if 'time' in item.name.lower() or 'timestamp' in item.name.lower():
                # Direkte Ausgabe der Daten der Zeitstempel
                print(item[:])
        elif isinstance(item, h5py.Group):
            for name in item:
                self.inspect_group(item[name])

# Nutzung:
if __name__ == "__main__":
    analyzer = HDF5Analyzer('A:/Program Files/Git/Big-Data/dataset')
    analyzer.read_files()