from visualisation_data import VisualisationData
import mongoConnection
from use_db_scan import UseDBSCAN
import matplotlib.pyplot as plt
import numpy as np


class VisualizationHandler:

    def __init__(self):
        pass

    @staticmethod
    def handle_scatter_chart_with_one_argument(data_sets):
        visual_data = VisualisationData()

        magnetization = {"magnetization": data_sets['magnetization']}
        velocity = {"velocity": data_sets['velocity']}
        wall_thickness = {"wall_thickness": data_sets['wall_thickness']}
        defect_channel = {"defect_channel": data_sets['defect_channel']}

        visual_data.create_scatter_plot(magnetization, data_sets['file_name'])

    @staticmethod
    def handle_scatter_chart_with_multiple_arguments():
        visual_data = VisualisationData()
        query = {}
        collection = "european_dolphins"

        results = mongoConnection.read_data_from_mongo(query, collection)

        data_sets = results[0]

        magnetization = {"magnetization": data_sets['magnetization_straightened_clean']}
        velocity = {"velocity": data_sets['velocity_clean']}
        wall_thickness = {"wall_thickness": data_sets['wall_thickness_clean']}
        defect_channel = {"defect_channel": data_sets['defect_channel']}

        relevant_sets = [magnetization, velocity]

        visual_data.create_scatterplot_with_different_data_src(relevant_sets, data_sets['file_name'])

    @staticmethod
    def handle_pie_chart_regions():
        regions = ["Africa", "Europe", "Asia", "Australia", "America"]
        title = "Configuration"
        results_per_region = []
        visual_data = VisualisationData()

        for region in regions:
            result = mongoConnection.count_data_from_mongo({"region": region})

            if result:
                results_per_region.append(result)
            else:
                results_per_region.append(0)

       # mongoConnection.close_mongo_client()
        visual_data.create_pie_chart(results_per_region, regions, title)

    @staticmethod
    def handle_visualisation_of_distance_and_velocity():
        """
        Ziel der Funktion ist es mehrer durchschnittswerte zu Clustern. Diese können als Gruppe geclustert werden, aber auch
        mehrer Abfragen können in einem Chart visualisiert werden.
        """
        visual_data = VisualisationData()
        collection = "european_dolphins"
        query = {"region": "Europe", "instrument": "Dolphin"}
        #query2 = {"region": "Europe", "instrument": "Dog"}

        results = mongoConnection.read_data_from_mongo(query, collection)
        #results2 = mongoConnection.read_data_from_mongo(query2, collection)
        mongoConnection.close_mongo_client()

        x_data = []
        y_data = []
        x_data2 = []
        y_data2 = []

        for item in results:
            x_data.append(item['velocity_median'])
            y_data.append(item['full_distance'])

        #for item in results2:
        #    x_data2.append(item['velocity_median'])
        #    y_data2.append(item['full_distance'])

        complete_x_data = []
        complete_x_data.append(x_data)
        #complete_x_data.append(x_data2)

        complete_y_data = []
        complete_y_data.append(y_data)
        #complete_y_data.append(y_data2)

        visual_data.create_scatterplot_with_different_data_src_without_index(complete_x_data, complete_y_data, 'velocity_median', 'full_distance', 'Velocity vs Full Distance')

    @staticmethod
    def visual_data_with_clustering_db_scan():
        collection = "european_dolphins"
        query = {"region": "Europe", "instrument": "Dolphin"}
        results = mongoConnection.read_data_from_mongo(query, collection)

        current_cluster_set = results[4]['wall_thickness_clean']

        plt.figure(figsize=(8, 4))
        plt.scatter(range(len(current_cluster_set)), current_cluster_set, c=current_cluster_set, cmap='viridis',
                    s=50, edgecolors='k')
        plt.xlabel("Datenpunkt")
        plt.ylabel("Wall Thickness")
        plt.title("Original Data - Wall Thickness")
        plt.colorbar()
        plt.show()

        clusters = UseDBSCAN.use_db_scan(0.6, 2, current_cluster_set)

        unique_clusters = np.unique(clusters)
        num_clusters = len(unique_clusters)
        colors = plt.cm.viridis(np.linspace(0, 1, num_clusters))
        plt.figure(figsize=(8, 4))
        for cluster_label, color in zip(unique_clusters, colors):
            cluster_indices = np.where(clusters == cluster_label)[0]
            cluster_points = [current_cluster_set[i] for i in cluster_indices]
            plt.scatter(cluster_indices, cluster_points, color=color, label=f'Cluster {cluster_label}',
                        s=50, edgecolors='k')

            if cluster_label == 1:
                cluster_1_points = cluster_points
        plt.xlabel("Datenpunkt")
        plt.ylabel("Wall Thickness")
        plt.title("Clustering wall_thickness without outliers")
        plt.legend()
        plt.show()

        print(len(cluster_1_points))


    @staticmethod
    def handle_show_linear_regression():
        visual_data = VisualisationData()
        query = {}
        collection = "european_dolphins"

        results = mongoConnection.read_data_from_mongo(query, collection)

        data_sets = results[0]

        magnetization_straighted_clean = {"magnetization_straightened_clean": data_sets['magnetization_straightened_clean']}
        magnetization_clean = {"magnetization_clean": data_sets['magnetization_straightened']}
        magnetization = {"magnetization": data_sets['magnetization']}

        relevant_sets = [magnetization_straighted_clean, magnetization]

        visual_data.create_scatterplot_with_different_data_src(relevant_sets, data_sets['file_name'])


if __name__ == "__main__":
    #VisualizationHandler.handle_visualisation_of_distance_and_velocity()
    VisualizationHandler.visual_data_with_clustering_db_scan()
    #VisualizationHandler.handle_scatter_chart_with_multiple_arguments()
    #VisualizationHandler.handle_show_linear_regression()
