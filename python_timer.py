import time

class Timeit():
    indent: int = 0
    last_indent: int = 0
    last_prefix: str = ''

    def __init__(self, name='Timeit', mute=False):
        init_start = time.perf_counter()
        if Timeit.last_indent == 0:
            self.prefix = ' ' * 4 * (Timeit.indent - 1)
        elif Timeit.last_indent == Timeit.indent:
            self.prefix = Timeit.last_prefix[:-4]
        else:
            self.prefix = Timeit.last_prefix.replace('\u2500', ' ').replace('\u250c', '\u2502').replace('\u251c', '\u2502') + ' ' * 4 * (Timeit.indent - Timeit.last_indent - 1)
        
        if Timeit.indent > 0 and Timeit.last_indent != Timeit.indent:
            self.prefix += '\u250c\u2500\u2500\u2500'  # ├───
        elif Timeit.indent > 0 and Timeit.last_indent == Timeit.indent:
            self.prefix += '\u251c\u2500\u2500\u2500'  # ┌───
        self.name = self.prefix + name
        self.mute = mute
        init_end = time.perf_counter()
        self.init_time = init_end - init_start

    def __enter__(self):
        Timeit.indent += 1
        self.start = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.mute:
            t = time.perf_counter() - self.start
            # automatically choose the unit of time (s, ms, us)
            if t > 1:
                print('{}: {:.2f} s'.format(self.name, t))
            elif t > 1e-3:
                print('{}: {:.2f} ms'.format(self.name, t * 1e3))
            elif t > 1e-4:
                print('{}: {:.2f} us'.format(self.name, t * 1e6))
            else:
                print('{}: {:.2f} us \33[90m(mytimeit costs additional {:.2f} us)\33[0m'.format(self.name, t * 1e6, self.init_time * 1e6))

        Timeit.indent -= 1
        Timeit.last_prefix = self.prefix
        Timeit.last_indent = Timeit.indent


def timeit(name=None, mute=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with Timeit(func.__name__ if name is None else name, mute=mute):
                return func(*args, **kwargs)
        return wrapper
    return decorator
