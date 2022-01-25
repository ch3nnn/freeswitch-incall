# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/11/18 10:34


class EventNames:
    """事件名称"""

    # 通道数据
    CHANNEL_DATA = "CHANNEL_DATA"
    # 通道应答
    CHANNEL_ANSWER = 'CHANNEL_ANSWER'
    # 记录开始
    RECORD_START = 'RECORD_START'
    # 记录结束
    RECORD_STOP = 'RECORD_STOP'
    # 播音开始
    PLAYBACK_START = 'PLAYBACK_START'
    # 播音结束
    PLAYBACK_STOP = 'PLAYBACK_STOP'
    # 通道挂断
    CHANNEL_HANGUP = 'CHANNEL_HANGUP'
    # 通道完成挂断
    CHANNEL_HANGUP_COMPLETE = 'CHANNEL_HANGUP_COMPLETE'
    # 通道呼叫状态
    CHANNEL_CALL_STATE = "CHANNEL_CALLSTATE"
    # 自定义事件
    CUSTOM_SMS_SEND_MESSAGE = "CUSTOM SMS::SEND_MESSAGE"
    # 桥接挂断
    CHANNEL_UNBRIDGE = "CHANNEL_UNBRIDGE"
    # 频道执行 (执行)
    CHANNEL_EXECUTE = "CHANNEL_EXECUTE"
    # 所有事件
    ALL = "ALL"
