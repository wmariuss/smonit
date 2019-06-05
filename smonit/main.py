import falcon

from smonit.salt import Api
from smonit.views import Index

salt_api = Api()

print(salt_api.minion())

app = falcon.API()
app.add_route('/', Index())
