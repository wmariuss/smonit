# smonit

[__This is a prototype__]

Monitor salt activities.

What are the features:

* collect all minions (connected, pending, denied, rejected, active)
* collect states for every minion
* changes (success and failures) for every state
* execution time and status of the last highstate run
* minions with highstate disabled
* can be used instead of the default salt scheduler
* integrate easily with Grafana
* more soon

## Requirements

* `Python >= 3.6`
* `influxdb >= 1.7.6`
* `salt-master >= 2018.3.2`
* `redis >=  4.0.9`

## Install

Development

* `pip install pipenv`
* `pipenv install --system --deploy`

For stable version, please check [releases](https://github.com/wmariuss/smonit/tags) section.

## Usage

* Run `sh start.sh`

## Tests

Soon.

## Authors

* [Marius Stanca](mailto:me@marius.xyz)
