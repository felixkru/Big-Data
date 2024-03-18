from visualisation_data import VisualisationData
import mongoConnection


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


if __name__ == "__main__":
    VisualizationHandler.handle_visualisation_of_distance_and_velocity()

