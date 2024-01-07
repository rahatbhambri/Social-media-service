from datetime import datetime as dt
from time import perf_counter

def timeit(func):  
    def inner():
        curr = perf_counter()
        func()
        then = perf_counter()
        
        print((then - curr), "seconds" )
        
    return inner
    