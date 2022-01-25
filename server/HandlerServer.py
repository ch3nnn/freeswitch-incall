# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/11/10 14:12
import threading
from importlib import import_module

from ESL import ESLconnection, ESLevent
from loguru import logger
from redis import Redis

from utils.EslEventUtils import EslEventUtils


class HandlerServer:
    cache: Redis
    eslConnection: ESLconnection

    # 事件处理程序导入模块名称
    EVENT_HANDLER_IMPORT_MODULE = "incall.handle.AbstractEventHandler"
    # 事件处理程序类名
    EVENT_HANDLER_CLASS_NAME = "AbstractEventHandler"

    def __init__(self, eslConnection: ESLconnection, cache: Redis):
        """初始化创建处理程序服务"""

        # 当前通话全局esl连接对象
        self.eslConnection = eslConnection
        # redis连接对象
        self.cache = cache
        # 当前通话是否挂掉
        self.isChannelHangup = False

    def handleConnectResponse(self):
        """freeswitch 接收wav录音数据event事件做出对应处理"""
        try:
            # TODO 桥接用户号码
            # innerUser = self.eslConnection.getInfo().getHeader("variable_inner_user")
            self.eslConnection.executeAsync("bridge", f"user/1010")
            # 循环监听事件直到通话结束
            while not self.isChannelHangup:
                # 20 改为 10 缩短接收事件定时 防止发完 hangup 命令 接收不到挂断事件
                if eslEvent := self.eslConnection.recvEventTimed(10):
                    logger.debug(EslEventUtils.getEventName(eslEvent))
                    self.onEventHandler(eslEvent)
        except Exception as e:
            logger.exception(f"Exception error: {e}")
        finally:
            logger.debug("recognizer stop ")

    def onEventHandler(self, eslEvent: ESLevent):
        """获取事件名称多线程处理对应事件

        :param eslEvent: esl事件对象
        :return: 执行对应handle文件夹下事件
        """
        module = import_module(self.EVENT_HANDLER_IMPORT_MODULE)
        clazz = getattr(module, self.EVENT_HANDLER_CLASS_NAME)
        eventName = EslEventUtils.getEventName(eslEvent)
        for subclass in clazz.__subclasses__():
            if eventName == subclass.EVENT_NAME:
                logger.info(f"current running event name is {eventName} ...")
                thread = threading.Thread(target=subclass.handle, args=(subclass, eslEvent, self.cache, self))
                thread.setDaemon(True)
                thread.start()
