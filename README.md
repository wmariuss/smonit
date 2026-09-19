# Smonit

[![CI](https://github.com/wmariuss/smonit/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/wmariuss/smonit/actions/workflows/ci.yml)
[![Tag](https://img.shields.io/github/v/tag/wmariuss/smonit)](https://github.com/wmariuss/smonit/tags)
[![Python](https://img.shields.io/badge/python-3.10-3776AB)](https://www.python.org/)
[![License](https://img.shields.io/github/license/wmariuss/smonit)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Smonit watches a SaltStack master and turns what it sees into time series:
which minions are connected, pending, rejected or denied, which ones answer,
how many states each minion carries, what the last highstate changed or
failed, how long it took, and where highstate is disabled. Everything lands
in InfluxDB, and a Grafana dashboard ships with the repository.

## How it works

Smonit runs on the salt-master host and uses the Salt Python API that is
already installed there.

- A small Falcon web service (`smonit.main`) hosts an APScheduler that
  enqueues collection jobs on a schedule.
- RQ workers (`worker.py`) take the jobs from Redis and ask Salt: key
  listing, `test.ping`, `state.highstate` results.
- Results are written as points to InfluxDB. Minion responsiveness is kept
  in a small TinyDB file under `/etc/salt/smonit`.
- Grafana reads InfluxDB. The dashboard is `grafana/SMONIT_Dashboard.json`.

Schedules: minion key status every minute, minion responsiveness every two
minutes, states and highstate details every `SCHEDULER_INTERVAL` minutes.

## Requirements

- Salt master 3006 or newer
- Python 3.10, the interpreter Salt runs on: smonit imports `salt` from the
  same Python, so it has to be one Salt supports, and every current Salt
  release supports 3.8 to 3.10
- InfluxDB 1.7 or newer on the 1.x line
- Redis 4 or newer
- Grafana 6 or newer for the dashboard

## Install

Salt's official packages are "onedir" builds with their own Python 3.10
under `/opt/saltstack/salt`. Install smonit's dependencies into that Python
with `salt-pip`, and run smonit with it, so `import salt` resolves:

```bash
salt-pip install pipenv
/opt/saltstack/salt/bin/python3 -m pipenv install --deploy --system
```

With a Salt installed from PyPI into a Python 3.10 of your own, the plain
form works:

```bash
pip install pipenv
pipenv install --system --deploy
```

Tagged versions are listed under
[tags](https://github.com/wmariuss/smonit/tags).

## Configure

Settings come from the environment. `env.local.template` lists them: copy
it to `.env.local`, adjust, and `source` it before starting.

| Variable | Default | Meaning |
| --- | --- | --- |
| `INFLUXDB_ENDPOINT` | `localhost:8086` | InfluxDB host and port |
| `INFLUXDB_USER`, `INFLUXDB_PASSWORD` | `smonit`, `smonit` | InfluxDB credentials |
| `INFLUXDB_DB` | `smonit` | Database the points go to |
| `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB` | `localhost`, `6379`, `1` | Redis for the job queue |
| `SCHEDULER_INTERVAL` | `60` | Minutes between state and highstate collections |
| `LOGLEVEL` | `INFO` | Log level; the log is written to `/var/log/smonit.log` |

## Run

For a local setup, start the backing services with Docker Compose. InfluxDB,
Grafana and Redis take their credentials from `.env.docker`; see
`env.docker.template`.

```bash
cp env.docker.template .env.docker
docker compose up -d
```

Then the service and at least one worker:

```bash
bash start.sh dev   # gunicorn on :8000, reloading on change
python worker.py    # an RQ worker on the high, default and low queues
```

`bash start.sh prod` runs gunicorn with a pid file under `/run/smonit`.
Unit files for both processes are in `system/`: `smonit.service` for the
API and scheduler, `smonit-worker@.service` for workers, and `system/env`
as their environment file.

`cleanup.sh` stops the compose stack and removes its volumes.

## Dashboard

Import `grafana/SMONIT_Dashboard.json` into Grafana and point its InfluxDB
data source at the `smonit` database.

## Development

```bash
pipenv install --dev
pipenv run black .
pipenv run pylint --errors-only smonit worker.py tasks.py
```

CI runs those two checks plus a byte-compile on every push and pull request
(`.github/workflows/ci.yml`). There is no test suite yet: the code needs a
Salt master to do anything, so tests would have to stub it.

## Roadmap

See [docs/list.todo](docs/list.todo).

## Contributing

- Fork the repository
- Branch from `master` and open a pull request against it
- Keep the CI green

## License

[Apache License 2.0](LICENSE).

## Author

[Marius Stanca](mailto:me@marius.xyz)
