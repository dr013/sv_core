# Copyright (C) 2018 Eugene Kryukov<ekryukov@icloud.com>
import logging

import shutil

logger = logging.getLogger(__name__)


def move_file(io_param):
    src = io_param["SOURCE_PATH"]
    dst = io_param["DEST_PATH"]
    logger.debug("Move file rule start")
    shutil.move(src, dst)


def send_notification(io_param):
    pass
