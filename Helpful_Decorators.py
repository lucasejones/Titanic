from functools import wraps
from functools import lru_cache
import signal 
import time

def timer(func):
    '''A decorator that prints how long a function took to run.
    
    Args:
        func (callable): The function being decorated.
    
    Returns:
        callable: the decorated function
    '''
    
    def wrapper(*args, **kwargs):
        t_start = time.time()
        result = func(*args, **kwargs)
        t_total = time.time() - t_start
        
        print('{} took {} seconds to run.'.format(func.__name__, t_total))
        return result
    
    return wrapper


@timer
def sleep_n_seconds(n):
    time.sleep(n)
    
sleep_n_seconds(5)

# ______________________________________________________________________________

def timeout(n_seconds):
    '''A decorator that will throw an error if the function doesn't run 
       by the number of seconds provided in the decorator argument.

       Args:
          int: the time in seconds before the error is thrown

       Returns:
          str: the error message itself
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.alarm(n_seconds)
            try:
                func(*args, **kwargs)
            finally:
                signal.alarm(0)
                print('{} timed out.'.format(func.__name__))
        return wrapper
    return decorator

@timeout(5)
def barr():
    time.sleep(3)
    print('barr!')
    
barr()


# ______________________________________________________________________________

# Type decorator
#   Another example, in which the decorator will print what type the result is. 
#   This can be very useful in debugging functions that return strange outputs. 
#   It confirms that the type of the output is the type that you expected.

def print_return_type(func):
    '''A decorator that will print what type the decorated function's result is.
        Args: 
            func (callable): the function being ddecorated
        Returns: 
            str: the returned type
    '''
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('{}() returned type {}'.format(func.__name__, type(result)))
        return result
    return wrapper

@print_return_type
def fly(value):
    return value

print(fly(42))
print(fly([1,2,3]))
print(fly({'a': 42}))

# ______________________________________________________________________________

# using lru_cache to speed up computation via caching results
@lru_cache
def factorial(n):
    return n * factorial(n-1) if n else 1

factorial(6)

# ______________________________________________________________________________

# Tagging Decorator
# A decorator that allows you to add tags to functions. This is useful for:

# saying who worked on a given functioin
# identifying if a function will need to be removed in production
# labelling a function as "experimental" so people know the inputs and outputs may change
def tag(tags):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result
        wrapper.tags = tags
        print(wrapper.tags)
        return wrapper
    return decorator

@tag('test tag here')
def froa(a, b):
    return a + b

froa(2, 5)