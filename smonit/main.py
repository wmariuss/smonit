import falcon
import logging
import pprint

from smonit.services.api import Salt
from smonit.services.api import InfluxDB
from smonit.views import Index

salt = Salt()
influx = InfluxDB()
minions = salt.minions_accepted

# pprint.pprint(salt.cmd('saltd', 'state.highstate'))
pprint.pprint(salt.changes('saltd'))

# for minion in minions:
#     pprint.pprint(salt.cmd(minion, 'state.highstate'))
#     pprint.pprint(salt.changes(minion))

app = falcon.API()
app.add_route('/', Index())
