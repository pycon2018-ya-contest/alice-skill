# coding: utf-8

from fabric.api import task, local


@task
def train():
    local('python -m rasa_nlu.train --config nlu_config.yml --data intents_config.json --path mldata/')


@task
def run():
    local('PYTHONPATH=$PYTHONPATH:. python seabattle/bot.py')
