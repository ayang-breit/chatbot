import time
from collections import defaultdict
from functools import wraps


class memoize():
    CACHE = defaultdict(dict)

    def __init__(self, *args, **kwargs):
        self.ttl = kwargs.get('ttl', None)

        self.func = None
        if len(args) > 0: self.func = args[0]

    def __call__(self, *args, **kwargs):
        if self.func is not None:
            current_time = time.time()
            if hasattr(self.func, '__class__'):
                funcname = f'{self.func.__module__}.{self.func.__class__.__name__}.{self.func.__name__}'
            else:
                funcname = f'{self.func.__module__}.{self.func.__name__}'
            key = (args, frozenset(kwargs.items()))  # Unique key for function and its args

            if (key in self.CACHE[funcname]):
                value, timestamp = self.CACHE[funcname][key]
                if (self.ttl is None) or (current_time - timestamp < self.ttl):
                    return value

            result = self.func(*args, **kwargs)
            self.CACHE[funcname][key] = (result, current_time)
            return result
        else:
            func = args[0]

            @wraps(func)
            def wrapper(*args, **kwargs):
                current_time = time.time()
                if hasattr(func, '__class__'):
                    funcname = f'{func.__module__}.{func.__class__.__name__}.{func.__name__}'
                else:
                    funcname = f'{func.__module__}.{func.__name__}'
                key = (args, frozenset(kwargs.items()))  # Unique key for function and its args

                if (key in self.CACHE[funcname]):
                    value, timestamp = self.CACHE[funcname][key]
                    if (self.ttl is None) or (current_time - timestamp < self.ttl):
                        return value

                result = func(*args, **kwargs)
                self.CACHE[funcname][key] = (result, current_time)
                return result

            return wrapper

    @classmethod
    def clear(cls):
        cls.CACHE.clear()