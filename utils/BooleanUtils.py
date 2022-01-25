# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/12/15 15:35


class BooleanUtils:

    @staticmethod
    def parseBoolean(s: str):
        """将字符串参数解析为布尔值"""
        if s is not None:
            if s.lower() == "true":
                return True
        return False

