from celery import shared_task
from time import sleep 
import random

@shared_task
def delayed_sum(a, b):
    d = random.randint(5, 15)
    sleep(d)
    print(a+b, "Async result")
    return a+b

