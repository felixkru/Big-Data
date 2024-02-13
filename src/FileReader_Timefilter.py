import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class HDF5Analyzer:

    def __init__(self, folder_path):
        self.folder_path = folder_path

    def read_files(self):
        files = os.listdir(self.folder_path)
        for file in files:
            file_path = os.path.join(self.folder_path, file)
            if file.endswith('.h5'):
                self.extract_and_print_timestamps(file_path)

    def extract_and_print_timestamps(self, file_path):
        with h5py.File(file_path, 'r') as hdf:
            print(f"Auslesen der Zeitstempel für Datei: {file_path}")
            for name in hdf:
                self.inspect_group(hdf[name], name_prefix=name)

    def inspect_group(self, item, name_prefix=''):
        if isinstance(item, h5py.Dataset):
            # Sie könnten spezifische Schlüsselnamen prüfen, die auf Zeitstempel hinweisen
            if 'time' in name_prefix.lower() or 'timestamp' in name_prefix.lower():
                print(f"Zeitstempel gefunden in: {name_prefix}, Daten: {item[:]}")
        elif isinstance(item, h5py.Group):
            for name in item:
                self.inspect_group(item[name], name_prefix=f"{name_prefix}/{name}")

    #dates = [datetime.utcfromtimestamp(ts) for ts in gesammelte_daten]

    # Visualisierung der Zeitstempel
    #plt.figure(figsize=(10, 6))
    #plt.plot(dates, np.arange(len(dates)))  # Erzeugt eine einfache Linie, die jede Zeitmarke darstellt
    #plt.xlabel('Zeit')
    #plt.ylabel('Index')
    #plt.title('Zeitstempel Visualisierung')
    #plt.xticks(rotation=45)
    #plt.tight_layout()
    #plt.show()

# Nutzung:
if __name__ == "__main__":
    analyzer = HDF5Analyzer('A:/Program Files/Git/Big-Data/dataset')
    analyzer.read_files()