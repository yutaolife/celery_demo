# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'yutao'
__time__ = '2018/4/21 00:35'

import os
from celery import Celery
from time import sleep
from kombu import serialization
serialization.registry._decoders.pop("application/x-python-serialize")


CELERY_ACCEPT_CONTENT = ['json','pickle']

env = os.environ
app = Celery(
    'tasks',
    broker=env.get('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0'),
    backend=env.get('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/0')
)
app.conf.update(CELERY_ACCEPT_CONTENT = ['json','pickle'],
                   CELERY_TASK_SERIALIZER='json',
                   CELERY_RESULT_SERIALIZER='json')


@app.task(name='mytasks.add')
def add(x, y):
    sleep(7)  # mimic long process with sleep
    return x + y