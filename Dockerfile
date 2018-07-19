FROM frizzlywitch/pycon2018_skill:0.15

WORKDIR /skill/
ENV PYTHONPATH=$PYTHONPATH:/skill/ FLASK_APP=/skill/seabattle/api.py
CMD flask run --host="::"

RUN pip install mock

COPY mldata/ mldata/
COPY config/ config/
COPY tests/ tests/
COPY seabattle/ seabattle/
