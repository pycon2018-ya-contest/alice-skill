# coding: utf-8

from fabric.api import task, local


@task
def train():
    local('python -m rasa_nlu.train --config spacy_config.yml --data intents_config.json --path projects')


@task
def run():
    local('python bot.py')
