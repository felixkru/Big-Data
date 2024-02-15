import os
import h5py
from datetime import datetime, timezone
from dateutil import parser
import csv


class Export_Grouped_Timestamps_To_CSV:

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

    def write_timestamps_to_csv_by_decade(self, output_folder):
        for decade, timestamps in sorted(self.timestamps_by_decade.items()):
            filename = os.path.join(output_folder, f'timestamps_{decade}s.csv')
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Index', 'Datum', 'Jahrzehnt'])
                for index, dt in enumerate(timestamps):
                    dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerow([index, dt_str, str(decade)])


# Nutzung:
if __name__ == "__main__":
    analyzer = Export_Grouped_Timestamps_To_CSV('A:/Program Files/Git/Big-Data/dataset')
    analyzer.read_files()

    output_folder = 'A:/Program Files/Git/Big-Data/Ausgabe'
    os.makedirs(output_folder, exist_ok=True)
    analyzer.write_timestamps_to_csv_by_decade(output_folder)
