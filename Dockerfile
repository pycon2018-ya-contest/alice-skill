FROM frizzlywitch/pycon2018_skill:0.13

WORKDIR /skill/
CMD PYTHONPATH=$PYTHONPATH:/skill/ FLASK_APP=/skill/seabattle/api.py flask run --host="::"

COPY mldata/ mldata/
COPY config/ config/
COPY seabattle/ seabattle/
