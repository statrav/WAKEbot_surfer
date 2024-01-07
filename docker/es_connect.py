import streamlit as st
from elasticsearch import Elasticsearch
from PIL import Image

ELASTIC_USERNAME = 'elastic'
ELASTIC_PASSWORD = 'YOUR_OWN_ES_PASSWORD'

es = Elasticsearch(
    "http://localhost:9200"
)

if es.ping():
    print('successfully connected')
else:
    print('not connected')