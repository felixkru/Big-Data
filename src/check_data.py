import datetime
import numpy as np


class CheckData:

    def __init__(self):
        pass

    @staticmethod
    def check_sub_set_timestamp(data_set):
        for group_set in data_set:
            for group in group_set:
                if 'time' in group.group:
                    timestamp = CheckData.handle_timestamp(group.data)
                    group.group = timestamp
        return data_set

    @staticmethod
    def handle_timestamp(timestamps):
        dates = []
        for timestamp in timestamps:
            try:
                if isinstance(timestamp, bytes):
                    try:
                        timestamp_str = timestamp.decode('utf-8')
                        timestamp_float = float(timestamp_str)
                    except UnicodeDecodeError:
                        continue

                elif isinstance(timestamp, np.float64):
                    timestamp_float = float(timestamp)

                else:
                    print("Ungültiger Zeitstempel-Format:", timestamp)
                    continue

                date = datetime.datetime.fromtimestamp(timestamp_float)
                dates.append(date)
            except Exception as e:
                print("Fehler beim Konvertieren eines Zeitstempels:", e)
        return dates

    @staticmethod
    def calculate_velocity(data_timestamp, data_distance):
        velocity = data_timestamp - data_distance

    @staticmethod
    def check_array_length(array):
        if len(array) == 1000:
            return array
        else:
            print("Zu wenig Daten in dem Array!")
            return []
