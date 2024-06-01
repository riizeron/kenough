import yaml
import logging

from src.utils.f_exist import FExist
from src.exceptions.file import FileException

logger = logging.getLogger(__name__)


def yml_to_dict(path_to_yml: str) -> dict:
    r"""
    Преобразование yaml файла в словарь python

    :param path_to_yml: Путь к yaml файлу
    :return: Словарь python
    :rtype: dict
    """
    if not FExist.file_exist(path_to_yml):
        logger.error(f"{path_to_yml} not found")
        raise FileException("File not found")

    with open(path_to_yml, 'r') as file:
        data = yaml.safe_load(file)

    return data
