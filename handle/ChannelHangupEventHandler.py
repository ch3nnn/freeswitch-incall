# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/11/10 14:08
from loguru import logger

from handle.AbstractEventHandler import AbstractEventHandler
from model.enum.EventNames import EventNames


class ChannelHangupEventHandler(AbstractEventHandler):
    """电话挂断事件"""

    EVENT_NAME = EventNames.CHANNEL_HANGUP

    def handle(self, eslEvent=None, cache=None, handlerServer=None):
        # TODO 记录正常通话-用户挂机
        handlerServer.isChannelHangup = True
        logger.debug(eslEvent.serialize("json"))
