# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/11/24 16:13

import importlib
import re
from pathlib import Path

from loguru import logger


class ImportInitialization:
    """导入初始化"""

    def __init__(self):
        # import 导入所有事件处理器
        for file in Path(__file__).parent.parent.joinpath("handle").rglob('*.py'):
            if fileName := ''.join(re.findall("([a-zA-Z0-9]+)\\.py", file.name)):
                logger.success(f"success load event handle {fileName}")
                importlib.import_module('incall.handle.' + fileName)
