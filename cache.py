import redis
REDIS_HOST = "localhost"
REDIS_PORT = 6379
CACHE_TIMEOUT = 300
cache = redis.StrictRedis(host = REDIS_HOST,port = REDIS_PORT)
# This method is used to get the saved value from the redis database
def get_cache(key):
    return cache.get(key)

# This method is used to set the new values to new key with a defined timeout method
def set_cache(key,value,timeout = CACHE_TIMEOUT):
    cache.set(key,value,ex = timeout)