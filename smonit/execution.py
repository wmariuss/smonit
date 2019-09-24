import os
from rq import Queue
from redis import Redis

from smonit.tasks import connected, pending, denied, rejected, respond_minion
from smonit.tasks import check_changes, respond_minion_db
from smonit.views import Index
from smonit.services.api import Salt


class Run(object):
    def __init__(self):
        redis_host = os.environ.get("REDIS_HOST", "localhost")
        redis_port = os.environ.get("REDIS_PORT", 6379)

        self.redis_conn = Redis(host=redis_host, port=redis_port)
        self.queue = Queue(connection=self.redis_conn)
        self.salt = Salt()
        self.minions_list = self.salt.minions_accepted

    def job_global(self):
        self.queue.enqueue(connected)
        self.queue.enqueue(pending)
        self.queue.enqueue(denied)
        self.queue.enqueue(rejected)

    def job_info(self):
        for minion in self.minions_list:
            self.queue.enqueue(check_changes, minion)

    def job_respond(self):
        self.queue.enqueue(respond_minion)

        for minion in self.minions_list:
            self.queue.enqueue(respond_minion_db, minion)
