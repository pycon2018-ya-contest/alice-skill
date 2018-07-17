FROM ubuntu:18.04

WORKDIR /skill/

RUN apt-get update && apt-get install -y python-pip git
RUN pip install -U pip

COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

COPY mldata/ .
COPY seabattle/ .
CMD PYTHONPATH=$PYTHONPATH:. python seabattle/bot.py
