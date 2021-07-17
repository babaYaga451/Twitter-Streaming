from elasticsearch import Elasticsearch
from os import environ

ES_HOST_URL = environ.get('ES_HOST_URL')

es = Elasticsearch([ES_HOST_URL], verify_certs=True)


def get_mapping():
    return '''
    {  
      "mappings":{  
          "properties":{  
            "location":{  
              "type":"geo_point"
            },
            "created_at":{
                "type": "date",
                "format": "EEE MMM dd HH:mm:ss Z yyyy"
            }
          }
        }
    }'''


es.indices.create(index='tweet-data', ignore=400, body=get_mapping())


def save(tweet):
    es.index(index='tweet-data', body=tweet)
