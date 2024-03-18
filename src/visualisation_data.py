import matplotlib.pyplot as plt


class VisualisationData:

    def __init__(self):
        pass

    @staticmethod
    def create_scatter_plot(y_ax_data, file_name):
        y_key = list(y_ax_data.keys())[0]
        y_values = y_ax_data[y_key]
        index_data = list(range(len(list(y_ax_data.values())[0])))

        fig, ax = plt.subplots()
        ax.set_ylabel(y_key)
        ax.set_xlabel("Point-Nr.")
        ax.scatter(index_data, y_values)

        plt.plot(y_values, linestyle='dotted')
        plt.grid()
        plt.title(file_name)
        plt.show()

    @staticmethod
    def create_pie_chart(data_set, data_labels, pie_title):
        plt.pie(data_set, labels=data_labels, autopct='%1.1f%%')
        plt.title(pie_title)
        plt.gca().set_axis_off()
        plt.show()

    @staticmethod
    def create_scatterplot_with_different_data_src(data_sets, file_name):
        index_data = list(range(len(list(data_sets[0].values())[0])))

        fig, ax = plt.subplots()

        for data_set in data_sets:
            if len(data_set) == len(data_sets[0]):
                y_ax_data = list(data_set.values())[0]
                ax.scatter(index_data, y_ax_data, label=list(data_set.keys())[0])
                ax.plot(y_ax_data, linestyle='dotted')

        ax.set_ylabel(list(data_sets[0].keys())[0])
        ax.set_xlabel("Point-Nr.")
        ax.legend()

        plt.legend()
        plt.grid()
        plt.title(file_name)
        plt.show()

    @staticmethod
    def create_scatterplot_with_different_data_src_without_index(data_sets_x, data_sets_y, x_ax_label, y_ax_label,plotName):

        fig, ax = plt.subplots()

        for index, x_data in enumerate(data_sets_x):
            ax.scatter(x_data, data_sets_y[index])

        ax.set_xlabel(x_ax_label)
        ax.set_ylabel(y_ax_label)
        ax.legend()

        plt.grid()
        plt.title(plotName)
        plt.show()


if __name__ == '__main__':
    y_data = {"distance": [8, 12, 3, -3.4, 5, 25, 7, 8, 14, -3, 44]}
    VisualisationData.create_scatter_plot(y_data, file_name="0145-gs45")

    full_data_set = [
        {"distance": [4, 12, 3, -3.4, 5, 25, 7, 8, 14, -3, 44]},
        {"magnetization": [8, 5, 3, -3.4, 5, 25, 7, 8, 4, 0, -4]},
        {"wall_thickness": [5, 5, 3, -3.4, -5, 4, 7, 8, 4, 0, -4]}
    ]
    VisualisationData.create_scatterplot_with_different_data_src(full_data_set, file_name="0145-gs45")

    pie_set = [15, 12, 4, 6, 0, 18]
    pie_label = ["Europa", "Afrika", "Asien", "Südamerika", "Nordamerika", "Australien"]

    VisualisationData.create_pie_chart(pie_set, pie_label, pie_title="Regionen")
