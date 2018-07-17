FROM ubuntu:18.04

WORKDIR /skill/
EXPOSE 5000
CMD PYTHONPATH=$PYTHONPATH:. FLASK_APP=seabattle/api.py flask run --host="::"

RUN apt-get update && apt-get install -y python-pip git
RUN pip install -U pip

COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

COPY mldata/ .
COPY seabattle/ .
