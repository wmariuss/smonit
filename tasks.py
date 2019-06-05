import os
from invoke import task, call


@task
def clean(c):
    files = [
        'build',
        'dist',
        '__pycache__',
        '*.pyc',
        '*.egg-info',
        '*.whl',
        '*.pex'
    ]
    print('Cleaning up...')
    for f in files:
        c.run('rm -rf {}'.format(f))
