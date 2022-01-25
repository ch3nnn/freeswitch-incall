# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/11/23 10:20


import redis

from settings import config


class CacheInitialization:
    """缓存初始化"""

    def __init__(self):
        self.cache = redis.Redis(
            connection_pool=redis.ConnectionPool(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                password=config.REDIS_PWD if config.REDIS_PWD else None,
                db=config.REDIS_DB,
                decode_responses=True)
        )

    @staticmethod
    def getClient():
        """获取缓存池客户端"""
        cache = CacheInitialization()
        return cache.cache
