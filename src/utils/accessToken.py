from django.conf import settings
import redis

def get_access_token():
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.DB, password=
    settings.REDIS_PWD)
    access_token = r.get('access_token')
    access_token = access_token.decode('utf-8')
    return access_token