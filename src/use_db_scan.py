from sklearn.cluster import DBSCAN


class UseDBSCAN:
    def __init__(self):
        pass

    @staticmethod
    def use_db_scan(eps, min_samples, data_set):
        dbscan = DBSCAN(eps, min_samples=min_samples)
        return dbscan.fit_predict([[x] for x in data_set])

