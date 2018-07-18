FROM frizzlywitch/pycon2018_skill:0.8

WORKDIR /skill/
CMD PYTHONPATH=$PYTHONPATH:/skill/ FLASK_APP=/skill/seabattle/api.py flask run --host="::"
