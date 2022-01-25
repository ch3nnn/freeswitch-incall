# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/11/10 10:34


import socketserver
from socketserver import BaseServer
from typing import Any

import ESL
from loguru import logger
from redis import Redis

from common.CacheInitialization import CacheInitialization
from model.enum.EventNames import EventNames
from server.HandlerServer import HandlerServer


class InCallHandler(socketserver.BaseRequestHandler):
    # 初始化创建redis连接池
    cache: Redis = CacheInitialization.getClient()
    logger.info("CacheInitialization success ...")

    def __init__(self, request: Any, client_address: Any, server: BaseServer) -> None:
        """初始化创建esl连接"""
        self.eslConnection = ESL.ESLconnection(request.fileno())
        super().__init__(request, client_address, server)

    def handle(self):
        """处理eslConnection各类事件"""

        logger.info(f'Application: client_address: {self.client_address} connected...')
        if self.eslConnection.connected():
            logger.info(f'Application: Connected: {self.eslConnection.connected()}')
            self.eslConnection.events('plain', EventNames.CHANNEL_ANSWER)
            self.eslConnection.events('plain', EventNames.RECORD_START)
            self.eslConnection.events('plain', EventNames.RECORD_STOP)
            self.eslConnection.events('plain', EventNames.CHANNEL_HANGUP)
            self.eslConnection.events('plain', EventNames.CUSTOM_SMS_SEND_MESSAGE)
            self.eslConnection.events('plain', EventNames.ALL)
            # 过滤事件操作
            self.eslConnection.filter('unique-id', self.eslConnection.getInfo().getHeader('unique-id'))

            logger.info(f"Channel-Caller-ID-Number: {self.eslConnection.getInfo().getHeader('Channel-Caller-ID-Number')}")
            logger.debug(f'Application Connected Info Data: {self.eslConnection.getInfo().serialize(format="json")}')

            # TODO 事件业务代码 处理连接响应
            server = HandlerServer(eslConnection=self.eslConnection, cache=self.cache)
            server.handleConnectResponse()

    def finish(self):
        """结束通过连接"""
        self.request.close()
        self.eslConnection.disconnect()
        logger.info("Application: Received disconnection notice.")
