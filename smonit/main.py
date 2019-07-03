import os
import falcon
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

from smonit.views import Index
from smonit.execution import Run
from smonit.services.api import InfluxDb


run = Run()
interval = os.environ.get('SCHEDULER_INTERVAL', 60)

executors = {
        'default': {'type': 'threadpool', 'max_workers': 10},
        'processpool': ProcessPoolExecutor(max_workers=3)
    }
job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }


def jobs():
    run.job_global()
    run.job_respond_minion()


scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)
scheduler.add_job(jobs, 'interval', minutes=2, id='jobs')
scheduler.add_job(run.job_minion, 'interval', minutes=int(interval), id='job_minion')
scheduler.start()

app = falcon.API()
app.add_route('/', Index())
