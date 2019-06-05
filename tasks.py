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


@task
def install(c, docker=False, compose=False):
    '''
    Install docker and docker-compose
    '''
    if docker:
        c.run("sudo apt install curl -y")
        c.run("curl -fsSL get.docker.com -o get-docker.sh")
        c.run("sudo sh get-docker.sh")
        c.run("sudo usermod -aG docker $(id -un)")
        c.run("sudo rm get-docker.sh")
    if compose:
        c.run("sudo curl -L https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose")
        c.run("sudo chmod +x /usr/local/bin/docker-compose")


@task
def build(c, containers=False):
    '''
    Build containers
    '''
    if containers:
        env_file()
        c.run("sudo docker-compose build")


@task(post=[call(build, containers=True)])
def run(c, containers=False):
    '''
    Run containers
    '''
    if containers:
        env_file()
        c.run("sudo docker-compose up -d")


@task
def upload(c, internal=False, external=False):
    '''All option based on .pypirc file
    '''
    if internal:
        c.run('python setup.py sdist upload -r pypicloud')
    if external:
        c.run('python setup.py sdist upload -r pypi')
