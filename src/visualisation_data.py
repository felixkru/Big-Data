import matplotlib.pyplot as plt

class VisualisationData:

    def __init__(self):
        pass

    @staticmethod
    def create_scatter_plot(x_ax_data, y_ax_data):
        x_key = list(x_ax_data.keys())[0]
        x_values = x_ax_data[x_key]

        y_key = list(y_ax_data.keys())[0]
        y_values = y_ax_data[y_key]

        plt.style.use('_mpl-gallery')
        fig, ax = plt.subplots()

        ax.set_xlabel(x_key)
        ax.set_ylabel(y_key)
        ax.scatter(x_values, y_values)

        plt.show()

if __name__ == '__main__':
    x_data = {"distance": [14, 12, 3, -3.4, 5, 25, 7, 8, 9, 10]}
    y_data = {"timestamp": [8, 12, 3, -3.4, 5, 25, 7, 8, 14, -3]}

    VisualisationData.create_scatter_plot(x_data, y_data)
