import os
import falcon
from apscheduler.schedulers.background import BackgroundScheduler

from smonit.views import Index
from smonit.execution import Run
from smonit.services.api import InfluxDb


# influx = InfluxDb()
# print(influx.list_databases)
# print(influx.drop_database('smonit'))
# print(influx.create_database('smonit'))
# pprint.pprint(influx.query('select * from highstate_disabled'))

run = Run()
interval = os.environ.get('SCHEDULER_INTERVAL', 60)

scheduler = BackgroundScheduler()
scheduler.add_job(run.jobs_global, 'interval', minutes=2, id='global')
scheduler.add_job(run.jobs_minion, 'interval', minutes=int(interval), id='minion')
scheduler.start()

app = falcon.API()
app.add_route('/', Index())
