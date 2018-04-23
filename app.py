# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
__author__ = 'yutao'
__time__ = '2018/4/20 23:49'


from gevent import monkey
from gevent.pywsgi import WSGIServer

# 在玩websockets，可以无视之哈，有空贴下flask websockets实现哈
from geventwebsocket.handler import WebSocketHandler

import os

from flask import Flask
from flask import url_for

from celery import Celery
from celery.result import AsyncResult
import celery.states as states
from kombu import serialization
serialization.registry._decoders.pop("application/x-python-serialize")

monkey.patch_all()

env=os.environ
CELERY_BROKER_URL=env.get('CELERY_BROKER_URL','redis://127.0.0.1:6379'),
CELERY_RESULT_BACKEND=env.get('CELERY_RESULT_BACKEND','redis://127.0.0.1:6379')
CELERY_ACCEPT_CONTENT = ['json','pickle']

celery= Celery('tasks',
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND)
celery.conf.update(CELERY_ACCEPT_CONTENT = ['json','pickle'],
                   CELERY_TASK_SERIALIZER='json',
                   CELERY_RESULT_SERIALIZER='json')

env=os.environ
app = Flask(__name__)

# Send two numbers to add
@app.route('/add/<int:param1>/<int:param2>')
def add(param1,param2):
    task = celery.send_task('mytasks.add', args=[param1, param2])
    return task.id

# Check the status of the task with the id found in the add function
@app.route('/check/<string:id>')
def check_task(id):
    res = celery.AsyncResult(id)
    return res.state if res.state==states.PENDING else str(res.result)



if __name__ == '__main__':
    '''
    app.run(debug=env.get('DEBUG',True),
            port=int(env.get('PORT',5000)),
            host=env.get('HOST','0.0.0.0'))
    '''
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
