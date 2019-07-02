import os
import redis
from rq import Worker, Queue, Connection


REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_DB = os.environ.get('REDIS_DB', 1)

listen = ['high', 'default', 'low']

redis_url = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
