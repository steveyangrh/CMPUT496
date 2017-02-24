import signal

# When MaxTime is up, print out
def timeout(MaxTime, func, failure):
    def handler(signum, other):
        print ('Time is up')       
    
    signal.alarm(MaxTime)
    signal.signal(signal.SIGALRM, handler)
            
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return failure
        
    return wrapped

