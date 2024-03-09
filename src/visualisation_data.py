import matplotlib.pyplot as plt
import numpy as np


class VisualisationData:

    def __init__(self):
        pass

    @staticmethod
    def create_scatter_plot(y_ax_data):
        y_key = list(y_ax_data.keys())[0]
        y_values = y_ax_data[y_key]

        index_data = []
        index = 0

        for value in y_values:
            index_data.append(index)
            index += 1

        fig, ax = plt.subplots()

        ax.set_ylabel(y_key)
        ax.set_xlabel("Point-Nr.")

        ax.scatter(index_data, y_values)

        plt.plot(y_values, linestyle='dotted')
        plt.grid()
        plt.show()


if __name__ == '__main__':
    y_data = {"distance": [8, 12, 3, -3.4, 5, 25, 7, 8, 14, -3, 44]}
    VisualisationData.create_scatter_plot(y_data)
