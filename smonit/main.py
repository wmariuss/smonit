import falcon
import pprint

from smonit.services.api import Salt
from smonit.views import Index

salt = Salt()
minions = salt.minions_accepted

for minion in minions:
    pprint.pprint(salt.cmd(minion, 'state.highstate'))
    pprint.pprint(salt.changes(minion))

app = falcon.API()
app.add_route('/', Index())
