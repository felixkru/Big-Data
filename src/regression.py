import matplotlib
import matplotlib.pyplot
import mongoConnection
import numpy as np
from sklearn.linear_model import LinearRegression


def main():
    counter = 0
    query_content = mongoConnection.read_data_from_mongo({
        "region": {"$in": ["Europe"]},
        "instrument": {"$in": ["Dolphin"]}
    }, "european_dolphins")
    for element in query_content:
        try:
            x = np.array(element["timestamp"])
            y = np.array(element["magnetization"])

            matplotlib.pyplot.scatter(x, y)
            matplotlib.pyplot.savefig(f"../plots/time_over_mag_{counter}.png")
            # matplotlib.pyplot.show()
            matplotlib.pyplot.close()

            model = LinearRegression()
            model.fit(x.reshape(-1, 1), y)

            residuale = y - model.predict(x.reshape(-1, 1)) + np.mean(y[:100])

            matplotlib.pyplot.scatter(x, residuale)
            matplotlib.pyplot.savefig(f"../plots/time_over_mag_regression_{counter}.png")
            # matplotlib.pyplot.show()
            matplotlib.pyplot.close()
            # mongoConnection.send_data_to_mongo(query_content, "european_dolphins")
            counter += 1
        except Exception as e:
            print(f"Error: {e} ")
            counter += 1
            x = []
            y = []
            continue


main()
