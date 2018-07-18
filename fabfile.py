# coding: utf-8

from fabric.api import task, local


@task
def train():
    local('python -m rasa_nlu.train --config nlu_config.yml --data intents_config.json --path mldata/')

@task
def train_docker():
    local('docker run -it --rm -v `pwd`/mldata:/skill/mldata rasa_skill:latest '
          'python -m rasa_nlu.train --config config/nlu_config.yml --data config/intents_config.json --path mldata/')

@task
def run():
    local('PYTHONPATH=$PYTHONPATH:. python seabattle/bot.py')
