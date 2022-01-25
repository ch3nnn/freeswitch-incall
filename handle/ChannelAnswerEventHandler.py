# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/11/10 14:08

from loguru import logger

from handle.AbstractEventHandler import AbstractEventHandler
from model.enum.EventNames import EventNames


class ChannelAnswerEventHandler(AbstractEventHandler):
    """应答事件处理"""

    EVENT_NAME = EventNames.CHANNEL_ANSWER

    def handle(self, eslEvent=None, cache=None, handlerServer=None):
        logger.debug(eslEvent.serialize("json"))
