# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/11/24 10:07
import traceback
from typing import Iterator

from ESL import ESLconnection, ESLevent
from loguru import logger


class EslEventUtils:

    @staticmethod
    def isConnected(eslConnection: ESLconnection):
        """esl是否连接"""
        if eslConnection.connected():
            return True
        return False

    @staticmethod
    def playBack(eslConnection: ESLconnection, filePathList: Iterator):
        """播放音频文件

        :param eslConnection:
        :param filePathList: 音频文件
        """
        if EslEventUtils.isConnected(eslConnection):
            uuid = eslConnection.getInfo().getHeader("unique-id")
            for filePath in filePathList:
                eslConnection.execute("playback", filePath, uuid)

    @staticmethod
    def getPlaybackFilePath(eslEvent: ESLevent) -> str or None:
        """获取播放文件路径"""
        if playbackFilePath := eslEvent.getHeader("Playback-File-Path"):
            return playbackFilePath
        return None

    @staticmethod
    def getEventName(eslEvent: ESLevent) -> str or None:
        """获取事件名称

        自定义事件需要补充Event-Subclass
        """
        eventName = str()
        if name := eslEvent.getHeader('Event-Name'):
            eventName = name
        if name := eslEvent.getHeader('Event-Subclass'):
            eventName += " " + name  # CUSTOM SMS::SEND_MESSAGE
        return eventName

    @staticmethod
    def getRecordFilePath(eslConnectionOrEslEvent: ESLconnection or ESLevent) -> str or None:
        """获取记录文件路径"""
        try:
            if isinstance(eslConnectionOrEslEvent, ESLconnection):
                if EslEventUtils.isConnected(eslConnectionOrEslEvent):
                    return eslConnectionOrEslEvent.getInfo().getHeader('variable_record_file_path')
            elif isinstance(eslConnectionOrEslEvent, ESLevent):
                return eslConnectionOrEslEvent.getHeader("variable_record_file_path")
        except Exception as e:
            logger.error(f"Exception error: {e} -> traceback: {traceback.print_exc()}")

    @staticmethod
    def isNormalClearing(eslConnectionOrEslEvent):
        """查看挂断事件是否正常清算"""
        if isinstance(eslConnectionOrEslEvent, ESLconnection):
            eslConnectionOrEslEvent: ESLconnection
            hangupCause = eslConnectionOrEslEvent.getInfo().getHeader("Hangup-Cause")
        elif isinstance(eslConnectionOrEslEvent, ESLevent):
            hangupCause = eslConnectionOrEslEvent.getHeader("Hangup-Cause")
        else:
            raise Exception("Type error")
        if hangupCause == "NORMAL_CLEARING":
            return True
        return False

    @staticmethod
    def hangup(eslConnection: ESLconnection):
        """挂机操作"""
        eslConnection.execute("hangup")

    @staticmethod
    def CUSTOM():
        """自定义发送事件"""

        con = ESLconnection("127.0.0.1", "8021", "ClueCon")
        event = ESLevent("CUSTOM", "SMS::SEND_MESSAGE")

        event.addHeader("unique-id", "唯一id")
        event.addHeader("自定义 key", "value")
        event.addHeader("自定义 key", "value")
        event.addHeader("自定义 key", "value")
        con.sendEvent(event)
