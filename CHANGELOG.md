# Changelog

## Unreleased

- CI moved from Travis CI to GitHub Actions: black, pylint (errors only) and
  a byte-compile run on every push and pull request.
- Python 3.10 replaces 3.6: the interpreter current Salt releases run on and
  bundle, since smonit imports `salt` from the same Python. Salt 3006 is the
  minimum. The lock file is regenerated for it, with gunicorn 23.0.0,
  rq 1.16.2 and APScheduler 3.10.4.
- Fixed: the scheduler enqueued jobs on Redis database 0 while the worker
  listened on database 1, so with default settings no job ever ran. Both now
  read `REDIS_DB` (default 1), and the systemd worker unit runs `worker.py`
  instead of the bare `rq worker` command, which ignored the setting.
- Fixed: an empty highstate result raised `UnboundLocalError` in
  `_minion_info`.
- README rewritten; the badges point at GitHub Actions.
- License changed from MPL 2.0 to Apache 2.0.

## v0.0.1

- Collect important activities from salt (check [roadmap](docs/list.todo))
