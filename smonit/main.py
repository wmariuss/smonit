import os
import falcon
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

from smonit.views import Index
from smonit.execution import Run


run = Run()
interval = os.environ.get("SCHEDULER_INTERVAL", 60)

executors = {
    "default": {"type": "threadpool", "max_workers": 10},
    "processpool": ProcessPoolExecutor(max_workers=3),
}
job_defaults = {"coalesce": False, "max_instances": 3}


scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)
scheduler.add_job(run.job_global, "interval", minutes=1, id="global")
scheduler.add_job(run.job_respond, "interval", minutes=2, id="response")
scheduler.add_job(run.job_info, "interval", minutes=int(interval), id="info")
scheduler.start()

app = falcon.API()
app.add_route("/", Index())
