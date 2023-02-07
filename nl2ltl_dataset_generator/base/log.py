import functools
import time

import numpy

means = {}


def log_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        # print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        if (func_name := func.__name__) in means:
            means[func_name].append(run_time)
        else:
            means[func_name] = [run_time]
        return value

    return wrapper


def get_means():
    return {k: numpy.mean(v) for k, v in means.items()}
