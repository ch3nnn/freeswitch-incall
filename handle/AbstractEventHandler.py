# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/11/10 14:42

from abc import ABCMeta, abstractmethod

from ESL import ESLevent
from redis import Redis

from server.HandlerServer import HandlerServer


class AbstractEventHandler(metaclass=ABCMeta):
    """抽象事件处理程序"""

    # 事件名称
    EVENT_NAME: str = None

    @abstractmethod
    def handle(self, eslEvent: ESLevent = None, cache: Redis = None, handlerServer: HandlerServer = None):
        """事件处理

        :param handlerServer:
        :param eslEvent: 对应事件连接对象 (PLAYBACK_START CHANNEL_ANSWER) 接收对象
        :param cache: redis客户端对象
        """
        raise Exception('子类中必须实现该方法')
