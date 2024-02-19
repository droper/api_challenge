"""
Wrapper classes for different cache server options
"""

import abc
import redis

class CacheClientInterface(abc.ABC):
    @abc.abstractmethod
    def get(self, key):
        pass

    @abc.abstractmethod
    def incr(self, key):
        pass

    @abc.abstractmethod
    def expire(self, key, seconds):
        pass

class RedisClient(CacheClientInterface):
    """
    Wrapper class for the Redis client.

    This class implements the RedisClientInterface using the redis.StrictRedis client.
    """
    def __init__(self, host='localhost', port=6379, db=0):
        """
        Initialize the Redis client wrapper.

        Args:
            host (str): The hostname or IP address of the Redis server.
            port (int): The port number of the Redis server.
            db (int): The Redis database index.
        """
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db)

    def get(self, key):
        """
        Get the value associated with the specified key from Redis.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            The value associated with the key, or None if the key does not exist.
        """
        return self.redis_client.get(key)

    def incr(self, key):
        """
        Increment the value associated with the specified key in Redis.

        Args:
            key (str): The key to increment the value for.

        Returns:
            int: The incremented value.
        """
        return self.redis_client.incr(key)

    def expire(self, key, seconds):
        """
        Set an expiration time for the specified key in Redis.

        Args:
            key (str): The key to set the expiration time for.
            seconds (int): The number of seconds until the key expires.
        """
        return self.redis_client.expire(key, seconds)