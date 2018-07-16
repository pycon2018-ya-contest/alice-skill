virtualenv venv
. venv/bin/activate
pip install -U pip
python -m spacy download xx_ent_wiki_sm

?? spacy.load(xx...)
