# _*_ coding:utf-8 _*_

import time
import redis
from logbook import Logger
import msgpack

log = Logger("LIB.REDISCLIENT")

class RedisClient(object):
    """
    包装 redis 库
    """
    def __init__(self):
        pass

    def init_app(self, app):
        """
        :param conf: dict, 包含 Redis 的 host, port, db
        """
        try:
            pool = redis.ConnectionPool(
                host=app.config.get('REDIS_HOST', 'localhost'),
                port=app.config.get('REDIS_PORT', 6379),
                db=app.config.get('REDIS_DB', 0))
            log.debug(pool)
            self.__db = redis.StrictRedis(connection_pool=pool, socket_timeout=1)
            self.testConnect()
            return self.__db
        except (ConnectionError, Exception) as e:
            log.error('\n' + str(e) + '\n')
            # 测试redis连通性
        
        
        

    def testConnect(self):
        """
        初始化连接 Redis 数据库, 确保 redis 连接成功
        :return: True
        """
        while True:
            try:
                self.__db.ping()
                return True
            except (ConnectionError, Exception) as e:
                log.error('\n' + str(e) + '\n')
                time.sleep(2)
                continue
        
    def set(self, key, value, ex=None, px=None, nx=False, xx=False):
        return self.__db.set(key, value, ex=ex, px=px, nx=nx, xx=xx)

    def get(self, key):
        return self.__db.get(key)

    def dequeue(self, key):
        """
        删除并返回队列的最后一个一个元素，如果队列为空则阻塞
        """
        return self.__db.rpop(key)

    def getLen(self, key):
        """
        返回队列的长度
        """
        return self.__db.llen(key)

    def enqueue(self, key, data):
        """
        压入数据，放在队列首的位置
        """
        return self.__db.lpush(key, data)

    def flushDb(self):
        """
        删除当前数据库的所有key
        """
        return self.__db.flushdb()

    def keys(self, pattern='*'):
        """
        返回一个列表，给与key所对应的所有值，pattern不传参数则返回所有
        """
        return self.__db.keys(pattern)
