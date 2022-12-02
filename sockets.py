#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2013-2014 Abram Hindle
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import flask
from flask import Flask, request, redirect
from flask_sockets import Sockets
import gevent
from gevent import queue
import time
import json
import os

app = Flask(__name__)
sockets = Sockets(app)
app.debug = True

class Client:
    def __init__(self) -> None:
        self.queue = queue.Queue()

    def put(self, v):
        self.queue.put_nowait(v)

    def get(self):
        return self.queue.get()

class World:
    def __init__(self):
        self.clear()
        # we've got listeners now!
        self.listeners = list()
        
    def add_set_listener(self, listener):
        self.listeners.append( listener )

    def remove_set_listener(self, listener):
        self.listeners.remove(listener)

    def update(self, entity, key, value):
        entry = self.space.get(entity,dict())
        entry[key] = value
        self.space[entity] = entry
        self.update_listeners( entity )

    def set(self, entity, data):
        self.space[entity] = data
        self.update_listeners( entity )

    def update_listeners(self, entity):
        '''update the set listeners'''
        for listener in self.listeners:
            listener(entity, self.get(entity))

    def clear(self):
        self.space = dict()

    def get(self, entity):
        return self.space.get(entity,dict())
    
    def world(self):
        return self.space

myWorld = World()
clients = []

def set_listener( entity, data ):
    ''' do something with the update ! '''
    for client in clients:
        client.put(json.dumps({entity:data}))

myWorld.add_set_listener( set_listener )
        
@app.route('/')
def hello():
    '''Return something coherent here.. perhaps redirect to /static/index.html '''
    return redirect("/static/index.html", code=302)

def read_ws(ws, client):
    '''A greenlet function that reads from the websocket and updates the world'''
    
    while True:
        msg = ws.receive()
        if (msg is not None):
            packet = json.loads(msg)
            for key in packet.keys():
                myWorld.set(key, packet[key])
        else:
            break


@sockets.route('/subscribe')
def subscribe_socket(ws):
    '''Fufill the websocket URL of /subscribe, every update notify the
       websocket and read updates from the websocket '''
    # XXX: TODO IMPLEMENT ME

    client = Client()
    clients.append(client)

    g = gevent.spawn(read_ws, ws, client)

    for i in myWorld.world().keys():
        client.put(json.dumps({i:myWorld.world()[i]}))

    try:
        while True:
            msg = client.get()
            ws.send(msg)
    except Exception as e:
        print("WS Error")
    finally:
        clients.remove(client)
        gevent.kill(g)


# I give this to you, this is how you get the raw body/data portion of a post in flask
# this should come with flask but whatever, it's not my project.
def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data.decode("utf8") != u''):
        return json.loads(request.data.decode("utf8"))
    else:
        return json.loads(request.form.keys()[0])

@app.route("/entity/<entity>", methods=['POST','PUT'])
def update(entity):
    '''update the entities via this interface'''
    req = flask_post_json()
    if (request.method == "PUT"):
        myWorld.set(entity, req)
    else:
        for key in req:
            myWorld.update(entity, key, req[key])

    return app.response_class(json.dumps(req),
                            status=200,
                            mimetype="application/json")

def parseWorld(dict):
    for key in dict:
        myWorld.set(key, dict[key])

@app.route("/world", methods=['POST','GET'])    
def world():
    '''you should probably return the world here'''
    if (request.method == "POST"):
        try:
            parseWorld(flask_post_json())
        except:
            return "Fail", 400
    return app.response_class(response=json.dumps(myWorld.world()),
                        status=200,
                        mimetype="application/json")

@app.route("/entity/<entity>")    
def get_entity(entity):
    '''This is the GET version of the entity interface, return a representation of the entity'''
    ent = myWorld.get(entity)
    if (ent == None):
        return "Not Found", 404
    else:
        return app.response_class(response=json.dumps(ent),
                            status=200,
                            mimetype="application/json")  


@app.route("/clear", methods=['POST','GET'])
def clear():
    '''Clear the world out!'''
    myWorld.clear()
    return app.response_class(response=json.dumps(myWorld.world()),
                            status=200,
                            mimetype="application/json") 


if __name__ == "__main__":
    ''' This doesn't work well anymore:
        pip install gunicorn
        and run
        gunicorn -k flask_sockets.worker sockets:app
    '''
    #server = pywsgi.WSGIServer(('', 8000), app, handler_class=WebSocketHandler)
    #server.serve_forever()
    app.run()
