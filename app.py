from elasticsearch import Elasticsearch
from flask import Flask
from flask_cors import CORS

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/')
def data_elastic():
    es = Elasticsearch(['localhost:9200'])
    data = es.search(index='upload_data')
    result = list()
    print(data.get('hits'))
    for upload_data in data.get('hits').get('hits'):
        result.append(upload_data.get('_source'))
    return result
