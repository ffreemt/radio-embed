import multiprocessing
import os
from multiprocessing import Pool
from pathlib import Path

import joblib
import more_itertools as mit
import ray
from about_time import about_time

os.environ["TOKENIZERS_PARALLELISM"] = "false"

if not ray.is_initialized():
    num_cpus = multiprocessing.cpu_count()
    ray.init(num_cpus=num_cpus)


def fib_loop(n):
    a, b = 0, 1
    for i in range(n + 1):
        a, b = b, a + b
    return a


@ray.remote
def fib_loop2(n):
    a, b = 0, 1
    for i in range(n + 1):
        a, b = b, a + b
    return a


def main():
    """Run."""
    _ = """
    with about_time() as dur5:
        _ = [ray_embed.remote(arg) for arg in args]
    print(dur5.duration_human)
    # """
    args = [10000] * 1600
    with about_time() as dur:
        ret = [fib_loop2.remote(arg) for arg in args]
        res = ray.get(ret)
    print(dur.duration_human)
    print(res[:2])


if __name__ == "__main__":
    main()
