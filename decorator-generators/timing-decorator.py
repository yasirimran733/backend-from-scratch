import time

def timer(func):
    def wrapper(*args,**kwargs):
        start = time.perf_counter()
        result = func(*args,**kwargs)
        end = time.perf_counter()
        print("Time = ",end-start)
        return result
    return wrapper

@timer
def counter(n):
    while n > 0:
        n-=1
# Time to execute 
counter(100000000)        