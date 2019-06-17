#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

import subprocess

#print('installing faiss')    
#process = subprocess.Popen("conda install faiss faiss-cpu -c pytorch", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#(output, err) = process.communicate() #now wait plus that you can send commands to process
##This makes the wait possible
#p_status = process.wait()
##This will give you the output of the command being executed
#print("Command faiss output: ",output)

from source.similarity_search import Similarity

app = Flask(__name__)
api = Api(app)

class LASER(Resource):
    def __init__(self):
        super().__init__()
        self.similarity = Similarity(p_path=os.getcwd())
        print('initializing',flush=True)
    
    def start(self):
        #Désactivé pour l'instant
        #similarity = Similarity()
        return False
    
    def post(self):
        print(request.json['sentences'],flush=True)
        t0 = time.process_time()
        
        #On enregistre les phrases dans le fichier langue associé
        sentences = request.json['sentences']
        sentences = [ tuple(sentences[x]) for x in range(len(sentences))]
        
        lan_sent = set([lan for sent, lan in sentences])
        for lan in lan_sent:
            file = open(os.path.normpath(os.path.join(os.getcwd(), './tasks/similarity/dev/input.'+lan) ),"w", encoding="utf-8") 
            for sent, lang in sentences:
                if lang == lan:
                    file.write( sent + '\n' )
            file.close() 
    
#        similarity = Similarity(lang=['en', 'fr'], p_path=os.getcwd())
        print(time.process_time() - t0, " seconds intermediate process time", flush=True)
        distances, indexes, cosine = self.similarity.launch(['en', 'fr'])

        print(time.process_time() - t0, " seconds process time", flush=True)
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
















