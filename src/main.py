import math
import seaborn as sns
import numpy as np
import matplotlib.cm as cm
import file_reader_h5
import check_data
import mongoConnection
from calculate_location_parameters import CalculateLocationParameters
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter


def handle_file_reader_and_write_to_database():
    path = "../dataset"
    collection = "complete_dataset"
    analyzer = file_reader_h5.HDF5Analyzer(path)
    dataset = analyzer.handle_file_reader()

    dataset_with_velocity = check_data.CheckData.calculate_velocity_from_time_and_distance(dataset)
    dataset_with_statistic_parameters = CalculateLocationParameters.handle_update_average_and_median_calculation(dataset_with_velocity)
    full_dataset = analyzer.handle_set_full_distance(dataset_with_statistic_parameters)

    mongoConnection.send_data_to_mongo(full_dataset, collection)


def median_average_visualization():
    visualization_data = []
    query_result = mongoConnection.read_data_from_mongo({
            "region": {"$in": ["Europe"]},
            "instrument": {"$in": ["Dog"]}
        }, "european_dog")
    for dataset in query_result:
        visualization_data.append(dataset["full_distance"])

    plt.hist(visualization_data, bins=40)
    plt.xlabel("Distance")
    plt.ylabel("Häufigkeit")
    plt.text(0, 6, "Median: " + str(np.median(visualization_data)))
    plt.text(0, 5.5, "Average: " + str(np.average(visualization_data)))
    plt.show()


def heatmap_visualizer():
    visualization_data_y = []
    visualization_data_x = []

    query_result = mongoConnection.read_data_from_mongo({"file_name": "bb888d23-15a5-458d-8fd5-5118ec48817c"}, "european_dolphins")
    try:
        for dataset in query_result:
            for datapoint in dataset["wall_thickness_clean"]:
                visualization_data_y.append(datapoint)
            for timestamp in dataset["timestamp"]:
                visualization_data_x.append(timestamp)
    except Exception as e:
        print(f"Exception: {e}")

    heatmap, xedges, yedges = np.histogram2d(visualization_data_x, visualization_data_y, bins=50)
    print(float(xedges[0]))
    print(max(visualization_data_x))
    print(yedges)
    print(max(visualization_data_y))

    extent = [float(xedges[0]), float(xedges[-1]), float(yedges[0]), float(yedges[-1])]

    plt.clf()
    plt.imshow(heatmap.T, extent=extent, origin='lower', interpolation='nearest', cmap='hot')
    plt.show()


def heatmap_no2():
    def myplot(x, y, s, bins=1000):
        heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
        heatmap = gaussian_filter(heatmap, sigma=s)

        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        return heatmap.T, extent

    fig, axs = plt.subplots(2, 2)

    visualization_data_y = []
    visualization_data_x = []

    query_result = mongoConnection.read_data_from_mongo({"file_name": "bb888d23-15a5-458d-8fd5-5118ec48817c"}, "european_dolphins")
    try:
        for dataset in query_result:
            smallest_timestamp = dataset["timestamp"][0]
            for datapoint in dataset["wall_thickness_clean"]:
                visualization_data_y.append(datapoint)
            for timestamp in dataset["timestamp"]:
                if math.isnan(timestamp):
                    print("error")
                visualization_data_x.append(int(timestamp - smallest_timestamp))
    except Exception as e:
        print(f"Exception: {e}")

    sigmas = [0, 16, 32, 64]

    for ax, s in zip(axs.flatten(), sigmas):
        if s == 0:
            ax.plot(visualization_data_x, visualization_data_y, 'k.', markersize=5)
            ax.set_title("Scatter plot")
        else:
            img, extent = myplot(visualization_data_x, visualization_data_y, s)
            ax.imshow(img, extent=extent, origin='lower', cmap=cm.jet)
            ax.set_title("Smoothing with  $\sigma$ = %d" % s)

    plt.show()


def heatmap_seaborn():
    visualization_data_y = []
    visualization_data_x = []

    query_result = mongoConnection.read_data_from_mongo({},
                                                        "european_dolphins")
    try:
        for dataset in query_result:
            try:
                for datapoint in dataset["magnetization"]:
                    visualization_data_y.append(datapoint)
            except Exception as e:
                print(f"Exception occurred: {e}")
                continue
            for datapoint in dataset["wall_thickness_clean"]:
                try:
                    visualization_data_x.append(datapoint)
                except Exception as e:
                    print(f"Exception occurred: {e}")
                    continue
    except Exception as e:
        print(f"Exception: {e}")

    print(len(visualization_data_x))
    print(len(visualization_data_y))

    plot = sns.jointplot(x=visualization_data_x, y=visualization_data_y, kind='hex', gridsize=30, cmap="plasma", marginal_kws=dict(bins=50))
    plot.set_axis_labels("Wandstärke", "Magnetisierung")
    plt.tight_layout()
    plt.show()


def seaborn_histogram():
    visualization_data = []
    query_result = mongoConnection.read_data_from_mongo({},
                                                        "european_dog")

    for dataset in query_result:
        visualization_data.append(dataset["year"])

    sns.set_theme(style="whitegrid")

    ax = sns.histplot(data=visualization_data,
                      color="skyblue",  # Farbe der Balken
                      binwidth=1,  # Breite der Balken, angepasst nach Bedarf
                      kde=True,  # Fügt eine Kernel-Density-Estimation-Linie hinzu
                      )

    ax.set(title='Jahr der Messsung: Europe / Dog',
           xlabel='Jahr',
           ylabel='Häufigkeit')

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    # median_average_visualization()
    # heatmap_no2()
    heatmap_seaborn()
    # seaborn_histogram()

    """
    Die Funktion verarbeitet das komplette Datenset
    """
    #handle_file_reader_and_write_to_database()
    """
    query_counter_result = mongoConnection.read_data_from_mongo({
            "region": {"$in": ["Europe"]},
            "instrument": {"$in": ["Dolphin"]}
        }, "complete_dataset")

    mongoConnection.send_data_to_mongo(query_counter_result, "european_dolphins")
    """
    """
    #mongoConnection.send_data_to_mongo(dataset)


    #query_counter_result = mongoConnection.count_data_from_mongo({"region": "Africa"})
    #print(f"Soviele Datensätze entsprechen deinem Query: {query_counter_result}")

    #query_content = mongoConnection.read_data_from_mongo({"file_id": 312})
    #print(query_content)

    So kann man z.B. die namen der datensätze ermitteln bei denen dein query zu trifft."""
"""

So kann man z.B. die namen der datensätze ermitteln bei denen dein query zu trifft.

query_content = mongoConnection.count_data_from_mongo({
    "region": {"$in": ["Europe"]},
    "instrument": {"$in": ["Elephant"]}
}, "raw_measurements_v2")
print(query_content)


for data in query_content:
    print(data['file_name'])
    """
