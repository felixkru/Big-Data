import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timezone
from dateutil import parser
import csv


class HDF5Analyzer:

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.all_timestamps = []

    def read_files(self):
        files = os.listdir(self.folder_path)
        for file in files:
            file_path = os.path.join(self.folder_path, file)
            if file.endswith('.h5'):
                self.extract_and_print_timestamps(file_path)
        self.visualize_timestamps()

    def extract_and_print_timestamps(self, file_path):
        with h5py.File(file_path, 'r') as hdf:
            print(f"Auslesen der Zeitstempel für Datei: {file_path}")
            for name in hdf:
                self.inspect_group(hdf[name], name_prefix=name)

    def inspect_group(self, item, name_prefix=''):
        if isinstance(item, h5py.Dataset):
            # add --> spezifische Schlüsselnamen prüfen, die auf Zeitstempel hinweisen
            if 'time' in name_prefix.lower() or 'timestamp' in name_prefix.lower():
                print(f"Zeitstempel gefunden in: {name_prefix}, Daten: {item[:]}")

                # Hier wird für jedes Element in item geprüft und konvertiert
                for ts in item[:]:

                    try:
                        # Versuche, als Unix-Zeitstempel zu interpretieren
                        ts_converted = datetime.fromtimestamp(int(ts), timezone.utc)
                    except (ValueError, TypeError):

                        # Falls das fehlschlägt, verarbeite als ISO-Format String
                        try:
                            ts_str = ts.decode('utf-8')  # Funktioniert nur, wenn ts ein Bytes-Objekt ist
                            ts_converted = parser.parse(ts_str)
                        except (ValueError, TypeError, AttributeError):
                            print(f"Unlesbarer Zeitstempel: {ts} in {item.name}")
                            continue

                    self.all_timestamps.append(ts_converted)

        elif isinstance(item, h5py.Group):
            for name in item:
                self.inspect_group(item[name], name_prefix=f"{name_prefix}/{name}")

    def visualize_timestamps(self):
        dates = [dt.replace(tzinfo=None) for dt in self.all_timestamps]

        # Einfacher Plot: Datum gegen Index
        plt.figure(figsize=(10, 6))
        plt.plot(dates, np.arange(len(dates)), marker='o', linestyle='-')
        plt.xlabel('Datum')
        plt.ylabel('Zeitstempel Index')
        plt.title('Visualisierung der gefundenen Zeitstempel')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def write_timestamps_to_csv(self, filepath):
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(['Index', 'Datum'])

            for index, dt in enumerate(self.all_timestamps):
                dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow([index, dt_str])


# Nutzung:
if __name__ == "__main__":
    analyzer = HDF5Analyzer('A:/Program Files/Git/Big-Data/dataset')
    analyzer.read_files()
    analyzer.write_timestamps_to_csv('A:/Program Files/Git/Big-Data/Ausgabe/timestamp.csv')
