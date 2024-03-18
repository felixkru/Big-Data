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

       # mongoConnection.close_mongo_client()
        visual_data.create_pie_chart(results_per_region, regions, title)

