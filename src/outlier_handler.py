import numpy as np


class outlier_handler:

    def __init__(self, file):
        self.file = file
        self.file_2 = file

    def zscore_detection(self):

        try:

            mean = np.mean(self.file)
            std = np.std(self.file)
            z_scores = (self.file - mean) / std
            inliers = np.where(np.abs(z_scores) <= 3)
            filtered_data = self.file[inliers]
        
            return filtered_data
        
        except ZeroDivisionError:
            print("Zero division is forbidden.")

        except Exception as e:
            print("Error:", str(e))


    def tukeys_detection(self):

        try:
       
            q1 = np.percentile(self.file_2, 25)
            q3 = np.percentile(self.file_2, 75)
            iqr = q3 - q1

            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            inliers = np.where((self.file_2 >= lower_bound) & (self.file_2 <= upper_bound))
            filtered_data = self.file_2[inliers]

            return filtered_data
        
        except ZeroDivisionError:
            print("Zero division is forbidden.")

        except Exception as e:
            print("Error:", str(e))
