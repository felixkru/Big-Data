import numpy as np


class CalculateLocationParameters:

    def __init__(self):
        pass

    @staticmethod
    def calculate_median(data_array):
        return np.median(data_array)

    @staticmethod
    def calculate_average(data_array):
        array_sum = sum(data_array)
        array_length = len(data_array)
        return array_sum / array_length

    @staticmethod
    def handle_update_average_and_median_calculation(data_set):

        for data_array in data_set:
            try:
                if len(data_array['calculated_velocity']) > 0:
                    data_array["velocity_median"] = CalculateLocationParameters.calculate_median(data_array['calculated_velocity'])
                    data_array["velocity_average"] = CalculateLocationParameters.calculate_average(data_array['calculated_velocity'])
                else:
                    data_array["velocity_median"] = CalculateLocationParameters.calculate_median(data_array['velocity'])
                    data_array["velocity_average"] = CalculateLocationParameters.calculate_average(data_array['velocity'])

                data_array["wall_thickness_median"] = CalculateLocationParameters.calculate_median(data_array['wall_thickness'])
                data_array["magnetization_median"] = CalculateLocationParameters.calculate_median(data_array['magnetization'])

                data_array["wall_thickness_average"] = CalculateLocationParameters.calculate_average(data_array['wall_thickness'])
                data_array["magnetization_average"] = CalculateLocationParameters.calculate_average(data_array['magnetization'])

            except Exception as e:
                print("Fehler beim Errechnen des Medians oder des Durchschnitts: ", e)
                print(data_array['file_name'])

        return data_set


if __name__ == '__main__':
    parameters = [7, 2, 1, 6, 3, 9, 5, 4, 25]
    # result = 5.0
    print(CalculateLocationParameters.calculate_median(parameters))
    # result 6.89
    print(CalculateLocationParameters.calculate_average(parameters))
