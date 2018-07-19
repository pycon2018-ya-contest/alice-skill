FROM python:2.7.15

WORKDIR /skill/
EXPOSE 5000

COPY requirements.txt .
RUN pip install --disable-pip-version-check --no-cache-dir -r requirements.txt \
    && rm requirements.txt \
    && python -m spacy download xx_ent_wiki_sm && python -m spacy link xx_ent_wiki_sm ru
