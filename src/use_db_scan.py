from sklearn.cluster import DBSCAN
import numpy as np


class UseDBSCAN:
    def __init__(self):
        pass

    @staticmethod
    def use_db_scan(eps, min_samples, data_set):
        data = np.array([[x] for x in data_set])
        dbscan = DBSCAN(eps, min_samples=min_samples)
        clusters = dbscan.fit_predict(data)
        return clusters


