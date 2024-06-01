import zipfile
import math

import logging

logger = logging.getLogger(__name__)


def get_archive_contents_size(file: bytes, max_size: int):
    size = 0
    with zipfile.ZipFile(file) as archive:
        logger.info(f"{len(archive.infolist())=}")
        for fileinfo in archive.infolist():
            size += fileinfo.file_size
            if size > max_size:
                return -1

    return size


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"
