import redis
REDIS_HOST = "localhost"
REDIS_PORT = 6379
CACHE_TIMEOUT = 300
cache = redis.StrictRedis(host = REDIS_HOST,port = REDIS_PORT)
def get_cache(key):
    return cache.get(key)

def set_cache(key,value,timeout = CACHE_TIMEOUT):
    cache.set(key,value,ex = timeout)
# set_cache("123:anup","helllo")
# print(get_cache("123:anup"))