import numpy as np


class outlier_handler:

    def __init__(self, file):
        self.file = file
        self.file_2 = file

    ##z-score
    def zscore_detection(self):

        try:

            mean_X = np.mean(self.file)
            std_X = np.std(self.file)
            z_scores = (self.file - mean_X) / std_X
            ##outliers = np.where(np.abs(z_scores) > 3)
            inliers = np.where(np.abs(z_scores) <= 3)
            filtered_data = self.file[inliers]
        
            return filtered_data
        
        except ZeroDivisionError:
            print("Zero division is forbidden.")

        except Exception as e:
            print("Error:", str(e))


    ##Tukeys Method
    def tukeys_detection(self):

        try:
       
            Q1 = np.percentile(self.file_2, 25)
            Q3 = np.percentile(self.file_2, 75)
            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            inliers = np.where((self.file_2 >= lower_bound) & (self.file_2 <= upper_bound))
            filtered_data = self.file_2[inliers]

            return filtered_data
        
        except ZeroDivisionError:
            print("Zero division is forbidden.")

        except Exception as e:
            print("Error:", str(e))
