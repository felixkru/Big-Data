import matplotlib
import matplotlib.pyplot
import mongoConnection
import numpy as np
from sklearn.linear_model import LinearRegression


def main():
    query_content = mongoConnection.read_data_from_mongo({
        "region": {"$in": ["Europe"]},
        "instrument": {"$in": ["Dolphin"]},
        "file_name": "1ad1bda2-c595-45f7-9eb9-0c440d489b76"
    }, "european_dolphins")

    x = np.array(query_content[0]["timestamp"])
    y = np.array(query_content[0]["magnetization"])

    matplotlib.pyplot.scatter(x, y)
    matplotlib.pyplot.show()

    model = LinearRegression()
    model.fit(x.reshape(-1, 1), y)

    residuale = y - model.predict(x.reshape(-1, 1))

    matplotlib.pyplot.scatter(x, residuale)
    matplotlib.pyplot.show()
    # mongoConnection.send_data_to_mongo(query_content, "european_dolphins")


main()
