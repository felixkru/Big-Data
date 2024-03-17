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
            return np.array([])

    @staticmethod
    def handle_ascii_string(array):
        new_array = []
        try:
            for data_set in array:
                float_number = float(data_set)
                new_array.append(float_number)
            return new_array
        except ValueError as e:
            return np.array([])

    @staticmethod
    def handel_byte_string(array):
        new_array = []
        try:
            for data_set in array:
                byte_string = data_set.decode('utf-8')
                float_number = float(byte_string)
                new_array.append(float_number)
            return new_array
        except ValueError as e:
            return np.array([])

    @staticmethod
    def handle_easter_egg(array, filename):
        new_array = []
        for data_set in array:
            try:
                byte_string = data_set.decode('utf-8')
                float_number = float(byte_string)
                new_array.append(float_number)
            except ValueError:
                new_array.append(0)
        return new_array

    @staticmethod
    def parse_type_to_float(data):
        try:
            return np.frombuffer(data, dtype=np.float64)
        except ValueError as e:
            print("ValueError:", e)
            return []

    @staticmethod
    def calculate_velocity_from_time_and_distance(data_sets):
        complete_set = []
        for data_set in data_sets:
            velocity = data_set['velocity']
            filename = data_set['file_name']
            timestamps = data_set['timestamp']
            distances = data_set['distance']

            if len(timestamps) == 1000 and len(distances) == 1000:
                if len(velocity) == 1000:
                    pass
                else:
                    try:
                        new_velocity = CheckData.calculate_velocity(timestamps, distances, velocity)
                        if len(new_velocity) == 1000:
                            data_set['calculated_velocity'] = new_velocity

                    except Exception as e:
                        print(e)
            else:
                print("Zu wenig Daten zur Berechnung der Velocity. Grund falscher Timestamp.")
                print(filename)
                data_set['calculated_velocity'] = []

            complete_set.append(data_set)

        return complete_set

    @staticmethod
    def calculate_velocity(timestamp, distance, velocity):
        complete_velocity = []

        for index, time in enumerate(timestamp):
            if index < len(velocity):
                complete_velocity.append(velocity[index])

            else:
                time_difference = timestamp - timestamp[index - 1]
                distance_difference = (distance - distance[index - 1])
                velocity = distance_difference / time_difference * 1000
                complete_velocity.append(velocity)

        return complete_velocity
