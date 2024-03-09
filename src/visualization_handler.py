from visualisation_data import VisualisationData


class VisualizationHandler:

    def __init__(self):
        pass

    @staticmethod
    def handle_scatter_chart_with_one_argument(data_sets):

        pass

    @staticmethod
    def handle_scatter_chart_with_multiple_arguments(data_sets):
        visual_data = VisualisationData()

        magnetization = {"magnetization": data_sets['magnetization']}
        velocity = {"velocity": data_sets['velocity']}
        wall_thickness = {"wall_thickness": data_sets['wall_thickness']}
        defect_channel = {"defect_channel": data_sets['defect_channel']}

        relevant_sets = [magnetization, velocity, defect_channel, wall_thickness]

        visual_data.create_scatterplot_with_different_data_src(relevant_sets)


