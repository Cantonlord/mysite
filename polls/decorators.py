from functools import wraps

def html_tag(tag):
    def wrap_text(msg):
        print(f'<{tag}>msg<\{tag}>')
    return wrap_text

def decorator_function(original_function):
    def wrapper_function(*args):
        print(f'wrapper executed this before {original_function.__name__}')
        return original_function(*args)
    return wrapper_function

def my_logger(orig_func):
    import logging
    logging.basicConfig(filename=f'{orig_func.__name__}.log', level=logging.INFO)

    @wraps(orig_func)
    def wrapper(*args):
        logging.info(f'Ran with args: {args}')
        return orig_func(*args)
    return wrapper


# Class decorator
class decorator_class(object):
    def __init__(self, original_function):
        self.original_function = original_function
    
    def __call__(self, *args):
        print(f'call method executed this before {self.original_function.__name__}')
        return self.original_function(*args)


@decorator_class
def display():
    print('display function ran')

@my_logger
def display_info(name, age):
    print(f'display_info ran with argument ({name}, {age})')

# display = decorator_function(display)
# display_info('Alwyn', 27)


def timer(func):
    import time
    '''Print the runtime of the decorated function'''
    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f'Finished {func.__name__!r} in {run_time:.4f} secs')
        return value
    return wrapper_timer

def debug(func):
    @wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f'{k}={v!r}' for k, v in kwargs.items()]
        signature = ', '.join(args_repr + kwargs_repr)
        print(f'Calling {func.__name__}({signature})')
        value = func(*args, **kwargs)
        print(f'{func.__name__!r} returned {value!r}')
        return value
    return wrapper_debug


@debug
def waste(num_times):
    for _ in range(num_times):
        sum([i**2 for i in range(10000)])

@debug
def make_greeting(name, age=None):
    if age is None:
        return f"Howdy {name}!"
    else:
        return f"Whoa {name}! {age} already, you are growing up!"

# print(make_greeting('Alwyn'))
print(globals())