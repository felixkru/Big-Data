from visualisation_data import VisualisationData
import mongoConnection
from use_db_scan import UseDBSCAN
import matplotlib.pyplot as plt


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
    def handle_scatter_chart_with_multiple_arguments(data_sets):
        visual_data = VisualisationData()

        magnetization = {"magnetization": data_sets['magnetization']}
        velocity = {"velocity": data_sets['velocity']}
        wall_thickness = {"wall_thickness": data_sets['wall_thickness']}
        defect_channel = {"defect_channel": data_sets['defect_channel']}

        relevant_sets = [magnetization, velocity, defect_channel, wall_thickness]

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

        mongoConnection.close_mongo_client()
        visual_data.create_pie_chart(results_per_region, regions, title)

    @staticmethod
    def handle_visualisation_of_distance_and_velocity():
        """
        Ziel der Funktion ist es mehrer durchschnittswerte zu Clustern. Diese können als Gruppe geclustert werden, aber auch
        mehrer Abfragen können in einem Chart visualisiert werden.
        """
        visual_data = VisualisationData()
        collection = "complete_dataset"
        query = {"region": "Europe", "instrument": "Dolphin"}
        query2 = {"region": "Europe", "instrument": "Dog"}

        results = mongoConnection.read_data_from_mongo(query, collection)
        results2 = mongoConnection.read_data_from_mongo(query2, collection)
        mongoConnection.close_mongo_client()

        x_data = []
        y_data = []
        x_data2 = []
        y_data2 = []

        for item in results:
            x_data.append(item['velocity_median'])
            y_data.append(item['full_distance'])

        for item in results2:
            x_data2.append(item['velocity_median'])
            y_data2.append(item['full_distance'])

        complete_x_data = []
        complete_x_data.append(x_data)
        complete_x_data.append(x_data2)

        complete_y_data = []
        complete_y_data.append(y_data)
        complete_y_data.append(y_data2)

        visual_data.create_scatterplot_with_different_data_src_without_index(complete_x_data, complete_y_data, 'velocity_median', 'full_distance', 'Velocity vs Full Distance')

    @staticmethod
    def visual_data_with_clustering_db_scan():
        collection = "european_dolphins"
        query = {"region": "Europe", "instrument": "Dolphin"}
        results = mongoConnection.read_data_from_mongo(query, collection)

        current_cluster_set = results[0]['wall_thickness_clean']

        plt.figure(figsize=(8, 4))
        plt.scatter(range(len(current_cluster_set)), current_cluster_set, c=current_cluster_set, cmap='viridis',
                    s=50, edgecolors='k')
        plt.xlabel("Datenpunkt")
        plt.ylabel("Wall Thickness")
        plt.title("Original Data - Wall Thickness")
        plt.colorbar()
        plt.show()

        clusters = UseDBSCAN.use_db_scan(0.2, 2, current_cluster_set)

        plt.figure(figsize=(8, 4))
        plt.scatter(range(len(clusters)), clusters, c=clusters, cmap='viridis', s=50, edgecolors='k')
        plt.xlabel("Datenpunkt")
        plt.ylabel("Cluster")
        plt.title("Clustering wall_thickness without outliers")
        plt.colorbar()
        plt.show()


if __name__ == "__main__":
    #VisualizationHandler.handle_visualisation_of_distance_and_velocity()
    VisualizationHandler.visual_data_with_clustering_db_scan()

