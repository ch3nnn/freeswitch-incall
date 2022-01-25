# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/12/2 09:45
from enum import Enum, unique
from typing import Optional


@unique
class CallStateResult(Enum):
    """通话状态结果"""

    USER_STATE_NULL = (0, "未知的初始状态")
    USER_STATE_ANSWERED = (200, "接通")
    USER_STATE_POWER_OFF = (301, "关机")
    USER_STATE_NOT_EXIST = (302, "空号")
    USER_STATE_INVALID_NUM = (303, "非法号码")
    USER_STATE_OUT_SERVICE = (304, "停机")
    USER_STATE_NOT_IN_SERVICE = (305, "不在服务区")
    USER_STATE_NOT_ANSWER = (306, "无人接听")
    USER_STATE_BUSY = (307, "用户拒接")
    USER_STATE_NOT_REACHABLE = (308, "无法接通")
    USER_STATE_NOT_LOCAL_NUM_NEED_ZERO = (309, "本地号码未加零")
    USER_STATE_LOCAL_NUM_ADD_ZERO = (310, "本地号码多加零")
    USER_STATE_BARRING_INCOMING = (311, "呼入限制")
    USER_STATE_CALL_REMINDER = (312, "来电提醒")
    USER_STATE_DEFAULTING = (313, "欠费")
    USER_STATE_LINE_BUSY = (314, "网络忙")
    USER_STATE_FORWARDED = (315, "呼叫转移失败")
    USER_STATE_CANNOT_CONNECTED = (316, "无法接听")
    USER_STATE_NUMBER_CHANGE = (317, "改号")
    USER_STATE_LINE_FAULT = (318, "线路故障")
    USER_STATE_NOT_RECOGNITION = (320, "未知状态")
    USER_STATE_CALL_FAILED = (321, "呼叫失败")
    USER_STATE_HANGUP = (500, "通话结束")

    def getCode(self):
        """根据枚举名称取状态码code

        @return: 状态码code
       """
        return self.value[0]

    def getMessage(self):
        """根据枚举名称取状态说明message

        @return: 状态说明message
        """
        return self.value[1]

    @classmethod
    def messageByCode(cls, code) -> Optional[str]:
        """根据状态码获取状态码说明"""
        for name, member in cls.__members__.items():
            if code in member.value:
                return cls[name].getMessage()
        return None
