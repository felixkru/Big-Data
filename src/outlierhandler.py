import numpy as np


class OutlierHandler:

    @staticmethod
    def tukeys_detection(data_array):

        try:

            q1 = np.percentile(data_array, 25)
            q3 = np.percentile(data_array, 75)
            iqr = q3 - q1
            mean = np.median(data_array)

            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            data_neu = [mean
                        if
                        lower_bound > data_point or data_point > upper_bound
                        else
                        data_point
                        for
                        data_point in data_array]
            return data_neu

        except Exception as e:
            print("Error:", str(e))
