# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/11/10 10:18


import os
import signal
import socket
import socketserver

from loguru import logger

from common.ImportInitialization import ImportInitialization
from common.LogInitialization import LogInitialization


class InCallApplication:
    """服务启动类"""

    # 初始化项目路径
    ImportInitialization()
    # 初始化日志处理器
    LogInitialization()

    @staticmethod
    def start():
        try:
            from settings import config
            from InCallHandler import InCallHandler
            with socketserver.ThreadingTCPServer((config.IN_CALL_HOST, config.IN_CALL_PORT), InCallHandler) as server:
                server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                logger.info(f"Application HTTP On: {config.IN_CALL_HOST} Port: {config.IN_CALL_PORT}...")
                server.serve_forever()
        except Exception as e:
            logger.exception(f"Application status: {e}")
            os.kill(os.getpid(), signal.SIGKILL)


if __name__ == '__main__':
    inCallApplication = InCallApplication()
    inCallApplication.start()
