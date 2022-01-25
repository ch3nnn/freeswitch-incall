class Base(object):
    # freeswitch
    ESL_IP = "127.0.0.1"
    ESL_PORT = "8021"
    ESL_PASSWORD = "ClueCon"

    # redis
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 1
    REDIS_PWD = ""
    REDIS_URL = f"redis://:{REDIS_PWD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

    # inCall 服务ip端口
    IN_CALL_PORT = 8050
    IN_CALL_HOST = "127.0.0.1"
