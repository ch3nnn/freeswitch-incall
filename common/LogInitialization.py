# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/11/23 10:20


import sys
import time
from pathlib import Path

from loguru import logger

LOG_LEVEL = "DEBUG"


class LogInitialization:
    """日志初始化"""

    def __init__(self):
        basePath = Path.cwd()
        logPath = Path(basePath, "logs")
        logger.remove()
        # 控制台
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <level>[{level}] [{file.name}] [{function}:{line}]: {message}</level>",
            enqueue=True,
            backtrace=True,
            diagnose=True

        )
        # 记录文件
        logger.add(
            f"{logPath}/{time.strftime('%Y%m%d')}.log",
            level=LOG_LEVEL,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <level>[{level}] [[{file.name}] [{function}:{line}]: {message}</level>",
            rotation="00:00",
            encoding="utf-8",
            enqueue=True,
            backtrace=True,
            diagnose=True
        )
