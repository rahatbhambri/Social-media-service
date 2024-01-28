from celery import shared_task
from time import sleep 
import random
from datetime import datetime as dt
from myproject.settings import Db


@shared_task
def delayed_sum(a, b):
    d = random.randint(5, 15)
    sleep(d)
    print(a+b, "Async result")
    return a+b



@shared_task
def accumulate_message(from_em, to_em, message):

    mssg_payl = {
        "from" : from_em, 
        "to" : to_em, 
        "timestamp" : dt.now(),
        "message" : message
        }
    Db.messages.insert_one(mssg_payl)
    return "message inserted"