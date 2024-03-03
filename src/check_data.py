import datetime
import numpy as np


class CheckData:

    def __init__(self):
        pass

    @staticmethod
    def convert_float_to_date(timestamps):
        new_timestamps = []
        start_date = datetime.datetime(1970, 1, 1)

        for timestamp in timestamps:
            try:
                converted_timestamp = start_date + datetime.timedelta(seconds=timestamp)
                new_timestamps.append(converted_timestamp)
            except Exception as error:
                print("Can't convert to Date:", timestamp)
                print("Error:", error)

        return new_timestamps

    @staticmethod
    def check_array_length(array):
        if len(array) == 1000:
            return array
        else:
            print("Zu wenig Daten in dem Array!")
            return []

    @staticmethod
    def parse_type_to_float(data):
        try:
            return np.frombuffer(data, dtype=np.float64)
        except ValueError as e:
            print("ValueError:", e)
            return []

    @staticmethod
    def calculate_velocity_from_time_and_distance(distances, velocities, timestamps):
        if len(timestamps['timestamp']) == 1000 and len(distances['distance']) == 1000:
            complete_velocity = []

            for index, timestamp in enumerate(timestamps['timestamp']):
                distance = distances['distance'][index]
                timestamp = timestamps['timestamp'][index]

                if index < len(velocities['velocity']):
                    velocity = velocities['velocity'][index]
                    complete_velocity.append(velocity)

                else:
                    time_difference = timestamp - timestamps['timestamp'][index - 1]
                    distance_difference = (distance - distances['distance'][index - 1])
                    velocity = distance_difference / time_difference * 1000
                    complete_velocity.append(velocity)

            return complete_velocity
