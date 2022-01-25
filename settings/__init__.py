import os

from loguru import logger

import settings.config

active = os.getenv("profile")
if active:
    config = getattr(config, active)()
    logger.info(f"load {active} profile")
else:
    config = config.Base()
    logger.info(f"load Base profile")
