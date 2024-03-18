from datetime import datetime
import numpy as np
import pymongo

import mongoConnection
import math


class CheckData:

    def __init__(self):
        pass

    @staticmethod
    def convert_datetime_to_float(timestamps, filename):
        new_timestamps = []

        try:
            for timestamp in timestamps:
                utf_stamp = timestamp.decode("utf-8")
                new_stamp = datetime.strptime(utf_stamp, "%Y-%m-%dT%H:%M:%S")
                new_timestamps.append(new_stamp.timestamp())

            return new_timestamps

        except Exception as error:
            new_stamps = CheckData.convert_to_unix_datetime(timestamps, filename)
            if len(new_stamps) > 0:
                return new_stamps
            else:
                print("Can't convert to Date:", filename)
                print("Error:", error)
                return timestamps

    @staticmethod
    def convert_to_unix_datetime(timestamps, filename):
        new_timestamps = []

        try:
            for timestamp in timestamps:
                new_stamp = float(timestamp)
                new_timestamps.append(new_stamp)
            return new_timestamps
        except ValueError as error:
            print("Can't create Timestamp", filename)
            return []

    @staticmethod
    def handle_ascii_string(array):
        new_array = []
        try:
            for data_set in array:
                float_number = float(data_set)
                new_array.append(float_number)
            return new_array
        except ValueError as e:
            return []

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
            return []

    @staticmethod
    def handle_easter_egg(array, filename):
        new_array = []
        for index, data_set in enumerate(array):
            try:
                byte_string = data_set.decode('utf-8')
                float_number = float(byte_string)
                new_array.append(float_number)
            except ValueError:
                if index > 0:
                    byte_string_prev = array[index - 1].decode('utf-8')
                    float_number_prev = float(byte_string_prev)
                    new_array.append(float_number_prev)
                elif index < len(array) - 1:
                    byte_string_next = array[index + 1].decode('utf-8')
                    float_number_next = float(byte_string_next)
                    new_array.append(float_number_next)
                else:
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
            data_set['calculated_velocity'] = []
            if len(timestamps) == 1000 and len(distances) == 1000:

                if len(velocity) == 1000:
                    pass
                else:
                    try:
                        new_velocity = CheckData.calculate_velocity(timestamps, distances, velocity)
                        if len(new_velocity) == 1000:
                            data_set['calculated_velocity'] = new_velocity

                    except Exception as e:
                        pass
            else:
                print("Zu wenig Daten zur Berechnung der Velocity. Grund falscher Timestamp.")
                print(filename)

            complete_set.append(data_set)

        return complete_set

    @staticmethod
    def calculate_velocity(timestamp, distance, velocity):
        complete_velocity = []
        try:
            for index, time in enumerate(timestamp):
                if index < len(velocity):
                    complete_velocity.append(velocity[index])

                else:
                    time_difference = timestamp[index] - timestamp[index - 1]
                    distance_difference = (distance[index] - distance[index - 1])
                    velocity_new = distance_difference / time_difference * 1000
                    complete_velocity.append(velocity_new)

            return complete_velocity
        except ValueError as e:
            print("Velocity konnte nicht berechnet werden!", e)
            return velocity

    @staticmethod
    def update_magnetization_in_database():
        collection = "european_dolphins"
        query = {}
        updates = []
        updates_bulk = []
        result = mongoConnection.read_data_from_mongo(query, collection)
        for item in result:
            counter = -1
            magnetization_values = item["magnetization"]
            for value_index in magnetization_values:
                counter += 1
                if math.isnan(value_index):
                    mean = (magnetization_values[counter-1] + magnetization_values[counter+1]) / 2
                    magnetization_values[counter] = mean
                    db_filter = {"file_name": item["file_name"]}
                    update = {"$set": {"magnetization": magnetization_values}}
                    updates.append((db_filter, update))
        for db_filter, update in updates:
            operation = pymongo.UpdateOne(db_filter, update)
            updates_bulk.append(operation)
        #mongoConnection.bulk_update_mongo(updates_bulk, collection)

if __name__ == "__main__":
    CheckData.update_magnetization_in_database()