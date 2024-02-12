import os


class CheckData:

    def __init__(self, folder_path):
        self.folder_path = folder_path

    def count_files(self):
        files = os.listdir(self.folder_path)
        return len(files)

