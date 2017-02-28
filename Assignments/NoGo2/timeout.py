import signal

# When MaxTime is up, print out
def timeout(MaxTime, func, failure):
    def handler(signum, other):
        raise Exception('Time is up')       
    
    def wrapped(*args, **kwargs):
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(MaxTime)
        try:
            result = func(*args, **kwargs)
        except:
            result = failure
        finally:
            signal.alarm(0)
        return result
        
    return wrapped
