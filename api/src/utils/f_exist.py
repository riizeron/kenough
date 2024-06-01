import os


# Path finding methods
class FExist:
    @staticmethod
    def folder_exist(path: str):
        return os.path.exists(path)  # False if it's not exist

    @staticmethod
    def file_exist(path: str):
        return os.path.isfile(path)