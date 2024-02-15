import h5py
from datetime import datetime, timezone
from dateutil import parser
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter


class Visualize_Organized_Timestamps:

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.all_timestamps = []
        self.timestamps_by_decade = {}

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
            if 'time' in name_prefix.lower() or 'timestamp' in name_prefix.lower():
                print(f"Zeitstempel gefunden in: {name_prefix}, Daten: {item[:]}")

                for ts in item[:]:

                    try:
                        ts_converted = datetime.fromtimestamp(int(ts), timezone.utc)
                    except (ValueError, TypeError):

                        try:
                            ts_str = ts.decode('utf-8')
                            ts_converted = parser.parse(ts_str)
                        except (ValueError, TypeError, AttributeError):
                            print(f"Unlesbarer Zeitstempel: {ts} in {item.name}")
                            continue

                        try:
                            ts_converted = parser.parse(ts_str)
                        except (ValueError, TypeError, AttributeError):
                            print(f"Unlesbarer Zeitstempel: {ts} in {item.name}")
                            continue

                        decade = (ts_converted.year // 10) * 10
                        if decade not in self.timestamps_by_decade:
                            self.timestamps_by_decade[decade] = []

                        self.timestamps_by_decade[decade].append(ts_converted)

                    self.all_timestamps.append(ts_converted)

        elif isinstance(item, h5py.Group):
            for name in item:
                self.inspect_group(item[name], name_prefix=f"{name_prefix}/{name}")

    def visualize_timestamps_by_decade(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = plt.cm.jet(np.linspace(0, 1, len(self.timestamps_by_decade)))  # Farbpalette

        for (decade, timestamps), color in zip(sorted(self.timestamps_by_decade.items()), colors):
            dates = [ts.replace(tzinfo=None) for ts in timestamps]  # Entferne Zeitzone für Plotting
            counts = list(range(len(dates)))  # Einfache Zählvariable für Y-Achse

            ax.plot(dates, counts, marker='o', linestyle='-', color=color, label=str(decade))

        ax.set_xlabel('Datum')
        ax.set_ylabel('Anzahl der Zeitstempel')
        ax.set_title('Zeitstempel pro Jahrzehnt')
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        plt.legend(title='Jahrzehnt')
        plt.tight_layout()
        plt.show()

# Nutzung:
if __name__ == "__main__":
        analyzer = Visualize_Organized_Timestamps('A:/Program Files/Git/Big-Data/dataset')
        analyzer.read_files()
        analyzer.visualize_timestamps_by_decade()