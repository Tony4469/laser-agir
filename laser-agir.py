from os import  getcwd, path
import os
from os import listdir
from os.path import isfile, join

import time
import json

from flask import Flask, request
from flask_restful import Resource, Api

from threading import Timer
import urllib 


print('chemin', os.getcwd(), os.getenv('LASER_AGIR','no path'))

from source.similarity_search import Similarity

app = Flask(__name__)
api = Api(app)

import subprocess

#On définit notre environnement de travail :
local=False
if os.environ["TERM_PROGRAM"] == "Apple_Terminal":
    local=True
    
class LASER(Resource):
    def __init__(self):
        super().__init__()
        print('initializing')
    
    def start(self):
        #Désactivé pour l'instant
        #similarity = Similarity()
        return False
    
    def post(self):
        print(request.json)
        print(request.json['sentences'])
        t0 = time.process_time()
        
        #On enregistre les phrases dans le fichier langue associé
#        sentences = request.json['sentences']
#        sentences = [ tuple(sentences[x]) for x in range(len(sentences))]
        
        similarity = Similarity(lang=['en', 'fr'], p_path=os.getcwd())
        distances, indexes, cosine = similarity.launch()

        print(time.process_time() - t0, "seconds process time")
        return json.dumps({'distances': distances, 'indexes': indexes, 'cosine': cosine.tolist(), 'time': time.process_time() - t0})
    
    def get(self):
        return {'employees': "got"}


print('initialized')
#q = Queue(connection=conn)
#
#result = q.enqueue(count_words_at_url, 'http://heroku.com')
#print('resultt', result.get_id())


def begin():
    print("beginning model")
    algo=LASER()
    print("ok dwnld")
    
t = Timer(1.0, begin)
t.start() # after 15 seconds, starting process

print('launching')

api.add_resource(LASER, '/laser') # Route_1

if __name__ == '__main__':
    print('dnas main')
    app.run(port="5001")
















