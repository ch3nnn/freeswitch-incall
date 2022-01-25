# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/11/10 14:08

from handle.AbstractEventHandler import AbstractEventHandler
from model.enum.EventNames import EventNames
from utils.EslEventUtils import EslEventUtils


class UnBridgeEventHandler(AbstractEventHandler):
    """桥接已终止"""

    EVENT_NAME = EventNames.CHANNEL_UNBRIDGE

    def handle(self, eslEvent=None, cache=None, handlerServer=None):
        # TODO 记录正常通话-坐席挂机
        # 被交接端挂机后, 执行桥阶端挂机操作
        EslEventUtils.hangup(handlerServer.eslConnection)
