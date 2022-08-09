"""Run ray tests.

poetry add protobuf="^3.20.1"
"""
import multiprocessing
import os
from multiprocessing import Pool
from pathlib import Path

# import joblib
import more_itertools as mit
import numpy as np
import psutil
import ray
from about_time import about_time
from logzero import logger

from radio_embed import radio_embed

num_cpus_m = multiprocessing.cpu_count()
num_cpus = psutil.cpu_count(logical=False)

filename = "fangfang-en.txt"
lines = Path(filename).read_text("utf8").splitlines()
lst = [_.strip() for _ in lines if _.strip()]

args = "\n".join(lst)
args_m = ["\n".join(elm) for elm in mit.divide(num_cpus_m, lst)]
args = ["\n".join(elm) for elm in mit.divide(num_cpus, lst)]

# with about_time() as dur: res1 = radio_embed("\n".join(lst))
# 143.72 s
# ray.init(num_cpus=num_cpus)


def test_pool(func, args_):
    """Test."""
    with Pool(num_cpus_m) as pool:
        ret = pool.map(func, args_)
    # pool.close()
    # pool.join()
    return ret

# with about_time() as dur2: res2 = test_pool(radio_embed, args_m)
# print(dur2.duration)
# forindo 26.5s  about 1/6 of 140s
# okteto 256 s! > 210s!

# res2a = np.concatenate(res2)
# np.allclose(res1, res2a, rtol=1e-05, atol=1e-07)
# np.allclose(res1, np.concatenate(res2), rtol=1e-05, atol=1e-07)

# %timeit ret = joblib.Parallel(n_jobs=num_cpus, backend='loky', verbose=0)(joblib.delayed(radio_embed)(arg) for arg in args)
# 28.1 s ± 1.08 s per loop (mean ± std. dev. of 7 runs, 1 loop each)
# with about_time() as dur4: ret4 = joblib.Parallel(n_jobs=num_cpus, backend='multiprocessing', verbose=0)(joblib.delayed(radio_embed)(arg) for arg in args)
# dur4.duration 28.48s
# ret4a = np.concatenate(ret4)
# assert np.allclose(res1, ret4a, rtol=1e-05, atol=1e-07)

os.environ["TOKENIZERS_PARALLELISM"] = "false"

if not ray.is_initialized():
    ray.init(num_cpus=num_cpus)


@ray.remote
def ray_embed(text):
    """Embed text to d-512."""
    return radio_embed(text)


def main():
    """Run."""
    _ = """
    with about_time() as dur:
        res1 = radio_embed("\n".join(lst))
    print(dur.duration_human)
    # forindo 143.72 s 137 s
    # okteto 3:33 (210s)
    # """

    with about_time() as dur5:
        _ = [ray_embed.remote(arg) for arg in args]
        res5 = ray.get(_)
    print(num_cpus, dur5.duration_human)  # forindo 40s
    # res5a = np.concatenate(res5)
    # _ = np.allclose(res1, res5a, rtol=1e-05, atol=1e-07)
    _ = np.allclose(res1, np.concatenate(res5), rtol=1e-05, atol=1e-07)
    print(_)

    ray.shutdown()
    ray.init(num_cpus=num_cpus // 2)
    with about_time() as dur5a:
        _ = [ray_embed.remote(arg) for arg in args]
        res6 = ray.get(_)
    print(num_cpus // 2, dur5a.duration_human)  # 40s
    res6a = np.concatenate(res6)
    _ = np.allclose(res5a, res6a, rtol=1e-05, atol=1e-07)

    logger.info(" res5a allclose to res6a? %s", _)

    ray.shutdown()
    ray.init(num_cpus=2)
    with about_time() as dur7:
        _ = [ray_embed.remote(arg) for arg in args]
        res7 = ray.get(_)
    print(2, dur7.duration_human)  # 90s
    res7a = np.concatenate(res7)
    _ = np.allclose(res5a, res7a, rtol=1e-05, atol=1e-07)

    logger.info(" res5a allclose to res7a? %s", _)

    # num_cpus - 1
    ray.shutdown()
    ray.init(num_cpus=num_cpus - 1)
    with about_time() as dur8:
        _ = [ray_embed.remote(arg) for arg in args]
        res8 = ray.get(_)
    print(num_cpus - 1, dur8.duration_human)  # 44s
    res8a = np.concatenate(res8)
    _ = np.allclose(res5a, res8a, rtol=1e-05, atol=1e-07)

    logger.info(" res5a allclose to res8a? %s", _)

    print(num_cpus, dur5.duration_human)  # 32s
    print(num_cpus // 2, dur5a.duration_human)  # 38s
    print(2, dur7.duration_human)  # 90s
    print(num_cpus - 1, dur8.duration_human)  # 44s


if __name__ == "__main__":
    main()
