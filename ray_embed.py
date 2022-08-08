import os
from radio_embed import radio_embed
from multiprocessing import cpu_count
import ray

num_cpus = cpu_count()

os.environ["TOKENIZERS_PARALLELISM"] = "false"
if not ray.is_initialized():
    ray.init(num_cpus=num_cpus)


@ray.remote                                                             
def ray_embed(text):
    return radio_embed(text)
